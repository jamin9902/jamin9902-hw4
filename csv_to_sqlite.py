#!/usr/bin/env python3

import csv
import os
import sqlite3
import sys

def csv_to_sqlite(db_name, csv_file):
    # Connect to SQLite database (create it if it doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Read CSV file
    with open(csv_file, 'r') as f:
        csv_reader = csv.reader(f)
        
        # Get headers from first row
        headers = next(csv_reader)
        
        # Get table name from CSV filename (without extension)
        table_name = os.path.splitext(os.path.basename(csv_file))[0]
        
        # Create table using headers as column names
        # Assuming all columns are TEXT for simplicity
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{header} TEXT' for header in headers])})"
        cursor.execute(create_table_sql)
        
        # Insert data
        placeholders = ','.join(['?' for _ in headers])
        insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
        
        # Insert all rows
        cursor.executemany(insert_sql, csv_reader)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()

def main():
    if len(sys.argv) != 3:
        print("Usage: python csv_to_sqlite.py <database_name> <csv_file>")
        sys.exit(1)
        
    db_name = sys.argv[1]
    csv_file = sys.argv[2]
    
    try:
        csv_to_sqlite(db_name, csv_file)
        print(f"Successfully converted {csv_file} to SQLite database {db_name}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()