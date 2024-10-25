# Rule-Engine-with-AST
Develop a simple 3-tier rule engine application(Simple UI, API and Backend, Data) to determine user eligibility based on attributes like age, department, income, spend etc.The system can use Abstract Syntax Tree (AST) to represent conditional rules and allow for dynamic creation,combination, and modification of these rules.
# Data Structure:
● Define a data structure to represent the AST.
● The data structure should allow rule changes
● E,g One data structure could be Node with following fields
○ type: String indicating the node type ("operator" for AND/OR, "operand" for
conditions)
○ left: Reference to another Node (left child)
○ right: Reference to another Node (right child for operators)
○ value: Optional value for operand nodes (e.g., number for comparisons)
Data Storage
● Define the choice of database for storing the above rules and application metadata
● Define the schema with samples.
# Sample Rules:
● rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND
department = 'Marketing')) AND (salary > 50000 OR experience >
5)"
● rule2 = "((age > 30 AND department = 'Marketing')) AND (salary >
20000 OR experience > 5)"
# API Design:
1. create_rule(rule_string): This function takes a string representing a rule (as
shown in the examples) and returns a Node object representing the corresponding AST.
2. combine_rules(rules): This function takes a list of rule strings and combines them
into a single AST. It should consider efficiency and minimize redundant checks. You can
explore different strategies (e.g., most frequent operator heuristic). The function should
return the root node of the combined AST.
3. evaluate_rule(JSON data): This function takes a JSON representing the combined
rule's AST and a dictionary data containing attributes (e.g., data = {"age": 35,
"department": "Sales", "salary": 60000, "experience": 3}). The
function should evaluate the rule against the provided data and return True if the user is
of that cohort based on the rule, False otherwise.
Here’s an overview of your **Rule Engine with AST (Abstract Syntax Tree)** project:

### Project Description
This project involves building a rule engine that uses an Abstract Syntax Tree (AST) to parse and evaluate user-defined conditional rules. The rules are defined in a simple, human-readable format (e.g., `(age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')`) and parsed into an AST, which represents the logical structure of the conditions. The system stores these rules in a database and provides an evaluation mechanism to test if a set of data meets the rule conditions.

### Project Structure
The project has the following structure:
```
/rule_engine_project
    /static
        - style.css
        - script.js
    - app.py               # Main Flask application file
    - rule_engine.db       # SQLite database storing rules
    - index.html           # Main HTML page for the web interface
```

### Core Functionalities
1. **Rule Creation**
   - Users input rules in a specific format, e.g., `(age > 30 AND department = 'Sales')`.
   - The rule string is parsed into an AST structure that is stored in the database along with the original rule string.
   - The AST captures the logical flow, operators, and conditions in a nested dictionary format that simplifies evaluation.

2. **Rule Evaluation**
   - Users submit a rule ID and data in JSON format, such as:
     ```json
     {
         "age": 32,
         "department": "Sales"
     }
     ```
   - The system retrieves the AST from the database, then traverses and evaluates it against the provided data to see if the conditions are met.

### Key Components
1. **Flask Web Application (`app.py`)**:
   - Provides endpoints for creating and evaluating rules.
   - Manages database connections and communicates with the frontend.

2. **SQLite Database (`rule_engine.db`)**:
   - Stores rule strings and their AST representations.
   - Allows rule persistence and retrieval by ID.

3. **Frontend (`index.html`, `style.css`, `script.js`)**:
   - The web interface lets users input rule strings, view rule IDs upon creation, and evaluate rules by entering rule IDs and JSON data.

### Example Workflow
1. **Define a Rule**:
   - Input a rule string, e.g., `(age > 30 AND department = 'Sales')`.
   - The rule is stored with an assigned ID.

2. **Evaluate a Rule**:
   - Provide the rule ID and data to evaluate, e.g., `{"age": 32, "department": "Sales"}`.
   - The system checks if the data meets the conditions specified by the rule.
   - Returns the evaluation result (`True` or `False`).

### Key Benefits
- **Dynamic Rule Definition**: Users can create custom rules as needed without hardcoding them.
- **Flexible Evaluations**: Rules are stored in an AST format, making evaluations efficient and flexible.
- **Web Interface**: Provides an easy way to interact with the rule engine without needing command-line access.

### Potential Extensions
- **Complex Rule Parsing**: Extend the parser to support more operators (`>=`, `<=`, `!=`) and nested logic.
- **Enhanced Validation**: Add validation for the JSON data against the required rule fields.
- **User Authentication**: Implement user accounts and permissions to restrict rule access.

This project provides a foundation for any system requiring user-defined conditional logic, such as eligibility verification, access control, and more. It’s designed to be straightforward yet extendable, providing a flexible framework for various applications.
