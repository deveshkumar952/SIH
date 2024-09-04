from flask import Flask, request, render_template, redirect, url_for
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import os
import time

app = Flask(__name__)

# Azure Cognitive Services credentials
API_KEY = "f589704f25234f469768230302e1759a"
ENDPOINT = "https://computervisionmodel1.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(url_for('home'))
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(url_for('home'))
    
    if file:
        image_path = os.path.join('uploads', file.filename)
        file.save(image_path)
        
        # Use Azure OCR to read text from image
        with open(image_path, 'rb') as image_stream:
            read_response = computervision_client.read_in_stream(image_stream, language='en', raw=True)
        
        read_operation_location = read_response.headers["Operation-Location"]
        operation_id = read_operation_location.split("/")[-1]
        
        # Polling for the OCR result
        while True:
            read_result = computervision_client.get_read_result(operation_id)
            if read_result.status not in ['notStarted', 'running']:
                break
            time.sleep(1)
        
        extracted_text = ''
        if read_result.status == OperationStatusCodes.succeeded:
            for text_result in read_result.analyze_result.read_results:
                for line in text_result.lines:
                    extracted_text += line.text + '\n'
        
        # Render result page with extracted text
        return render_template('result.html', text=extracted_text)
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
