import os
import logging
from flask import Flask, request, jsonify, render_template
from PyPDF2 import PdfReader
from werkzeug.utils import secure_filename

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'  # Use /tmp for Vercel
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def find_in_pdf(pdf_path, student_numbers):
    """
    Search for multiple student numbers in a PDF file and return their page numbers.
    """
    reader = PdfReader(pdf_path)
    results = {number: [] for number in student_numbers}
    
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text = page.extract_text()
        
        for number in student_numbers:
            if str(number) in text:
                # Add 1 to page_num because PDF pages are 0-indexed
                results[number].append(page_num + 1)
                logger.debug(f"Found student {number} on page {page_num + 1}")
    
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    student_numbers = request.form.get('student_numbers', '').strip()
    
    if not student_numbers:
        return jsonify({'error': 'No student numbers provided'}), 400
    
    # Split and clean student numbers
    student_numbers = [num.strip() for num in student_numbers.split(',') if num.strip()]
    
    # Validate number of student numbers
    if len(student_numbers) > 100:
        return jsonify({'error': 'Maximum 100 student numbers allowed'}), 400
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension != '.pdf':
        return jsonify({'error': 'Only PDF documents are supported'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Log file information
        logger.debug(f"Processing PDF file: {filename}")
        
        results = find_in_pdf(filepath, student_numbers)
        
        # Clean up the uploaded file
        os.remove(filepath)
        
        # Format results for display
        formatted_results = []
        for student_number, pages in results.items():
            formatted_results.append({
                'student_number': student_number,
                'pages': sorted(pages),
                'found': len(pages) > 0
            })
        
        return jsonify({
            'success': True,
            'results': formatted_results
        })
    
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

# For local development
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
