document.addEventListener("DOMContentLoaded", function () {
    const createRuleForm = document.getElementById("createRuleForm");
    const evaluateRuleForm = document.getElementById("evaluateRuleForm");
    const createRuleResult = document.getElementById("createRuleResult");
    const evaluateRuleResult = document.getElementById("evaluateRuleResult");

    // Handle Create Rule form submission
    createRuleForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent default form submission
        const ruleString = document.getElementById("ruleString").value;

        fetch('/create_rule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ rule_string: ruleString })
        })
        .then(response => response.json())
        .then(data => {
            createRuleResult.innerHTML = `Rule created with ID: ${data.rule_id}`;
        })
        .catch(error => {
            createRuleResult.innerHTML = `Error: ${error.message}`;
        });
    });

    // Handle Evaluate Rule form submission
    evaluateRuleForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent default form submission
        const ruleId = document.getElementById("ruleId").value;
        const data = document.getElementById("data").value;

        fetch('/evaluate_rule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                rule_id: ruleId,
                data: data
            })
        })
        .then(response => response.json())
        .then(data => {
            evaluateRuleResult.innerHTML = `Evaluation result: ${data.result}`;
        })
        .catch(error => {
            evaluateRuleResult.innerHTML = `Error: ${error.message}`;
        });
    });
});
function evaluateRule() {
    const ruleId = document.getElementById('evaluate_rule_id').value;
    const jsonData = document.getElementById('json_input').value; // Your JSON data as string

    fetch('/evaluate_rule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'rule_id': ruleId,
            'data': jsonData
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = 'Evaluation result: ' + data.result;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'Evaluation result: ' + error.message;
    });
}
