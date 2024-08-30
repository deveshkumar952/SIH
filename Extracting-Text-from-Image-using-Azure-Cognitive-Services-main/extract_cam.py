import cv2
import time
import numpy as np
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

# Configuration
API_KEY = "f589704f25234f469768230302e1759a"
ENDPOINT = "https://computervisionmodel1.cognitiveservices.azure.com/"

# Initialize Computer Vision client
computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))

# Initialize camera
cap = cv2.VideoCapture(0)

while True:
    # Read frame from camera
    ret, frame = cap.read()
    
    # Display frame
    cv2.imshow('Camera', frame)
    
    # Check for 'c' key press to capture image
    if cv2.waitKey(1) & 0xFF == ord('c'):
        # Save frame to file
        cv2.imwrite('captured_image.jpg', frame)
        
        # Extract text from captured image
        local_image = 'captured_image.jpg'
        read_response = computervision_client.read_in_stream(open(local_image, 'rb'), language='en', raw=True)
        read_operation_location = read_response.headers["Operation-Location"]
        operation_id = read_operation_location.split("/")[-1]

        while True:
            read_result = computervision_client.get_read_result(operation_id)
            if read_result.status not in ['notStarted', 'running']:
                break
            time.sleep(1)

        if read_result.status == OperationStatusCodes.succeeded:
            text = ''
            for text_result in read_result.analyze_result.read_results:
                for line in text_result.lines:
                    text += line.text + ' '
                    text += '\n'
            open('output.txt', 'w').write(text)
            print("Text successfully written in output file")
        
    # Check for 'q' key press to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release camera and close window
cap.release()
cv2.destroyAllWindows()