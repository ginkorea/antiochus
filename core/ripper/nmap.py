import re
import pandas as pd
from core.ripper.base import BaseRipper


class NmapRipper(BaseRipper):

    def __init__(self):
        super().__init__()
        self.type = "Nmap" # Specify the type of ripper
        self.needs_cleaning = True

    def rip(self, text):
        """Extracts Nmap commands and their context from the provided text."""
        # Regex to capture the full Nmap command and the target (IP address or range)
        pattern = r"(nmap\s+[\S\s]+?\s+(\d+\.\d+\.\d+\.\d+(?:/\d+)?)(?:[\S\s]+?)?)"
        commands = re.findall(pattern, text)
        command_context = []

        for command, target in commands:
            # Find context: capture surrounding lines (you can tweak this as needed)
            start_idx = max(0, text.find(command) - 100)
            end_idx = min(len(text), text.find(command) + len(command) + 100)
            context = text[start_idx:end_idx].replace("\n", " ").strip()
            command_context.append((command, context, target))

        # Convert extracted commands into a DataFrame
        self.ripped = pd.DataFrame(command_context, columns=["Command", "Context", "Target"])

    def clean(self):
        """Cleans the ripped Nmap commands by separating the command from the description."""
        if self.ripped is None:
            raise ValueError("No knowledge to clean. Run rip first.")

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
            command_parts = command.split()

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

        # Apply the cleaning logic across the DataFrame
        self.ripped = self.ripped.apply(clean_row, axis=1)


