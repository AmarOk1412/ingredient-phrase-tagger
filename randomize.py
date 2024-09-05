import csv
import random

# Read the input CSV file
with open('new.csv', 'r') as file:
    reader = csv.DictReader(file)
    lines = list(reader)

# Randomize the lines
random.shuffle(lines)

for i, line in enumerate(lines):
    line['index'] = i

# Write the sorted lines to a new CSV file
with open('new2.csv', 'w', newline='') as file:
    fieldnames = ['index', 'input', 'name', 'qty', 'range_end', 'unit', 'comment']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(lines)