import asyncio
from argparse import ArgumentParser
from aiopath import AsyncPath
from logger import logging
from file_ops import read_folder


def parse_args():
    """parses arguments that come with app start

    Returns:
        tuple[AsyncPath]: source and output fonders as AsyncPath objects
    """
    try:
        parser = ArgumentParser()
        parser.add_argument("-s", "--source", help="Source folder", default="pictures")
        parser.add_argument("-o", "--output", help="Output folder", default="sorted_copies")

        args = parser.parse_args()

        if args.source:
            source_path = AsyncPath(args.source)
            output_path = AsyncPath(args.output)
            return source_path, output_path
        else:
            logging.error("Provide source directory")
            return None
    except Exception as e:
        logging.error(f"Parsing error: {e}")

def main():
    try:
        source, dest = parse_args()
        asyncio.run(read_folder(source, dest))
    except Exception as e:
        logging.error(f"Some error occured: {e}")

if __name__ == "__main__":
    main()