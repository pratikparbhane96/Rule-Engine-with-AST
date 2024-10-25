from flask import Flask, request, jsonify, render_template
import sqlite3
import json
import re

app = Flask(__name__, template_folder='.')

def get_db_connection():
    conn = sqlite3.connect('rule_engine.db')
    conn.row_factory = sqlite3.Row  # Allows access to rows as dictionaries
    return conn

# Define the function to parse the rule string into an AST
def parse_rule(rule_string):
    tokens = re.findall(r"\(|\)|\w+|\'\w+\'|AND|OR|>|<|=", rule_string)

    def parse_expression(index):
        node = {'type': None, 'value': None, 'left': None, 'right': None}

        while index < len(tokens):
            token = tokens[index]

            if token == '(':
                sub_node, index = parse_expression(index + 1)
                if node['left'] is None:
                    node['left'] = sub_node
                else:
                    node['right'] = sub_node
            elif token == ')':
                return node, index
            elif token in {'AND', 'OR'}:
                node['type'] = 'operator'
                node['value'] = token
            elif token in {'>', '<', '='}:
                node['type'] = 'operand'
                node['value'] = token
                node['left'] = tokens[index - 1]  # Operand (attribute)
                node['right'] = tokens[index + 1]  # Operand (value)
                return node, index + 1
            else:
                if node['left'] is None:
                    node['left'] = token
                elif node['right'] is None:
                    node['right'] = token

            index += 1

        return node, index

    ast, _ = parse_expression(0)
    return ast

# Database Initialization
def init_db():
    conn = sqlite3.connect('rule_engine.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS rules (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        rule_string TEXT,
                        ast_representation TEXT
                    )''')
    conn.commit()
    conn.close()

# Save rule and AST representation to the database
def save_rule_to_db(rule_string, ast_representation):
    conn = sqlite3.connect('rule_engine.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO rules (rule_string, ast_representation) VALUES (?, ?)",
                   (rule_string, json.dumps(ast_representation)))
    conn.commit()
    conn.close()

# Evaluate the AST with the given data
def evaluate_ast(ast, data):
    if ast['type'] == 'operator':
        left_value = evaluate_ast(ast['left'], data)
        right_value = evaluate_ast(ast['right'], data)
        if ast['value'] == 'AND':
            return left_value and right_value
        elif ast['value'] == 'OR':
            return left_value or right_value
    elif ast['type'] == 'operand':
        left_attr = ast['left']
        operator = ast['value']
        right_value = ast['right'].strip("'")  # Remove quotes for string comparison
        
        # Debugging output
        print(f"Evaluating: {left_attr} {operator} {right_value}, Data: {data[left_attr]}")

        if left_attr in data:
            if operator == '>':
                return data[left_attr] > int(right_value)  # Ensure right_value is treated as an int
            elif operator == '<':
                return data[left_attr] < int(right_value)
            elif operator == '=':
                return data[left_attr] == right_value
    return False

# Route to create a new rule
@app.route('/create_rule', methods=['POST'])
def create_rule():
    rule_string = request.json.get('rule_string')

    if not rule_string:
        return jsonify({"error": "No rule string provided"}), 400

    # Parse the rule string into an AST
    ast_representation = parse_rule(rule_string)

    # Connect to the database and insert the rule
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO rules (rule_string, ast_representation) VALUES (?, ?)",
                   (rule_string, str(ast_representation)))
    conn.commit()
    rule_id = cursor.lastrowid
    conn.close()

    return jsonify({"message": "Rule created", "rule_id": rule_id})

# Route to evaluate a rule
@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule():
    try:
        # Expecting JSON input
        request_data = request.json
        rule_id = request_data.get('rule_id')
        data = request_data.get('data')

        if rule_id is None or data is None:
            raise ValueError("Both 'rule_id' and 'data' must be provided.")

        conn = sqlite3.connect('rule_engine.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ast_representation FROM rules WHERE id = ?", (rule_id,))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            raise ValueError("Rule not found.")

        ast_representation = json.loads(row[0])
        result = evaluate_ast(ast_representation, data)

        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
