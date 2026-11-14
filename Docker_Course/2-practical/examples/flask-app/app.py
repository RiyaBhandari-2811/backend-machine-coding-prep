"""
Flask Application Example for Docker
Simple multiplication table app (same as in the transcript)
"""

from flask import Flask, render_template_string, request

app = Flask(__name__)

# Simple HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Multiplication Table Generator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        input {
            padding: 10px;
            font-size: 16px;
            width: 100%;
            max-width: 200px;
        }
        button {
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 10px;
        }
        button:hover {
            background-color: #0056b3;
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            background-color: #f9f9f9;
            border-left: 4px solid #007bff;
        }
        .table {
            font-family: monospace;
            font-size: 16px;
            line-height: 1.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Multiplication Table Generator</h1>
        <p>Enter a number to see its multiplication table (1-10):</p>
        
        <form method="post">
            <input type="number" name="number" placeholder="Enter a number" required>
            <button type="submit">Generate Table</button>
        </form>
        
        {% if result %}
        <div class="result">
            <h3>Multiplication Table of {{ number }}:</h3>
            <div class="table">
                {% for row in result %}
                {{ row }}<br>
                {% endfor %}
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    """Home endpoint with multiplication table"""
    result = None
    number = None
    
    if request.method == 'POST':
        try:
            number = int(request.form.get('number'))
            if 1 <= number <= 1000:
                result = [f"{number} × {i} = {number * i}" for i in range(1, 11)]
            else:
                result = ["Please enter a number between 1 and 1000"]
        except ValueError:
            result = ["Please enter a valid number"]
    
    return render_template_string(HTML_TEMPLATE, result=result, number=number)

@app.route('/health')
def health_check():
    """Health check endpoint for Docker"""
    return {"status": "ok", "service": "Flask App"}, 200

if __name__ == '__main__':
    # Important: Listen on 0.0.0.0 so container is accessible from outside
    app.run(host='0.0.0.0', port=5000, debug=True)
