import csv

def increment_prefix(prefix):
    try:
        last_char = prefix[-1]
        if last_char == 'Z':
            return increment_prefix(prefix[:-1]) + 'A'
        else:
            return prefix[:-1] + chr(ord(last_char) + 1)
    except:
        return None

def increment_mixed_series(id_start:str, batch_size:int, keep_first:bool=False) -> list:
    series = []
    id = id_start
    for _ in range(batch_size):
        prefix = ""
        numeric = ""
        for char in id:
            if char.isalpha():
                prefix += char
            elif char.isdigit():
                numeric += char
            else:
                break
        if numeric:
            max_numeric_val = int('9' * len(numeric))
            current_numeric_val = int(numeric)
            if current_numeric_val < max_numeric_val:
                new_prefix = prefix
                new_numeric = str(current_numeric_val + 1).zfill(len(numeric))
            else:
                new_prefix = increment_prefix(prefix)
                if new_prefix is not None:
                    new_numeric = '0' * len(numeric)
                else:
                    print("End of possible mixed series reached!")
                    break
            id = new_prefix + new_numeric
        else:
            id = increment_prefix(id)
            if id is not None:
                series.append(id)
            else:
                print("End of possible mixed series reached!")
                break
        series.append(id)

    if keep_first:
        series.insert(0, id_start)

    return series


print(increment_mixed_series("ZZ9995", 5, False))


def generate_incremental_series(starting_number, batch_size):
    series = []
    for i in range(starting_number, starting_number + batch_size):
        series.append(i)
    return series

def split_mixed_string(input_string:str) -> (str, str):
    prefix = ""
    numeric_part = ""

    for char in input_string:
        if char.isalpha():
            prefix += char
        elif char.isdigit():
            numeric_part += char
        else:
            break
    return prefix, numeric_part

def calculate_max_number(length):
    return 10**length - 1



# print(increment_prefix("AA"))


def generate_series_with_chars(starting_number, batch_size):
    series = []
    for _ in range(batch_size):
        current = list(starting_number)
        series.append("".join(current))
        
        i = len(current) - 1
        while i >= 0:
            if current[i] == "9":
                current[i] = "A"
                break
            elif current[i] == "Z":
                current[i] = "0"
                i -= 1
            else:
                current[i] = chr(ord(current[i]) + 1)
                break
        starting_number = "".join(current)
    return series

# start = "012345"
# num_series = 10000
# result = generate_series(starting_number, batch_size)

def save_to_csv(series, filename):
    with open(filename, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows([[s] for s in series])

# csv_filename = "series_output.csv"
# save_to_csv(result, csv_filename)
# print(f"Series saved to {csv_filename}")


def search_in_csv(csv_filename, search_strings):
    found_strings = []
    
    with open(csv_filename, "r", newline="") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            series = row[0]
            for search_string in search_strings:
                if search_string in series:
                    found_strings.append(search_string)
    
    return found_strings

# csv_filename = "series_output.csv"
# search_strings = ["01234A", "ABCDEF", "567890"]
# found_strings = search_in_csv(csv_filename, search_strings)

# for search_string in search_strings:
#     if search_string in found_strings:
#         print(f""{search_string}" found in the CSV file.")
#     else:
#         print(f""{search_string}" not found in the CSV file.")


def copy_lines_and_save(source_csv_filename, dest_csv_filename, start_line, num_lines):
    lines_to_copy = []
    
    with open(source_csv_filename, "r", newline="") as csvfile:
        csvreader = csv.reader(csvfile)
        lines = list(csvreader)
        
        start_index = None
        for index, row in enumerate(lines):
            if start_line in row[0]:
                start_index = index
                break
        
        if start_index is not None:
            lines_to_copy = lines[start_index:start_index + num_lines]
    
    if lines_to_copy:
        with open(dest_csv_filename, "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(lines_to_copy)
        print(f"{num_lines} lines copied and saved to {dest_csv_filename}")
    else:
        print("Start line not found in the source CSV.")

# source_csv_filename = "series_output.csv"
# dest_csv_filename = "batch_output.csv"
# start_line = "012345"
# num_lines = 5000
# copy_lines_and_save(source_csv_filename, dest_csv_filename, start_line, num_lines)

import sqlite3

def create_table_from_csv(database_filename, csv_filename, table_name="new_table", header_name=["Series"]):
    conn = sqlite3.connect(database_filename)
    cursor = conn.cursor()

    with open(csv_filename, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        
        column_names = ', '.join(header_name)
        placeholders = ', '.join(['?'] * len(header_name))
        
        create_table_query = f"CREATE TABLE {table_name} ({column_names})"
        cursor.execute(create_table_query)
        
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        for row in csvreader:
            cursor.execute(insert_query, row)
    
    conn.commit()
    conn.close()
    print(f"Table '{table_name}' created and data inserted into the database.")

# csv_filename = "batch_output.csv"
# database_filename = "my_database.db"

# create_table_from_csv(database_filename, csv_filename)

