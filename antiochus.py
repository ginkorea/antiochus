import argparse
import pandas as pd
from core.himself import Antiochus  # Importing the new Antiochus class
from core.forget import forget  # Importing the forget function


def main():
    # Argument parser
    parser = argparse.ArgumentParser(
        description="Extract commands from a book or directory of books using Nmap and other commands.")
    parser.add_argument('--file', type=str, help="Path to a single file to rip.")
    parser.add_argument('--dir', type=str, help="Directory containing multiple files to rip.")
    parser.add_argument('--output', type=str, default="knowledge.csv",
                        help="Output CSV file name (default: knowledge.csv).")
    parser.add_argument('--verbose', action='store_true', help="Enable verbose output.")
    parser.add_argument('--knowledge', type=str, help="Existing knowledge CSV file to append to.")
    parser.add_argument('--forget', action='store_true', help="Clean the knowledge by forgetting nulls and duplicates.")

    args = parser.parse_args()

    # Load existing knowledge from a CSV file, if provided
    if args.knowledge:
        if args.forget:
            knowledge = pd.read_csv(args.knowledge)
            # Clean the knowledge file
            forget(knowledge)
            knowledge.to_csv(args.knowledge, index=False)  # Save the cleaned knowledge
            exit(0)
        else:
            knowledge = args.knowledge
    else:
        knowledge = None

    # Create the Antiochus instance
    antiochus = Antiochus(knowledge=knowledge)

    if args.file:
        # Process a single file
        antiochus.tasks.process_file(antiochus, args.file, args.verbose)

    if args.dir:
        # Process a directory of files
        antiochus.tasks.process_directory(antiochus, args.dir, args.verbose)

    # Write the final knowledge to a CSV file
    antiochus.write_knowledge(args.output)


if __name__ == "__main__":
    main()
