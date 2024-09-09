from core.book import Book
import os

class Task:

    def __init__(self):
        pass

    @staticmethod
    def process_file(antiochus, file_path, output_file, verbose):
        """Process a single book file and extract commands to CSV using the Antiochus class."""
        # Step 1: Create an Antiochus object
        antiochus.book = Book(file_path)
        if verbose:
            print(f"Processing {antiochus.book.file_path}")
        antiochus.book.get_book_type()

        # Step 2: Use Antiochus to read the text from the PDF
        antiochus.read()

        if verbose:
            print(f"Extracted text from {file_path}")
            print(f"Text: {antiochus.book.text[:500]}...")  # Print the first 500 characters for preview

        # Step 3: Use Antiochus to rip the commands from the text
        antiochus.rip_commands()

        # Step 4: Clean the ripped commands
        antiochus.clean_knowledge()

    @staticmethod
    def process_directory(antiochus, directory, verbose):
        """Process all PDF files in a directory using the Antiochus class."""
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            output_file_path = os.path.splitext(file_path)[0] + "_commands.csv"
            Task.process_file(antiochus, file_path, output_file_path, verbose)