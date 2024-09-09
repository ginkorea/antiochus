import re
import pandas as pd
from core.utils import Task


class Antiochus:
    """Handles reading, ripping, cleaning, and writing text with stored knowledge."""

    def __init__(self, knowledge=None, book=None):
        """
        Initializes the Antiochus class with optional existing knowledge.
        :param knowledge: Optional existing DataFrame to store commands and contexts.
        """
        self.knowledge = knowledge
        self.book = book # Book object to store the text
        self.tasks = Task()

    def read(self):
        """Reads the book and extracts text based on the book type."""
        self.book.read()

    def rip_commands(self):
        """Extracts Nmap commands and their context from the text using regex."""
        # Regex to capture the full Nmap command and the target (IP address or range)
        pattern = r"(nmap\s+[\S\s]+?\s+(\d+\.\d+\.\d+\.\d+(?:/\d+)?)(?:[\S\s]+?)?)"
        commands = re.findall(pattern, self.book.text)
        command_context = []

        for command, target in commands:
            # Find context: capture surrounding lines (you can tweak this as needed)
            start_idx = max(0, self.book.text.find(command) - 100)
            end_idx = min(len(self.book.text), self.book.text.find(command) + len(command) + 100)
            context = self.book.text[start_idx:end_idx].replace("\n", " ").strip()
            command_context.append((command, context, target))

        # Convert extracted commands into a DataFrame
        gained_knowledge = pd.DataFrame(command_context, columns=["Command", "Context", "Target"])

        # Merge gained knowledge with existing knowledge
        if self.knowledge is not None:
            self.knowledge = pd.concat([self.knowledge, gained_knowledge])
        else:
            self.knowledge = gained_knowledge


    def clean_knowledge(self):
        """Cleans the ripped commands by separating the Nmap command from the description."""
        if self.knowledge is None:
            raise ValueError("No knowledge to clean. Run rip_commands first.")

        # List of flags that require something to follow them, including 'nmap' which should always be included
        follow_on_flags = [
            'nmap', '-oX', '-oN', '-oG', '-oA', '--append-output',  # Output files
            '-iL', '--excludefile',  # Input files (target list)
            '--script', '--script-args', '--script-help',  # Scripts
            '--version-intensity', '--osscan-limit', '--osscan-guess',  # Version and OS detection
            '-PS', '-PA', '-PU', '-PR', '-PP', '-PM',  # Host discovery
            '-D', '-S', '--proxies', '--data-length', '--source-port', '--ip-options', '--ttl',
            # Firewall/IDS evasion
            '--min-hostgroup', '--max-hostgroup', '--min-parallelism', '--max-parallelism', '--scan-delay',
            '--max-scan-delay', '--host-timeout',  # Timing and performance
            '-p', '-g', '--min-rate', '--max-rate', '--resume', '-f'  # Other options
        ]

        def clean_row(row):
            command = row['Command']
            command_parts = command.split()  # Split the command by spaces

            cleaned_command = []
            description_start = False

            for idx, part in enumerate(command_parts):
                # If part is a number, starts with '-', or is part of the follow-on flags, it's part of the command
                if (part.isdigit() or part.startswith('-') or part in follow_on_flags or
                        (idx > 0 and command_parts[idx - 1] in follow_on_flags)):
                    cleaned_command.append(part)
                else:
                    # Once we find something that doesn't match, we assume it's part of the description
                    description_start = idx
                    break

            # Create the cleaned command and description
            cleaned_command = " ".join(cleaned_command)
            description = " ".join(command_parts[description_start:]) if description_start else ""

            return pd.Series({
                'Cleaned_Command': cleaned_command,
                'Description': description,
                'Target': row['Target'],
                'Context': row['Context']
            })

        # Apply the clean_row function to each row in the DataFrame
        self.knowledge = self.knowledge.apply(clean_row, axis=1)

    def write_knowledge(self, output_file='antiochus_knowledge.csv'):
        """Writes the cleaned knowledge to a CSV file."""
        if self.knowledge is not None:
            self.knowledge.to_csv(output_file, index=False)
            print(f"Knowledge saved to {output_file}")
        else:
            raise ValueError("No knowledge to write. Run rip_commands and clean_commands first.")

# Example usage:
# antiochus = Antiochus()
# text = antiochus.read_pdf("path_to_pdf.pdf")
# antiochus.rip_commands(text)
# antiochus.clean_commands()
# antiochus.write_to_csv("cleaned_nmap_commands.csv")
