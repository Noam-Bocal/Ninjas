import json
import os
import sqlite3

# Directory path containing the JSON files
directory = R'C:\Users\test0\OneDrive\שולחן העבודה\rephael ninjas\cti-master\enterprise-attack\attack-pattern'

# Path to the SQLite database file
database_file = R'C:\Users\test0\OneDrive\שולחן העבודה\rephael ninjas\sql database handle\attacks_data.db'

# Connect to the SQLite database
conn = sqlite3.connect(database_file)
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS attacks (
                    Name TEXT,
                    Description TEXT,
                    Id TEXT PRIMARY KEY,
                    x_mitre_platforms TEXT,
                    x_mitre_detection TEXT,
                    phase_name TEXT
                  )''')

# Iterate through JSON files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            objects = data.get('objects', [])

            for obj in objects:
                if obj.get('type') == 'attack-pattern':
                    attack_name = obj.get('name', 'NA')
                    attack_description = obj.get('description', 'NA')
                    attack_id = obj.get('id', 'NA')
                    platforms = ', '.join(obj.get('x_mitre_platforms', ['NA']))
                    detection = obj.get('x_mitre_detection', 'NA')

                    kill_chain_phases = obj.get('kill_chain_phases', [])
                    phase_names = [phase.get('phase_name', 'NA') for phase in kill_chain_phases]
                    phases = ', '.join(phase_names)

                    # Insert values into the database
                    cursor.execute('''INSERT INTO attacks (
                                        Name, Description, Id, x_mitre_platforms, x_mitre_detection, phase_name
                                      )
                                      VALUES (?, ?, ?, ?, ?, ?)''',
                                   (attack_name, attack_description, attack_id, platforms, detection, phases))

# Commit changes and close the database connection
conn.commit()
conn.close()
