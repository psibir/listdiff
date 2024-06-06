import csv
import argparse
from collections import defaultdict

def find_unique_upcs(csv_file, column_indices, has_header=True):
    upcs = defaultdict(set)
    column_names = {}

    try:
        with open(csv_file, 'r', newline='') as file:
            reader = csv.reader(file)
            
            if has_header:
                column_names = {index: name for index, name in enumerate(next(reader))}
            
            for row in reader:
                for index, upc_set in upcs.items():
                    upc_set.add(row[index])
    except FileNotFoundError as e:
        print("File not found:", csv_file)
        return {}, {}
    except Exception as e:
        print("Error:", e)
        return {}, {}

    unique_upcs = set()
    for index, upc_set in upcs.items():
        if index in column_indices:
            other_upc_sets = [upcs[i] for i in column_indices if i != index]
            unique_upcs |= upc_set.difference(*other_upc_sets)

    return unique_upcs, column_names

def write_to_csv(upcs, column_names, column_indices, output_file):
    try:
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["UPC", "Column(s)"])
            for upc in upcs:
                columns = ", ".join(column_names[index] for index in column_indices)
                writer.writerow([upc, columns])
        print("Unique UPCs written to:", output_file)
    except Exception as e:
        print("Error writing to CSV:", e)

def main():
    parser = argparse.ArgumentParser(description="Find unique UPCs between specified columns in a CSV file")
    parser.add_argument("input_csv", help="Path to the input CSV file")
    parser.add_argument("output_csv", help="Path to the output CSV file")
    parser.add_argument("column_indices", nargs='+', type=int, help="Indices of the columns to check (0-based)")
    parser.add_argument("--has_header", action="store_true", help="Specify if the CSV has a header")

    args = parser.parse_args()

    unique_upcs, column_names = find_unique_upcs(args.input_csv, args.column_indices, args.has_header)
    write_to_csv(unique_upcs, column_names, args.column_indices, args.output_csv)

if __name__ == "__main__":
    main()
