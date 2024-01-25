# main.py

import yaml
import json
from jsonschema import validate, ValidationError
from datetime import date, datetime
import io
import os

from schema import task_list_schema

# Function to convert date objects to strings recursively
def convert_dates_to_strings(obj):
    if isinstance(obj, dict):
        return {key: convert_dates_to_strings(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_dates_to_strings(item) for item in obj]
    elif isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    else:
        return obj

# Function to parse date strings into datetime.date objects or strings
def parse_dates(obj):
    if isinstance(obj, dict):
        return {key: parse_dates(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [parse_dates(item) for item in obj]
    elif isinstance(obj, (date, datetime)):
        return obj.strftime('%Y-%m-%d')
    elif isinstance(obj, str):
        return obj
    else:
        return obj

def load_tasks_from_yaml(yaml_string):
    loaded_tasks = yaml.safe_load(yaml_string)
    return parse_dates(loaded_tasks)

def convert_yaml_to_json(yaml_string, folder_path):
    loaded_data = yaml.safe_load(yaml_string)
    # Convert date objects to strings before JSON serialization
    loaded_data = convert_dates_to_strings(loaded_data)
    json_data = json.dumps(loaded_data, indent=2)
    
    # Create a folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Determine the next available file number
    file_number = 1
    while os.path.exists(os.path.join(folder_path, f'tasks_{file_number}.json')):
        file_number += 1

    # Save to a new JSON file with a numbered filename
    json_filename = os.path.join(folder_path, f'tasks_{file_number}.json')
    with io.open(json_filename, 'w', encoding='utf8') as json_file:
        json_file.write(json_data)

    return json_filename

def validate_tasks(tasks):
    try:
        validate(instance=tasks, schema=task_list_schema)
        print("Validation successful.")
    except ValidationError as e:
        print(f"Validation error: {e}")

# Example YAML DSL with additional features
yaml_dsl = """
tasks:
  - title: Buy groceries
    priority: high
    completed: false
    due_date: 2022-02-28
    tags:
      - shopping
  - title: Finish report
    priority: medium
    completed: true
    due_date: 2022-03-10
    tags:
      - work
    subtasks:
      - title: Research
        completed: true
      - title: Write
        completed: true
      - title: Edit
        completed: false
"""

# Load tasks from YAML DSL
tasks = load_tasks_from_yaml(yaml_dsl)

# Validate tasks against the schema
validate_tasks(tasks)

# Modify tasks (e.g., add a new task with subtasks)
tasks['tasks'].append({
    'title': 'Plan vacation',
    'priority': 'medium',
    'completed': False,
    'due_date': date(2022, 4, 15),
    'tags': ['travel'],
    'subtasks': [
        {'title': 'Choose destination', 'completed': False},
        {'title': 'Book flights', 'completed': False},
        {'title': 'Pack bags', 'completed': False}
    ]
})

# Convert YAML to JSON and save to a new file
json_filename = convert_yaml_to_json(yaml_dsl, 'modified_json_tasks')

print("Original YAML DSL:")
print(yaml_dsl)

print(f"\nConverted YAML to JSON saved to {json_filename}")
