from flask import Flask, request, jsonify, render_template
from python import extract_cam
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    # Replace this with your actual processing function
    result = my_function(data['input'])
    return jsonify({'result': result})

def my_function(input_data):
    # Example function; replace with your actual logic
    return f"Processed {input_data}"

if __name__ == '__main__':
    app.run(debug=True)
