from fpdf import FPDF

def convert_document_to_pdf(input_path, output_path):
    """
    Converts a JPG image to a PDF file.

    :param input_path: Path to the input JPG file.
    :param output_path: Path where the PDF will be saved.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    
    # Add image to PDF
    pdf.image(input_path, x=10, y=10, w=190)  # Adjust x, y, and w as needed
    
    # Output the PDF
    pdf.output(output_path)
    print(f"PDF saved as {output_path}")

if __name__ == "__main__":
    # Test the conversion
    input_image_path = "path/to/your/image.jpg"  # Replace with the actual image path
    output_pdf_path = "path/to/your/output.pdf"  # Replace with the desired output PDF path
    
    convert_document_to_pdf(input_image_path, output_pdf_path)
