import csv
import argparse
from collections import defaultdict

def find_unique_upcs(csv_file, column1_index, column2_index, has_header=True):
    upcs1 = set()
    upcs2 = set()

    try:
        with open(csv_file, 'r', newline='') as file:
            reader = csv.reader(file)
            
            if has_header:
                next(reader)  # Skip header row
            
            for row in reader:
                if len(row) > max(column1_index, column2_index):
                    upcs1.add(row[column1_index])
                    upcs2.add(row[column2_index])
                else:
                    print("Skipping row with insufficient columns:", row)
    except FileNotFoundError:
        print("File not found:", csv_file)
    except Exception as e:
        print("Error:", e)

    unique_upcs = upcs1 ^ upcs2  # Use set symmetric difference directly
    return unique_upcs

def write_to_csv(upcs, output_file):
    try:
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows([[upc] for upc in upcs])  # Use writerows for better efficiency
        print("Unique UPCs written to:", output_file)
    except Exception as e:
        print("Error writing to CSV:", e)

def main():
    parser = argparse.ArgumentParser(description="Find unique UPCs between two columns in a CSV file")
    parser.add_argument("input_csv", help="Path to the input CSV file")
    parser.add_argument("output_csv", help="Path to the output CSV file")
    parser.add_argument("--column1_index", type=int, default=0, help="Index of the first column (0-based)")
    parser.add_argument("--column2_index", type=int, default=1, help="Index of the second column (0-based)")
    parser.add_argument("--has_header", action="store_true", help="Specify if the CSV has a header")

    args = parser.parse_args()

    unique_upcs = find_unique_upcs(args.input_csv, args.column1_index, args.column2_index, args.has_header)
    write_to_csv(unique_upcs, args.output_csv)

if __name__ == "__main__":
    main()
