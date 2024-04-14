import os
import sys
import argparse
import json
import datetime
import logging
import math

LOG_FORMAT = "[%(asctime)s] [%(levelname)s]: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
VALID_FIELDS = ["bannerUrl", "category", "description", "developer", "frontBoxArt", "iconUrl", "id", "intro", "isDemo", "key", "languages", "name", "nsuId",
                "numberOfPlayers", "publisher", "rank", "rating", "ratingContent", "region", "regions", "releaseDate", "rightsId", "screenshots", "size", "version"]

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


def validate_fields(fields):
    if fields and not all(field in VALID_FIELDS for field in fields):
        invalid_fields = ', '.join(set(fields) - set(VALID_FIELDS))
        logging.error(f"Invalid field [{invalid_fields}]. Valid fields are {', '.join(VALID_FIELDS)}")
        sys.exit(1)


def read_json_file(file_path):
    if not os.path.exists(file_path):
        logging.error(f"File {file_path} does not exist")
        sys.exit(1)

    try:
        with open(file_path) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"{file_path} is not a valid JSON file. {e}")
        sys.exit(1)


def reduce_data_size(data, fields):
    new_data = {}
    previous = 0
    for count, (title_id, title_data) in enumerate(data.items(), start=1):
        if title_data.get("name"):
            new_data[title_id] = {field: title_data[field] for field in (fields or title_data) if field in title_data}

        progress = int(math.floor(count/len(data)*100))
        if progress != previous and progress % 5 == 0:
            logging.info(f"Progress: {progress}% - {count}/{len(data)}")
            previous = progress
    return new_data


def write_to_file(output, new_data):
    try:
        with open(output, "w") as f:
            json.dump(new_data, f, separators=(",", ":"))
    except Exception as e:
        logging.error(f"Error writing to {output}. {e}")
        sys.exit(1)


if __name__ == "__main__":
    logging.info("Initialising tiny.py")
    start_time = datetime.datetime.now()
    parser = argparse.ArgumentParser(description="Process some JSON.")
    parser.add_argument("input_file", help="The JSON file to process")
    parser.add_argument("-o", "--output_file", help="The file to output to. Defaults to the input file if not provided")
    parser.add_argument("-f", "--fields", nargs="*", help="List of fields to keep in the output, defaults to all fields")
    args = parser.parse_args()

    title_db = args.input_file
    output = args.input_file if args.output_file is None else args.output_file
    fields = args.fields

    validate_fields(fields)

    logging.info(f"Starting tiny.py with input file: {title_db}, output file: {output}, fields: {fields if fields else 'All fields'}")
    logging.info(f"Reading from {title_db}")
    data = read_json_file(title_db)

    start_size = os.path.getsize(title_db)
    logging.info(f"Read {len(data)} titles from {title_db} ({start_size/1024/1024:.1f} MB)")

    new_data = reduce_data_size(data, fields)

    logging.info(f"Writing {len(new_data)} titles to {output}")
    write_to_file(output, new_data)

    logging.info(f"Task completed in {(datetime.datetime.now() - start_time).total_seconds()} seconds and reduced the file size from {
                 (start_size/1024/1024):.1f} MB to {(os.path.getsize(output)/1024/1024):.1f} MB. Exiting.")
