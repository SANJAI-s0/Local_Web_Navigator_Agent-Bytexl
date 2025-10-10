from webagent.webapp import app

if __name__ == '__main__':
    # Ensure data directory exists
    import os
    os.makedirs('data', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
