from flask import Flask, render_template, request, send_file
from pdf2docx import Converter
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the uploaded PDF file from the request
        pdf_file = request.files['pdf_file']

        # Get the output file name from the input box
        output_file_name = request.form['output_file_name']

        # Save the uploaded PDF file to a temporary location
        pdf_path = f'tmp/{pdf_file.filename}'
        pdf_file.save(pdf_path)

        # Convert PDF to DOCX
        docx_file = convert_pdf_to_docx(pdf_path, output_file_name)

        # Clean up the temporary PDF file
        os.remove(pdf_path)

        # Send the converted file as a download
        return send_file(docx_file, as_attachment=True)

    # Render the home page
    return render_template('home.html')

def convert_pdf_to_docx(pdf_path, output_file_name):
    # Create a temporary file with a .docx extension
    docx_file = f'tmp/{output_file_name}.docx'

    # Convert the PDF file to DOCX
    cv = Converter(pdf_path)
    cv.convert(docx_file, start=0, end=None)
    cv.close()

    return docx_file

if __name__ == '__main__':
    app.run(debug=True)