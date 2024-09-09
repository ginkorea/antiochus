from core.book import Book
import os

class Task:

    def __init__(self):
        pass

    @staticmethod
    def process_file(antiochus, file_path, verbose):
        """Process a single book file and extract commands to CSV using the Antiochus class."""
        # Step 1: Create an Antiochus object
        antiochus.pick_up_book_and_read(file_path)
        if verbose:
            print(f"Extracted text from {file_path}")
            print(f"Text: {antiochus.book.text[:500]}...")  # Print the first 500 characters for preview
        antiochus.rip()
        if verbose:
            print(f"Ripped commands: {antiochus.ripper.ripped}")

    @staticmethod
    def process_directory(antiochus, directory, verbose):
        """Process all PDF files in a directory using the Antiochus class."""
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            # output_file_path = os.path.splitext(file_path)[0] + "_commands.csv"
            Task.process_file(antiochus, file_path, verbose)