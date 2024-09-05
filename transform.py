import json
import csv
from fractions import Fraction

# Read the JSON file
with open('final.json', 'r') as json_file:
    data = json.load(json_file)

# Prepare the CSV file
csv_file = open('output.csv', 'w', newline='')
writer = csv.writer(csv_file)

# Write the headers
headers = ['index', 'input', 'name', 'qty', 'range_end', 'unit', 'comment']
writer.writerow(headers)

# Start index
index = 179207

# Transform the JSON data and write to CSV
for row in data:
    try:
        answer_str = row['Answer']
        context_str = row['Context']
        answer = json.loads(answer_str)
        for item in answer:
            ingredient = item['ingredient']
            quantity = item['quantity'] if item['quantity'] != 'None' else ''

            unit = item['unit'] if item['unit'] != 'None' else ''

            row = [index, context_str, ingredient, float(Fraction(quantity)), 0.0, unit, '']
            writer.writerow(row)

            index += 1
    except:
        print(row)
        continue

# Close the CSV file
csv_file.close()