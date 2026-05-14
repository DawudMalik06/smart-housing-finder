'''
Run this file after running python/pipeline.py to update the sheffield.json file
'''
import json
import pandas as pd

def update_sheffield_json():
    csv_df = pd.read_csv("../final_output/LivabilityScores_with_Greenspace.csv")

    json_to_csv_map = {
        'Arbourthorne': 'Park & Arbourthorne Ward',
        'Beauchief and Greenhill': 'Beauchief & Greenhill Ward',
        'Beighton': 'Beighton Ward',
        'Birley': 'Birley Ward',
        'Broomhill': 'Broomhill & Sharrow Vale Ward',
        'Burngreave': 'Burngreave Ward',
        'Central': 'City Ward',
        'Crookes': 'Crookes & Crosspool Ward',
        'Darnall': 'Darnall Ward',
        'Dore and Totley': 'Dore & Totley Ward',
        'East Ecclesfield': 'East Ecclesfield Ward',
        'Ecclesall': 'Ecclesall Ward',
        'Firth Park': 'Firth Park Ward',
        'Fulwood': 'Fulwood Ward',
        'Gleadless Valley': 'Gleadless Valley Ward',
        'Graves Park': 'Graves Park Ward',
        'Hillsborough': 'Hillsborough Ward',
        'Manor Castle': 'Manor Castle Ward',
        'Mosborough': 'Mosborough Ward',
        'Nether Edge': 'Nether Edge & Sharrow Ward',
        'Richmond': 'Richmond Ward',
        'Shiregreen and Brightside': 'Shiregreen & Brightside',
        'Southey': 'Southey Ward',
        'Stannington': 'Stannington Ward',
        'Stocksbridge and Upper Don': 'Stocksbridge & Upper Don Ward',
        'Walkley': 'Walkley Ward',
        'West Ecclesfield': 'West Ecclesfield Ward',
        'Woodhouse': 'Woodhouse Ward'
    }
    
    json_path = "../dashboard/sheffield.json" 
    
    with open(json_path, "r", encoding="utf-8") as f:
        map_data = json.load(f)
    csv_lookup = csv_df.set_index('Neighborhood').to_dict('index')
    
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
            
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(map_data, f, ensure_ascii=False, indent=2)
        
    print(f"Injected fresh data into {updated_count} map boundary features.")

if __name__ == "__main__":
    update_sheffield_json()