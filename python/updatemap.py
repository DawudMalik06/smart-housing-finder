'''
Run this file after running python/pipeline.py to update the sheffield.json file
'''
import json
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CSV_PATH = BASE_DIR / "final_output" / "LivabilityScores_with_Greenspace.csv"
JSON_PATH = BASE_DIR / "dashboard" / "sheffield.json"
CONFIG_PATH = Path(__file__).parent / "config.json"

def update_sheffield_json():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    json_to_csv_map = config['json_to_csv_map']
    csv_df = pd.read_csv(CSV_PATH)
    csv_lookup = csv_df.set_index('Neighborhood').to_dict('index')
    
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        map_data = json.load(f)
    
    updated_count = 0
    for feature in map_data['features']:
        wd13_name = feature['properties'].get('WD13NM')
        csv_target_name = json_to_csv_map.get(wd13_name)
        
        if csv_target_name and csv_target_name in csv_lookup:
            row_data = csv_lookup[csv_target_name]
            feature['properties']['LivabilityScore'] = row_data['LivabilityScore']
            feature['properties']['GreenSpace'] = row_data['GreenSpace']
            feature['properties']['Cost'] = row_data['Cost']
            updated_count += 1
        else:
            print(f"Could not find matching CSV row for JSON Ward '{wd13_name}'")

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(map_data, f, ensure_ascii=False, indent=2)
        
    print(f"Injected fresh data into {updated_count} map boundary features.")

if __name__ == "__main__":
    update_sheffield_json()