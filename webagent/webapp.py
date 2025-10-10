from flask import Flask, render_template, request, jsonify
from .agent import WebAgent
import os

app = Flask(__name__)

# Configure template folder path
app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')

# Initialize agent with error handling
try:
    agent = WebAgent()
except Exception as e:
    print(f"Failed to initialize agent: {str(e)}")
    agent = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    if not agent:
        return jsonify({'error': 'Agent not initialized'}), 500

    data = request.json
    instruction = data.get('instruction', '').strip()

    if not instruction:
        return jsonify({'error': 'No instruction provided'}), 400

    try:
        plan = agent.parse_and_plan(instruction)
        results = agent.execute_plan(plan)
        return jsonify({
            'plan': plan,
            'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/voice', methods=['POST'])
def voice_input():
    return jsonify({'status': 'Voice input not implemented'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
