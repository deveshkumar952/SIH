import requests
import time
import os

# Azure credentials and OCR URL
subscription_key = "f589704f25234f469768230302e1759a"
endpoint = "https://computervisionmodel1.cognitiveservices.azure.com/"
ocr_url = endpoint + "vision/v3.2/read/analyze"

def extract_text_from_image(image_path):
    # Read the image into a byte array
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "application/octet-stream"
    }

    response = requests.post(ocr_url, headers=headers, data=image_data)

    if response.status_code != 202:
        raise Exception(f"Failed to analyze image. Status code: {response.status_code}, Response: {response.text}")

    operation_url = response.headers.get("Operation-Location")

    if not operation_url:
        raise Exception("Operation-Location header not found in response")

    # Wait for the OCR operation to complete
    print("Waiting for OCR results...")
    time.sleep(10)  # Increased sleep time for reliable result fetching

    result_response = requests.get(operation_url, headers={"Ocp-Apim-Subscription-Key": subscription_key})

    if result_response.status_code != 200:
        raise Exception(f"Failed to retrieve results. Status code: {result_response.status_code}, Response: {result_response.text}")

    results = result_response.json()

    extracted_text = []
    if results["status"] == "succeeded":
        for read_result in results["analyzeResult"]["readResults"]:
            for line in read_result["lines"]:
                extracted_text.append({
                    'text': line["text"],
                    'boundingBox': line["boundingBox"]
                })
    else:
        raise Exception(f"OCR operation did not succeed. Status: {results['status']}, Details: {results.get('analyzeResult', {})}")

    return extracted_text

def format_text(extracted_text):
    # Sort lines by their vertical position (top) and horizontal position (left)
    lines = sorted(extracted_text, key=lambda x: (x['boundingBox'][1], x['boundingBox'][0]))

    formatted_text = []
    last_bottom = None
    last_left = None

    for item in lines:
        text = item['text']
        top = item['boundingBox'][1]
        left = item['boundingBox'][0]

        if last_bottom is not None:
            # Check if the current line is far enough from the last line to be considered a new line
            if top > (last_bottom + 10):  # 10 is a threshold to detect line breaks; adjust if needed
                formatted_text.append("")  # Add a blank line for spacing

        # Calculate indentation based on horizontal position
        indent = " " * int(left / 10)  # Adjust multiplier as needed for your specific case

        formatted_text.append(indent + text)

        last_bottom = top + item['boundingBox'][3]  # Update last_bottom for the next line
        last_left = left

    return "\n".join(formatted_text)

def save_text_to_file(text, output_file_path):
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"Formatted text has been saved to {output_file_path}")

def process_image(input_image_path, output_text_file_path):
    # Extract text from the image using Azure OCR
    extracted_text = extract_text_from_image(input_image_path)

    # Format the extracted text
    formatted_text = format_text(extracted_text)

    # Save the formatted text to the file
    save_text_to_file(formatted_text, output_text_file_path)

# Example usage
input_image_path = "C:/Users/priya/Downloads/formattest2.jpg"
output_text_file_path = "C:/Users/priya/OneDrive/Desktop/ocr/ocr_practice/output_text.txt"

process_image(input_image_path, output_text_file_path)
