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

# Home page route
@app.route('/')
def home():
    # This page now contains a link to the image-to-text converter page
    return render_template('home1.html')  # Your home page (TEXT.CON)

# Route for the image-to-text converter page
@app.route('/image-to-text')
def image_to_text():
    # Render the image converter page with the form for uploading an image
    return render_template('index.html')

# Route to handle image upload and text extraction
@app.route('/upload', methods=['POST'])
def upload_image():
    # Ensure that a file is uploaded
    if 'file' not in request.files:
        return redirect(url_for('image_to_text'))
    
    file = request.files['file']
    
    # Ensure that a file is selected
    if file.filename == '':
        return redirect(url_for('image_to_text'))
    
    if file:
        # Save the uploaded image to the 'uploads' directory
        image_path = os.path.join('uploads', file.filename)
        file.save(image_path)
        
        # Use Azure's OCR to extract text from the image
        with open(image_path, 'rb') as image_stream:
            read_response = computervision_client.read_in_stream(image_stream, language='en', raw=True)
        
        # Extract the operation ID from the response headers
        read_operation_location = read_response.headers["Operation-Location"]
        operation_id = read_operation_location.split("/")[-1]
        
        # Poll for the OCR result
        while True:
            read_result = computervision_client.get_read_result(operation_id)
            if read_result.status not in ['notStarted', 'running']:
                break
            time.sleep(1)
        
        # Collect the extracted text
        extracted_text = ''
        if read_result.status == OperationStatusCodes.succeeded:
            for text_result in read_result.analyze_result.read_results:
                for line in text_result.lines:
                    extracted_text += line.text + '\n'
        
        # Render a results page displaying the extracted text
        return render_template('result.html', text=extracted_text)
    
    # Redirect back to the image-to-text converter page if no file was provided
    return redirect(url_for('image_to_text'))

# Ensure the 'uploads' directory exists
if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
