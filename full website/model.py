import requests
import time

subscription_key = "f589704f25234f469768230302e1759a"
endpoint = "https://computervisionmodel1.cognitiveservices.azure.com/"
ocr_url = endpoint + "vision/v3.2/read/analyze"

def analyze_image(image_path, output_file):
    # Read the image into a byte array
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "application/octet-stream"
    }

    response = requests.post(ocr_url, headers=headers, data=image_data)

    if response.status_code != 202:
        raise Exception("Failed to analyze image. Status code: {}".format(response.status_code))

    operation_url = response.headers["Operation-Location"]

    # Wait for the OCR operation to complete
    print("Waiting for OCR results...")
    time.sleep(5)

    result_response = requests.get(operation_url, headers={"Ocp-Apim-Subscription-Key": subscription_key})

    if result_response.status_code != 200:
        raise Exception("Failed to retrieve results. Status code: {}".format(result_response.status_code))

    results = result_response.json()

    if results["status"] == "succeeded":
        with open(output_file, "w", encoding="utf-8") as output_file_handle:
            for read_result in results["analyzeResult"]["readResults"]:
                for line in read_result["lines"]:
                    output_file_handle.write(line["text"] + "\n")
        return True
    else:
        raise Exception("OCR operation did not succeed. Status: {}".format(results["status"]))
