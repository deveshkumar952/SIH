from pdf2docx import Converter

def convert_pdf_to_word(pdf_file_path, word_file_path):
    """
    Converts a PDF file to a Word document.

    :param pdf_file_path: The path to the PDF file.
    :param word_file_path: The path to save the Word document.
    """
    try:
        cv = Converter(pdf_file_path)
        cv.convert(word_file_path, start=0, end=None)
        cv.close()
        print(f"Word document saved as {word_file_path}")
    except Exception as e:
        print(f"Error converting PDF to Word: {e}")
