# PDF Student Number Search

A web application that allows users to search for student numbers within PDF documents and returns the page numbers where these numbers appear.

## Features

- Upload and process PDF documents
- Search for multiple student numbers simultaneously (up to 100)
- Get accurate page numbers for each student number
- Copy all found page numbers with a single click
- Clean and intuitive web interface

## Requirements

- Python 3.7+
- Flask
- PyPDF2
- Werkzeug

## Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd pdf-student-number-search
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:
   ```bash
   python main.py
   ```

2. Open your web browser and navigate to `http://localhost:5009`

3. Upload a PDF document and enter student numbers (comma-separated)

4. Click "Search" to find the page numbers where the student numbers appear

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
