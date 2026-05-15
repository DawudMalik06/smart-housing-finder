'''
Fetch Datasets from the appropriate links and place in /data before running this file.
Ensure names are consistent and matching.
Download requirements before running with pip install -r requirements.txt
'''
import json
import pandas as pd
import numpy as np
import geopandas as gpd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "final_output"
CONFIG_PATH = Path(__file__).parent / "config.json"

MORTGAGE_INTEREST_RATE = 0.055  #based on sheffield
MONTHS_IN_YEAR = 12

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def build_data_artifact():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    config = load_config()
    
    #house prices | https://www.sheffield.gov.uk/sites/default/files/2022-11/house-price-information.xlsx
    file_path = DATA_DIR / "Ward_House_Prices.csv"
    if not file_path.exists():
        file_path = DATA_DIR / "Neighbourhood_House_Prices.csv"
        
    cost_matrix = pd.read_csv(file_path, header=2)
    cost_matrix.columns = cost_matrix.columns.str.strip().str.lower()
    
    name_col = cost_matrix.columns[0]
    year_cols = [c for c in cost_matrix.columns if c.isdigit()]
    target_year = year_cols[-1]
    print(f"Compiling baseline transactional indices using target period: '{target_year}'")
    
    cost_matrix = cost_matrix.rename(columns={
        name_col: "Neighborhood_Raw",
        target_year: "House_Price"  
    })
    
    cost_matrix = cost_matrix.dropna(subset=["Neighborhood_Raw"])
    cost_matrix["Neighborhood_Raw"] = cost_matrix["Neighborhood_Raw"].str.strip()
    cost_matrix["Neighborhood"] = (
        cost_matrix["Neighborhood_Raw"]
        .str.replace(" Ward", "", regex=False)
        .str.replace("&", "and", regex=False)
        .str.replace("  ", " ", regex=False)
        .str.strip()
    )
    
    cost_matrix["House_Price"] = (
        cost_matrix["House_Price"]
        .astype(str)
        .str.replace(r"[£,:\-]", "", regex=True)
        .str.strip()
    )
    cost_matrix["House_Price"] = pd.to_numeric(cost_matrix["House_Price"], errors="coerce").fillna(0).astype(int)
    cost_matrix = cost_matrix[cost_matrix["House_Price"] > 0].copy()
    cost_matrix["Cost"] = ((cost_matrix["House_Price"] * MORTGAGE_INTEREST_RATE) / MONTHS_IN_YEAR).round().astype(int)
    
    #livability | https://www.gov.uk/government/statistics/english-indices-of-deprivation-2019
    deprivation_matrix = pd.read_csv(DATA_DIR / "File_7_-_All_IoD2019_Scores__Ranks__Deciles_and_Population_Denominators_3.csv")
    deprivation_matrix.columns = deprivation_matrix.columns.str.strip()
    
    sheffield_lsoas = deprivation_matrix[deprivation_matrix['Local Authority District name (2019)'] == 'Sheffield'].copy()
    max_rank = deprivation_matrix['Index of Multiple Deprivation (IMD) Rank (where 1 is most deprived)'].max()
    sheffield_lsoas['Baseline_Livability'] = sheffield_lsoas['Index of Multiple Deprivation (IMD) Rank (where 1 is most deprived)'] / max_rank
    
    mean_livability = sheffield_lsoas['Baseline_Livability'].mean()
    std_livability = sheffield_lsoas['Baseline_Livability'].std()

    ward_profiles = {
        ward: mean_livability + (multiplier * std_livability)
        for ward, multiplier in config['ward_livability_multipliers'].items()
    }
    
    cost_matrix['LivabilityScore'] = cost_matrix['Neighborhood'].map(ward_profiles)
    missing_mappings = cost_matrix[cost_matrix['LivabilityScore'].isna()]['Neighborhood'].tolist()
    if missing_mappings:
        print(f"Unmapped areas falling back to average: {missing_mappings}")
        
    cost_matrix['LivabilityScore'] = cost_matrix['LivabilityScore'].fillna(mean_livability)
    cost_matrix['LivabilityScore'] = np.clip(cost_matrix['LivabilityScore'], 0.1, 1.0).round(4)
    unified_records = cost_matrix.copy()
    
    #green spaces | https://www.data.gov.uk/dataset/90b1db1f-18e1-4e9d-bb52-a4d1c198f6f2/sheffield-parks-and-countryside-sites
    #park boundaries | https://sheffield-city-council-open-data-sheffieldcc.hub.arcgis.com/search?collection=dataset&layout=grid&tags=elections
    geojson_path = DATA_DIR / "parks_and_countrysides.geojson"
    active_green_nodes = []
    if geojson_path.exists():
        parks_spatial = gpd.read_file(geojson_path)
        active_green_nodes = parks_spatial['site_name'].dropna().str.lower().tolist()
        
    def resolve_environmental_access(name_string):
        intersect = any(name_string.lower() in node or node in name_string.lower() for node in active_green_nodes)
        return "Yes" if intersect else "No"
        
    unified_records['GreenSpace'] = unified_records['Neighborhood'].apply(resolve_environmental_access)
    established_green_vectors = config['established_green_vectors']
    unified_records.loc[unified_records['Neighborhood'].isin(established_green_vectors), 'GreenSpace'] = 'Yes'
    clean_framework = unified_records.copy()

    #ml below
    clean_framework['GreenSpace_Scalar'] = clean_framework['GreenSpace'].map({"Yes": 1, "No": 0})
    model_features = ['Cost', 'LivabilityScore', 'GreenSpace_Scalar']
    engine_scaler = StandardScaler()
    scaled_array = engine_scaler.fit_transform(clean_framework[model_features])
    
    clustering_engine = KMeans(n_clusters=3, random_state=42, n_init=10)
    clean_framework['Assigned_Cluster'] = clustering_engine.fit_predict(scaled_array)
    clean_framework['Neighborhood'] = clean_framework['Neighborhood_Raw']

    target_schema = ['Neighborhood', 'LivabilityScore', 'GreenSpace', 'Cost']
    production_artifact = clean_framework[target_schema].copy()
    destination_file = OUTPUT_DIR / "LivabilityScores_with_Greenspace.csv"
    production_artifact.to_csv(destination_file, index=False)
    
    print(f"Written to: {destination_file}")
    print(production_artifact.head(10))

if __name__ == "__main__":
    build_data_artifact()