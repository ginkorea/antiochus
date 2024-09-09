import PyPDF2

import docx
from ebooklib import epub
from bs4 import BeautifulSoup

class Book:
    """Represents the book with file path and extracted text."""

    def __init__(self, file_path):
        self.file_path = file_path
        self.text = None
        self.type = self.get_book_type()

    def get_book_type(self):
        """Extracts the book type based on the file extension."""
        try:
            self.type = self.file_path.split('.')[-1].lower()  # Convert to lowercase for consistency
        except IndexError:
            self.type = None
        return self.type

    def read(self):
        """Reads the book and extracts text based on the book type."""
        if self.type == 'pdf':
            self.text = self.read_pdf()
        elif self.type == 'txt':
            self.text = self.read_txt()
        elif self.type == 'epub':
            self.text = self.read_epub()
        elif self.type == 'docx':
            self.text = self.read_docx()
        else:
            raise ValueError(f"Unsupported file type: {self.type}")
        return self.text

    def read_pdf(self):
        """Reads text from a PDF file."""
        text = ""
        try:
            with open(self.file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() or ""  # Handle cases where text extraction may fail
        except Exception as e:
            raise ValueError(f"Error reading PDF: {e}")
        return text

    def read_txt(self):
        """Reads text from a plain text file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise ValueError(f"Error reading TXT: {e}")

    def read_epub(self):
        """Reads text from an EPUB file."""
        try:
            book = epub.read_epub(self.file_path)
            text = ""
            for item in book.get_items():
                if item.get_type() == epub.EpubItem.DOCUMENT:
                    # Use BeautifulSoup to extract text content from HTML
                    soup = BeautifulSoup(item.get_body_content(), 'html.parser')
                    text += soup.get_text()
        except Exception as e:
            raise ValueError(f"Error reading EPUB: {e}")
        return text

    def read_docx(self):
        """Reads text from a DOCX file."""
        try:
            doc = docx.Document(self.file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            raise ValueError(f"Error reading DOCX: {e}")
        return text
