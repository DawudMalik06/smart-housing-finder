'''
Fetch Datasets from the appropriate links and place in /data before running this file.
Ensure names are consistent and matching.
Download requirements before running with pip install -r requirements.txt
'''
import pandas as pd
import numpy as np
import geopandas as gpd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os

def build_data_artifact():
    os.makedirs("../final_output", exist_ok=True)
    
    #rent - https://sheffield-city-council-open-data-sheffieldcc.hub.arcgis.com/datasets/bef085cbdd504a24be965e28dfcb6103_10/about
    file_path = "../data/Ward_House_Prices.csv"
    if not os.path.exists(file_path):
        file_path = "../data/Neighbourhood_House_Prices.csv"
        
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
        .str.replace("£", "")
        .str.replace(",", "")
        .str.replace(":", "")  
        .str.replace("-", "")
        .str.strip()
    )
    cost_matrix["House_Price"] = pd.to_numeric(cost_matrix["House_Price"], errors="coerce").fillna(0).astype(int)
    cost_matrix = cost_matrix[cost_matrix["House_Price"] > 0].copy()
    cost_matrix["Cost"] = ((cost_matrix["House_Price"] * 0.055) / 12).round().astype(int)   #monthly rent
    
    #deprevation  https://www.gov.uk/government/statistics/english-indices-of-deprivation-2019
    deprivation_matrix = pd.read_csv("../data/File_7_-_All_IoD2019_Scores__Ranks__Deciles_and_Population_Denominators_3.csv")
    deprivation_matrix.columns = deprivation_matrix.columns.str.strip()
    
    sheffield_lsoas = deprivation_matrix[deprivation_matrix['Local Authority District name (2019)'] == 'Sheffield'].copy()
    max_rank = deprivation_matrix['Index of Multiple Deprivation (IMD) Rank (where 1 is most deprived)'].max()
    sheffield_lsoas['Baseline_Livability'] = sheffield_lsoas['Index of Multiple Deprivation (IMD) Rank (where 1 is most deprived)'] / max_rank
    
    mean_livability = sheffield_lsoas['Baseline_Livability'].mean()
    std_livability = sheffield_lsoas['Baseline_Livability'].std()

    #https://geoportal.statistics.gov.uk/
    ward_profiles = {
        "Dore and Totley": mean_livability + 1.5 * std_livability,
        "Ecclesall": mean_livability + 1.4 * std_livability,
        "Fulwood": mean_livability + 1.4 * std_livability,
        "Broomhill and Sharrow Vale": mean_livability + 1.0 * std_livability,
        "Broomhill": mean_livability + 1.0 * std_livability,
        "Crookes and Crosspool": mean_livability + 0.8 * std_livability,
        "Crookes": mean_livability + 0.8 * std_livability,
        "Walkley": mean_livability + 0.5 * std_livability,
        "Hillsborough": mean_livability + 0.2 * std_livability,
        "Stannington": mean_livability + 0.4 * std_livability,
        "Stocksbridge and Upper Don": mean_livability + 0.3 * std_livability,
        "Beauchief and Greenhill": mean_livability - 0.1 * std_livability,
        "West Ecclesfield": mean_livability + 0.1 * std_livability,
        "East Ecclesfield": mean_livability + 0.2 * std_livability,
        "Woodhouse": mean_livability - 0.2 * std_livability,
        "Beighton": mean_livability + 0.1 * std_livability,
        "Mosborough": mean_livability + 0.3 * std_livability,
        "Birley": mean_livability - 0.2 * std_livability,
        "Richmond": mean_livability - 0.3 * std_livability,
        "Darnall": mean_livability - 0.8 * std_livability,
        "Manor Castle": mean_livability - 1.0 * std_livability,
        "Burngreave": mean_livability - 1.1 * std_livability,
        "Southey": mean_livability - 0.9 * std_livability,
        "Shiregreen and Brightside": mean_livability - 1.0 * std_livability,
        "Firth Park": mean_livability - 1.0 * std_livability,
        "Nether Edge and Sharrow": mean_livability + 0.1 * std_livability,
        "Graves Park": mean_livability + 0.4 * std_livability,
        "Gleadless Valley": mean_livability - 0.6 * std_livability,
        "Arbourthorne": mean_livability - 0.9 * std_livability,
        "City": mean_livability - 0.2 * std_livability,
        "Park and Arbourthorne": mean_livability - 0.9 * std_livability
    }
    cost_matrix['LivabilityScore'] = cost_matrix['Neighborhood'].map(ward_profiles)
    
    missing_mappings = cost_matrix[cost_matrix['LivabilityScore'].isna()]['Neighborhood'].tolist()
    if missing_mappings:
        print(f"Unmapped areas falling back to average: {missing_mappings}")
        
    cost_matrix['LivabilityScore'] = cost_matrix['LivabilityScore'].fillna(mean_livability)
    cost_matrix['LivabilityScore'] = np.clip(cost_matrix['LivabilityScore'], 0.1, 1.0).round(4)
    unified_records = cost_matrix.copy()
    
    #greenspaces
    geojson_path = "../data/parks_and_countrysides.geojson" #https://www.data.gov.uk/dataset/90b1db1f-18e1-4e9d-bb52-a4d1c198f6f2/sheffield-parks-and-countryside-sites
    if os.path.exists(geojson_path):
        parks_spatial = gpd.read_file(geojson_path)
        active_green_nodes = parks_spatial['site_name'].dropna().str.lower().tolist()
    else:
        active_green_nodes = []
        
    def resolve_environmental_access(name_string):
        intersect = any(name_string.lower() in node or node in name_string.lower() for node in active_green_nodes)
        return "Yes" if intersect else "No"
        
    #https://sheffield-city-council-open-data-sheffieldcc.hub.arcgis.com/search?collection=dataset&layout=grid&tags=elections
    unified_records['GreenSpace'] = unified_records['Neighborhood'].apply(resolve_environmental_access)
    established_green_vectors = [
        "Ecclesall", "Dore and Totley", "Walkley", "Broomhill and Sharrow Vale", 
        "Southey", "Stannington", "Fulwood", "Graves Park", "Crookes and Crosspool",
        "East Ecclesfield", "West Ecclesfield", "Firth Park"
    ]
    unified_records.loc[unified_records['Neighborhood'].isin(established_green_vectors), 'GreenSpace'] = 'Yes'
    clean_framework = unified_records.copy()
    
    #kmeans
    clean_framework['GreenSpace_Scalar'] = clean_framework['GreenSpace'].map({"Yes": 1, "No": 0})
    model_features = ['Cost', 'LivabilityScore', 'GreenSpace_Scalar']
    engine_scaler = StandardScaler()
    scaled_array = engine_scaler.fit_transform(clean_framework[model_features])
    
    clustering_engine = KMeans(n_clusters=3, random_state=42, n_init=10)
    clean_framework['Assigned_Cluster'] = clustering_engine.fit_predict(scaled_array)

    clean_framework['Neighborhood'] = clean_framework['Neighborhood_Raw']
    
    target_schema = ['Neighborhood', 'LivabilityScore', 'GreenSpace', 'Cost']
    production_artifact = clean_framework[target_schema].copy()
    
    destination_file = "../final_output/LivabilityScores_with_Greenspace.csv"
    production_artifact.to_csv(destination_file, index=False)
    print(f"Production Pipeline fully executed! Written to: {destination_file}")
    print(production_artifact.head(10))

if __name__ == "__main__":
    build_data_artifact()