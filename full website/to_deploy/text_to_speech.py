import pyttsx3

def text_to_speech(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set properties before adding anything to speak
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

    # Pass the text to the speech engine
    engine.say(text)

    # Run the speech engine
    engine.runAndWait()

if __name__ == "__main__":
    # Provide the path to the file containing the OCR output
    file_path = "C:/Users/priya/OneDrive/Desktop/ocr/ocr_practice/output_text.txt" 
    
    # Read the text from the file
    with open(file_path, "r") as file:
        ocr_output = file.read()

    # Call the text-to-speech function
    text_to_speech(ocr_output)