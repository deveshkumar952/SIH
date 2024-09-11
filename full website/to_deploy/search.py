from termcolor import colored

def search_and_highlight(file_path, search_term):
    """
    Searches for a specific term in a text file, highlights it, and prints the entire content with the highlighted term.
    
    :param file_path: Path to the text file to search in.
    :param search_term: The term to search for in the file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Check if the search term is found
    if search_term.lower() in content.lower():
        # Highlight all occurrences of the search term
        highlighted_content = content.lower().replace(search_term.lower(), colored(search_term, "yellow"))
        print(highlighted_content)
    else:
        print(f"'{search_term}' not found in {file_path}.")

if __name__ == "__main__":
    # Path to the file where OCR output is stored
    file_path = "C:/Users/priya/OneDrive/Desktop/ocr/ocr_practice/output_text.txt"  # Replace with the actual path to your OCR output file
    
    # Term to search for in the file
    search_term = input("Enter the term you want to search for: ")

    # Call the search and highlight function
    search_and_highlight(file_path, search_term)