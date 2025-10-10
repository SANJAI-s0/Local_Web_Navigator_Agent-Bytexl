# webagent/main.py
from flask import Flask, request, render_template
from webagent.agent import WebAgent

app = Flask(__name__)
agent = WebAgent(headless=True)

@app.route('/', methods=['GET', 'POST'])
def search():
    results = None
    plan = None
    error = None
    if request.method == 'POST':
        instruction = request.form.get('instruction', '').strip()
        if instruction:
            try:
                plan = agent.parse_and_plan(instruction)
                results = agent.execute_plan(plan)
            except Exception as e:
                error = str(e)
    return render_template('index.html', plan=plan, results=results, error=error)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
