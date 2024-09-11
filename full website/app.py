from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
from model import analyze_image
from model_jpg_to_pdf import convert_document_to_pdf
from model_pdf_to_word import convert_pdf_to_word
from advanced_ocr import process_image  # Import the advanced OCR function

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(image_path)
        
        output_file = os.path.join(OUTPUT_FOLDER, 'output_text.txt')

        try:
            success = analyze_image(image_path, output_file)
            if success:
                with open(output_file, 'r', encoding='utf-8') as file:
                    text_content = file.read()
                return render_template('index.html', text=text_content)
        except Exception as e:
            return str(e)

@app.route('/jpg_to_pdf_page')
def jpg_to_pdf_page():
    return render_template('jpg_to_pdf.html')

@app.route('/jpg_to_pdf', methods=['POST'])
def jpg_to_pdf():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        jpg_path = os.path.join(UPLOAD_FOLDER, file.filename)
        pdf_path = os.path.join(OUTPUT_FOLDER, f"{os.path.splitext(file.filename)[0]}.pdf")
        file.save(jpg_path)
        try:
            convert_document_to_pdf(jpg_path, pdf_path)
            return render_template('jpg_to_pdf.html', pdf_url=url_for('download_file', filename=os.path.basename(pdf_path)))
        except Exception as e:
            return str(e)

@app.route('/pdf_to_word_page')
def pdf_to_word_page():
    return render_template('pdf_to_word.html')

@app.route('/pdf_to_word', methods=['POST'])
def pdf_to_word():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
        word_path = os.path.join(OUTPUT_FOLDER, f"{os.path.splitext(file.filename)[0]}.docx")
        file.save(pdf_path)
        try:
            convert_pdf_to_word(pdf_path, word_path)
            return render_template('pdf_to_word.html', word_url=url_for('download_file', filename=os.path.basename(word_path)))
        except Exception as e:
            return str(e)

@app.route('/advanced_ocr_page')
def advanced_ocr_page():
    return render_template('advanced_ocr.html')

@app.route('/advanced_ocr', methods=['POST'])
def advanced_ocr():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_path = os.path.join(OUTPUT_FOLDER, 'extracted_text.txt')
        file.save(input_path)
        try:
            process_image(input_path, output_path)
            with open(output_path, 'r', encoding='utf-8') as file:
                extracted_text = file.read()
            return render_template('advanced_ocr.html', extracted_text=extracted_text, text_url=url_for('download_file', filename='extracted_text.txt'))
        except Exception as e:
            return str(e)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
