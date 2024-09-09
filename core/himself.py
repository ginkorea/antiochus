import pandas as pd
from core.utils import Task
from core.ripper.nmap import NmapRipper
from core.book import Book


class Antiochus:
    """Handles reading, ripping, cleaning, and writing text with stored knowledge."""

    def __init__(self, knowledge=None, book=None):
        """
        Initializes the Antiochus class with optional existing knowledge.
        :param knowledge: Optional existing DataFrame to store commands and contexts.
        """
        if knowledge is not None:
            knowledge = pd.read_csv(knowledge)
        self.knowledge = knowledge
        self.book = book  # Book object to store the text
        self.tasks = Task()
        self.ripper = None

    def pick_up_book_and_read(self, file_path):
        """Picks up a book and initializes the Book object."""
        self.book = Book(file_path)
        self.book.get_book_type()
        print(f"Picked up {self.book.file_path_or_url}")
        self.read()

    def read(self):
        """Reads the book and extracts text based on the book type."""
        self.book.read()

    def rip(self, ripper_type='nmap'):
        """Rips commands from the text using the specified ripper type."""
        self.select_ripper(ripper_type)
        self.rip_commands()

    def select_ripper(self, ripper_type='nmap'):
        """Selects the ripper type to use for extracting commands."""
        if ripper_type == 'nmap':
            self.ripper = NmapRipper()
        else:
            raise ValueError(f"Unsupported ripper type: {ripper_type}")

    def rip_commands(self):
        """Rips commands from the text using the specified ripper type."""
        if self.ripper is None:
            raise ValueError("No ripper selected. Run select_ripper() first.")
        self.ripper.rip(self.book.text)
        if self.ripper.needs_cleaning:
            self.ripper.clean()
        if self.knowledge is not None:
            self.knowledge = pd.concat([self.knowledge, self.ripper.ripped], ignore_index=True)
        else:
            self.knowledge = self.ripper.ripped

    def write_knowledge(self, output_file='antiochus_knowledge.csv'):
        """Writes the cleaned knowledge to a CSV file."""
        if self.knowledge is not None:
            self.knowledge.to_csv(output_file, index=False)
            print(f"Knowledge saved to {output_file}")
        else:
            raise ValueError("No knowledge to write. Run rip_commands and clean_commands first.")


