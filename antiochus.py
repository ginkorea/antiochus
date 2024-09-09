import argparse
from core.himself import Antiochus  # Importing the new Antiochus class


def main():
    # Argument parser
    parser = argparse.ArgumentParser(
        description="Extract commands from a book or directory of books using Nmap and other commands.")
    parser.add_argument('--file', type=str, help="Path to a single PDF file to rip.")
    parser.add_argument('--dir', type=str, help="Directory containing multiple PDF files to rip.")
    parser.add_argument('--output', type=str, default="knowledge.csv",
                        help="Output CSV file name (default: commands.csv).")
    parser.add_argument('--verbose', action='store_true', help="Enable verbose output.")
    parser.add_argument('--knowledge', type=str, help="Existing knowledge CSV file to append to.")

    args = parser.parse_args()

    # Ensure either --file or --dir is provided
    if not args.file and not args.dir:
        parser.error("You must specify either --file or --dir")

    if args.knowledge:
        # Load existing knowledge from a CSV file
        knowledge = args.knowledge
    else:
        knowledge = None

    antiochus = Antiochus(knowledge=knowledge)

    if args.file:
        # Process a single file
        antiochus.tasks.process_file(antiochus, args.file, args.verbose)

    if args.dir:
        # Process a directory of PDF files
        antiochus.tasks.process_directory(antiochus, args.dir, args.verbose)

    # Write the final knowledge to a CSV file
    antiochus.write_knowledge(args.output)


if __name__ == "__main__":
    main()
