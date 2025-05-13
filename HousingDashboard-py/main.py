import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pydeck as pdk
import numpy as np

st.set_page_config(page_title="SmartHousing", layout="wide")

# ✅ CSS override for the entire Streamlit app background
st.markdown(
    """
    <style>
    .stApp {
        animation: bgSlide 25s infinite;
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }

    @keyframes bgSlide {
        0%   { background-image: url('https://images.unsplash.com/photo-1580587771525-78b9dba3b914'); }
        33%  { background-image: url('https://images.unsplash.com/photo-1568605114967-8130f3a36994'); }
        66%  { background-image: url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c'); }
        100% { background-image: url('https://images.unsplash.com/photo-1580587771525-78b9dba3b914'); }
    }

    .shadow-text {
        text-shadow: 1px 1px 4px rgba(0,0,0,0.8);
    }

    .navbar {
        background-color: white;
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-radius: 0 0 12px 12px;
        margin-bottom: 2rem;
    }

    .navbar a {
        margin-left: 20px;
        font-weight: 600;
        text-decoration: none;
        color: #2c3e50;
    }

    .stat-card {
        background-color: rgba(0,0,0,0.7);
        border-radius: 10px;
        padding: 2rem;
        color: white;
    }

    .timeline-col {
        background-color: #16a085;
        border-radius: 8px;
        padding: 1rem;
        color: white;
        text-align: center;
        font-weight: bold;
    }

    .timeline-col a {
        color: white;
        text-decoration: underline;
    }

    .chart-container {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .filter-container {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    .map-container {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- SAMPLE DATA (if CSV is not found) ---
@st.cache_data
def load_sample_data():
    # Sheffield areas with approximate coordinates
    areas = [
        "City Centre", "Ecclesall", "Broomhill", "Crookes", 
        "Hillsborough", "Meadowhall", "Dore", "Walkley", 
        "Nether Edge", "Burngreave", "Darnall", "Sharrow"
    ]
    
    # Latitude and longitude coordinates for Sheffield areas
    coordinates = [
        [53.3811, -1.4701],  # City Centre
        [53.3600, -1.5099],  # Ecclesall
        [53.3800, -1.5001],  # Broomhill
        [53.3900, -1.5099],  # Crookes
        [53.4100, -1.5001],  # Hillsborough
        [53.4141, -1.4172],  # Meadowhall
        [53.3200, -1.5199],  # Dore
        [53.3950, -1.5050],  # Walkley
        [53.3550, -1.4899],  # Nether Edge
        [53.3950, -1.4501],  # Burngreave
        [53.3890, -1.4202],  # Darnall
        [53.3690, -1.4801]   # Sharrow
    ]
    
    # Generate sample data
    np.random.seed(42)
    
    # Create rent prices that match the UI filters
    rent_prices = [
        950,  # City Centre
        1100, # Ecclesall
        950,  # Broomhill
        850,  # Crookes
        880,  # Hillsborough
        780,  # Meadowhall
        1200, # Dore
        870,  # Walkley
        920,  # Nether Edge
        680,  # Burngreave
        700,  # Darnall
        800   # Sharrow
    ]
    
    sample_data = {
        'Area': areas,
        'Latitude': [coord[0] for coord in coordinates],
        'Longitude': [coord[1] for coord in coordinates],
        'Avg Rent (£)': rent_prices,
        'Transport Score': np.random.randint(50, 100, len(areas)),
        'Energy Rating A-B (%)': np.random.randint(10, 90, len(areas)),
        'Smart Homes (%)': np.random.randint(5, 80, len(areas)),
        'Available Properties': np.random.randint(10, 200, len(areas)),
        'Schools Nearby': np.random.randint(1, 10, len(areas)),
        'Crime Rate (per 1000)': np.random.randint(20, 120, len(areas)),
        'Green Spaces': np.random.randint(1, 15, len(areas))
    }
    
    df = pd.DataFrame(sample_data)
    
    # Add some values to match what's in the UI
    for idx, area in enumerate(df['Area']):
        if area == "Broomhill":
            df.loc[idx, 'Transport Score'] = 85
        elif area == "Crookes":
            df.loc[idx, 'Transport Score'] = 75
        elif area == "Ecclesall":
            df.loc[idx, 'Transport Score'] = 82
        elif area == "Darnall":
            df.loc[idx, 'Transport Score'] = 62
        elif area == "Sharrow":
            df.loc[idx, 'Transport Score'] = 72  
        elif area == "Walkley":
            df.loc[idx, 'Transport Score'] = 78
        elif area == "Nether Edge":
            df.loc[idx, 'Transport Score'] = 80
        elif area == "Burngreave":
            df.loc[idx, 'Transport Score'] = 67
            
    return df

# --- LOAD DATA ---
@st.cache_data
def load_data():
    try:
        csv_path = os.path.join(os.getcwd(), "data/housing_insights.csv")
        df = pd.read_csv(csv_path)
        # Clean the data - replace NaN values with defaults
        for col in df.columns:
            if df[col].dtype == 'float64' or df[col].dtype == 'int64':
                df[col] = df[col].fillna(df[col].mean() if not df[col].isna().all() else 0)
            else:
                df[col] = df[col].fillna("Unknown")
        return df
    except FileNotFoundError:
        st.warning("⚠️ Sample data is being used. For real data, please add a CSV file at `data/housing_insights.csv`")
        return load_sample_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return load_sample_data()

# --- VISUALIZATION FUNCTIONS ---
def create_bar_chart(data, x_column, y_column, title, color_palette="Blues_d"):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=x_column, y=y_column, data=data, palette=color_palette, ax=ax)
    ax.set_title(title, fontsize=16)
    ax.set_xlabel(x_column, fontsize=12)
    ax.set_ylabel(y_column, fontsize=12)
    plt.tight_layout()
    return fig

def create_line_chart(data, x_column, y_column, title, color_palette="Blues_d"):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Sort data for better line visualization
    sorted_data = data.sort_values(by=x_column)
    
    # Plot line
    ax.plot(sorted_data[x_column], sorted_data.index, marker='o', linewidth=2, 
            color=sns.color_palette(color_palette)[3])
    
    # Set y-ticks to area names
    ax.set_yticks(sorted_data.index)
    ax.set_yticklabels(sorted_data[y_column])
    
    ax.set_title(title, fontsize=16)
    ax.set_xlabel(x_column, fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    return fig

def create_pie_chart(data, column, title):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Get values and labels
    values = data[column].values
    labels = data['Area'].values
    
    # Create pie chart
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, 
           wedgeprops={'edgecolor': 'white', 'linewidth': 1})
    ax.set_title(title, fontsize=16)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.tight_layout()
    return fig

def create_map(data, lat_col, lon_col, radius_col=None, color_col=None):
    # Make a copy to avoid modifying the original dataframe
    map_data = data.copy()
    
    # Calculate radius size if provided
    if radius_col:
        # Handle potential NaN values in the radius column
        if map_data[radius_col].isna().any():
            # Fill NaN values with the mean or a default value
            map_data[radius_col] = map_data[radius_col].fillna(map_data[radius_col].mean() if not map_data[radius_col].isna().all() else 100)
            
        radius_min = 100
        radius_max = 1000
        radius_range = max(map_data[radius_col].max() - map_data[radius_col].min(), 1)  # Avoid division by zero
        radius_scale = (radius_max - radius_min) / radius_range
        map_data['radius'] = map_data[radius_col].apply(lambda x: radius_min + (x - map_data[radius_col].min()) * radius_scale)
    else:
        map_data['radius'] = 300
    
    # Set color if provided
    if color_col:
        # Handle potential NaN values in the color column
        if map_data[color_col].isna().any():
            # Fill NaN values with the mean or a default value
            map_data[color_col] = map_data[color_col].fillna(map_data[color_col].mean() if not map_data[color_col].isna().all() else 50)
            
        # Normalize the color values between 0 and 255
        min_val = map_data[color_col].min()
        max_val = map_data[color_col].max()
        value_range = max(max_val - min_val, 1)  # Avoid division by zero
        
        map_data['color_r'] = map_data[color_col].apply(lambda x: int(255 * (1 - (x - min_val) / value_range)))
        map_data['color_g'] = map_data[color_col].apply(lambda x: int(100 + 155 * ((x - min_val) / value_range)))
        map_data['color_b'] = 50
    else:
        map_data['color_r'] = 33
        map_data['color_g'] = 102
        map_data['color_b'] = 172
    
    # Create tooltip for the data points - handle potential missing values
    map_data['tooltip'] = map_data.apply(
        lambda row: f"{row['Area']}<br>" + 
                   (f"Avg Rent: £{row['Avg Rent (£)']}<br>" if 'Avg Rent (£)' in row and not pd.isna(row['Avg Rent (£)']) else "") + 
                   (f"Transport Score: {row['Transport Score']}" if 'Transport Score' in row and not pd.isna(row['Transport Score']) else ""),
        axis=1
    )
    
    # Create the PyDeck layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        map_data,
        get_position=["Longitude", "Latitude"],
        get_radius="radius",
        get_fill_color=["color_r", "color_g", "color_b", 180],
        pickable=True,
    )
    
    # Set initial view state
    view_state = pdk.ViewState(
        latitude=map_data["Latitude"].mean(),
        longitude=map_data["Longitude"].mean(),
        zoom=11,
        pitch=0,
    )
    
    # Create the deck
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{tooltip}"},
    )
    
    return deck

# --- NAVBAR ---
page = st.selectbox("Navigate", ["Home", "Data Insights", "Compare Areas", "Interactive Map"])

# --- PAGE CONTENT SWITCHING ---
if page == "Home":
    st.title("🏠 Home Page")
    st.write("Welcome to the Smart Housing Finder")

    # --- HERO SECTION ---
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<h1 class='shadow-text' style='color:white;'>Empowering Futures<br>Through Smart Housing</h1>", unsafe_allow_html=True)
        st.markdown(
            "<p class='shadow-text' style='color:white; font-size:1.1rem; max-width:600px;'>Explore affordable, energy-efficient homes tailored for students, families, and low-income households across Sheffield.</p>",
            unsafe_allow_html=True
        )
        colA, colB = st.columns([1, 1])
        with colA:
            st.button("Start Your Journey")
        with colB:
            st.button("Discover Programs")

    with col2:
        st.markdown(
            "<div class='stat-card'>"
            "<h4>🎓 98% Graduate Employment</h4>"
            "<h4>🌍 45+ International Partners</h4>"
            "<h4>👩‍🏫 15:1 Student-Faculty Ratio</h4>"
            "<h4>📚 120+ Degree Programs</h4>"
            "</div>",
            unsafe_allow_html=True
        )

    # --- TIMELINE ---
    st.markdown("###")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            "<div class='timeline-col'><div>NOV 15</div><div>Open House Day</div><div><a href='#'>Register</a></div></div>",
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            "<div class='timeline-col'><div>DEC 5</div><div>Application Workshop</div><div><a href='#'>Register</a></div></div>",
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            "<div class='timeline-col'><div>JAN 10</div><div>Student Orientation</div><div><a href='#'>Register</a></div></div>",
            unsafe_allow_html=True
        )

elif page == "Data Insights":
    st.title("📊 Data Insights")
    
    # Load data
    df = load_data()
    
    # Set up control panel for chart selection
    st.markdown("<div class='filter-container'>", unsafe_allow_html=True)
    chart_type = st.radio("Select Chart Type:", ["Bar Chart", "Line Chart", "Pie Chart"], horizontal=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Create charts based on selection
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        metric = st.selectbox("Select Metric for Chart 1:", 
                              ["Avg Rent (£)", "Transport Score", "Energy Rating A-B (%)", "Smart Homes (%)", 
                               "Available Properties", "Schools Nearby", "Crime Rate (per 1000)", "Green Spaces"])
        
        if chart_type == "Bar Chart":
            fig = create_bar_chart(df, metric, "Area", f"{metric} by Area", "Blues_d")
            st.pyplot(fig)
        elif chart_type == "Line Chart":
            fig = create_line_chart(df, metric, "Area", f"{metric} by Area", "Blues_d")
            st.pyplot(fig)
        else:  # Pie Chart
            fig = create_pie_chart(df, metric, f"Distribution of {metric}")
            st.pyplot(fig)
    
    with col2:
        metric2 = st.selectbox("Select Metric for Chart 2:", 
                              ["Transport Score", "Avg Rent (£)", "Energy Rating A-B (%)", "Smart Homes (%)",
                               "Available Properties", "Schools Nearby", "Crime Rate (per 1000)", "Green Spaces"])
        
        if chart_type == "Bar Chart":
            fig = create_bar_chart(df, metric2, "Area", f"{metric2} by Area", "Greens_d")
            st.pyplot(fig)
        elif chart_type == "Line Chart":
            fig = create_line_chart(df, metric2, "Area", f"{metric2} by Area", "Greens_d")
            st.pyplot(fig)
        else:  # Pie Chart
            fig = create_pie_chart(df, metric2, f"Distribution of {metric2}")
            st.pyplot(fig)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Additional charts
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        metric3 = st.selectbox("Select Metric for Chart 3:", 
                              ["Energy Rating A-B (%)", "Avg Rent (£)", "Transport Score", "Smart Homes (%)",
                               "Available Properties", "Schools Nearby", "Crime Rate (per 1000)", "Green Spaces"])
        
        if chart_type == "Bar Chart":
            fig = create_bar_chart(df, metric3, "Area", f"{metric3} by Area", "Oranges_d")
            st.pyplot(fig)
        elif chart_type == "Line Chart":
            fig = create_line_chart(df, metric3, "Area", f"{metric3} by Area", "Oranges_d")
            st.pyplot(fig)
        else:  # Pie Chart
            fig = create_pie_chart(df, metric3, f"Distribution of {metric3}")
            st.pyplot(fig)
    
    with col2:
        metric4 = st.selectbox("Select Metric for Chart 4:", 
                              ["Smart Homes (%)", "Avg Rent (£)", "Transport Score", "Energy Rating A-B (%)",
                               "Available Properties", "Schools Nearby", "Crime Rate (per 1000)", "Green Spaces"])
        
        if chart_type == "Bar Chart":
            fig = create_bar_chart(df, metric4, "Area", f"{metric4} by Area", "Purples_d")
            st.pyplot(fig)
        elif chart_type == "Line Chart":
            fig = create_line_chart(df, metric4, "Area", f"{metric4} by Area", "Purples_d")
            st.pyplot(fig)
        else:  # Pie Chart
            fig = create_pie_chart(df, metric4, f"Distribution of {metric4}")
            st.pyplot(fig)
    
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Compare Areas":
    st.title("📍 Compare Areas")
    
    # Load data
    df = load_data()
    
    # Area selection
    st.markdown("<div class='filter-container'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    # Check if we have at least two areas to compare
    if len(df['Area'].unique()) >= 2:
        with col1:
            area1 = st.selectbox("Select First Area:", df['Area'].unique())
        with col2:
            area2_options = [a for a in df['Area'].unique() if a != area1]
            area2 = st.selectbox("Select Second Area:", area2_options)
            
        # Filter data for selected areas - with error handling
        try:
            area1_data = df[df['Area'] == area1].iloc[0]
            area2_data = df[df['Area'] == area2].iloc[0]
            
            # Display comparisons
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            
            # Create comparison metrics
            metrics = ["Avg Rent (£)", "Transport Score", "Energy Rating A-B (%)", "Smart Homes (%)", 
                      "Available Properties", "Schools Nearby", "Crime Rate (per 1000)", "Green Spaces"]
            
            # Ensure metrics exist in the dataframe
            valid_metrics = [m for m in metrics if m in df.columns]
            
            if len(valid_metrics) > 0:
                comparison_data = {
                    'Metric': valid_metrics,
                    area1: [area1_data[metric] for metric in valid_metrics],
                    area2: [area2_data[metric] for metric in valid_metrics]
                }
                
                comparison_df = pd.DataFrame(comparison_data)
                
                # Create comparison visualization
                fig, ax = plt.subplots(figsize=(12, 6))
                
                x = np.arange(len(valid_metrics))
                width = 0.35
                
                bar1 = ax.bar(x - width/2, comparison_df[area1], width, label=area1, color='#3498db')
                bar2 = ax.bar(x + width/2, comparison_df[area2], width, label=area2, color='#2ecc71')
                
                ax.set_title('Area Comparison', fontsize=16)
                ax.set_xticks(x)
                ax.set_xticklabels(valid_metrics, rotation=45, ha='right')
                ax.legend()
                ax.grid(axis='y', linestyle='--', alpha=0.7)
                
                # Add value labels on top of bars
                for i, v in enumerate(comparison_df[area1]):
                    ax.text(i - width/2, v + 0.5, str(int(v) if v.is_integer() else round(v, 1)), ha='center', fontsize=9)
                
                for i, v in enumerate(comparison_df[area2]):
                    ax.text(i + width/2, v + 0.5, str(int(v) if v.is_integer() else round(v, 1)), ha='center', fontsize=9)
                
                plt.tight_layout()
                st.pyplot(fig)
                
                # Text comparison
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                st.subheader(f"{area1} vs {area2} - Detailed Analysis")
                
                col1, col2 = st.columns(2)
                with col1:
                    if "Avg Rent (£)" in valid_metrics:
                        st.metric(label="Average Rent", 
                                 value=f"£{int(area1_data['Avg Rent (£)'])}", 
                                 delta=f"{int(area1_data['Avg Rent (£)'] - area2_data['Avg Rent (£)'])}",
                                 delta_color="inverse")
                    if "Transport Score" in valid_metrics:
                        st.metric(label="Transport Score", 
                                 value=f"{int(area1_data['Transport Score'])}/100", 
                                 delta=int(area1_data['Transport Score'] - area2_data['Transport Score']))
                    if "Energy Rating A-B (%)" in valid_metrics:
                        st.metric(label="Energy Efficiency", 
                                 value=f"{int(area1_data['Energy Rating A-B (%)'])}%", 
                                 delta=int(area1_data['Energy Rating A-B (%)'] - area2_data['Energy Rating A-B (%)']))
                    if "Smart Homes (%)" in valid_metrics:
                        st.metric(label="Smart Features", 
                                 value=f"{int(area1_data['Smart Homes (%)'])}%", 
                                 delta=int(area1_data['Smart Homes (%)'] - area2_data['Smart Homes (%)']))
                
                with col2:
                    if "Available Properties" in valid_metrics:
                        st.metric(label="Available Properties", 
                                 value=f"{int(area1_data['Available Properties'])}", 
                                 delta=int(area1_data['Available Properties'] - area2_data['Available Properties']))
                    if "Schools Nearby" in valid_metrics:
                        st.metric(label="Schools Nearby", 
                                 value=f"{int(area1_data['Schools Nearby'])}", 
                                 delta=int(area1_data['Schools Nearby'] - area2_data['Schools Nearby']))
                    if "Crime Rate (per 1000)" in valid_metrics:
                        st.metric(label="Crime Rate", 
                                 value=f"{int(area1_data['Crime Rate (per 1000)'])} per 1000", 
                                 delta=-(int(area1_data['Crime Rate (per 1000)'] - area2_data['Crime Rate (per 1000)'])),
                                 delta_color="inverse")
                    if "Green Spaces" in valid_metrics:
                        st.metric(label="Green Spaces", 
                                 value=f"{int(area1_data['Green Spaces'])}", 
                                 delta=int(area1_data['Green Spaces'] - area2_data['Green Spaces']))
                
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error("No valid metrics found in the data for comparison.")
                
        except (IndexError, KeyError) as e:
            st.error(f"Error comparing areas: {e}")
            st.warning("Make sure both areas exist in your dataset.")
    else:
        st.warning("Need at least two distinct areas in your data to perform comparison.")

elif page == "Interactive Map":
    st.title("🗺️ Interactive Map")
    
    # Load data
    df = load_data()
    
    # Map filters
    st.markdown("<div class='filter-container'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        radius_metric = st.selectbox(
            "Circle Size Based On:", 
            ["Avg Rent (£)", "Transport Score", "Energy Rating A-B (%)", "Smart Homes (%)",
             "Available Properties", "Schools Nearby", "Crime Rate (per 1000)", "Green Spaces"]
        )
    
    with col2:
        color_metric = st.selectbox(
            "Circle Color Based On:",
            ["Transport Score", "Avg Rent (£)", "Energy Rating A-B (%)", "Smart Homes (%)",
             "Available Properties", "Schools Nearby", "Crime Rate (per 1000)", "Green Spaces"]
        )
    
    with col3:
        filtered_areas = st.multiselect("Filter Areas:", df['Area'].unique(), default=df['Area'].unique())
    
    # Apply filters
    if filtered_areas:
        filtered_df = df[df['Area'].isin(filtered_areas)]
    else:
        filtered_df = df
    
    # Handle potential NaN values for the rent slider
    min_rent_value = df['Avg Rent (£)'].min()
    max_rent_value = df['Avg Rent (£)'].max()
    
    # Check for NaN values and provide default values if needed
    if pd.isna(min_rent_value):
        min_rent_value = 500
    if pd.isna(max_rent_value):
        max_rent_value = 1500
        
    min_rent = st.slider("Maximum Rent (£)", 
                         min_value=int(min_rent_value), 
                         max_value=int(max_rent_value),
                         value=int(max_rent_value))
    
    filtered_df = filtered_df[filtered_df['Avg Rent (£)'] <= min_rent]
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Create map
    st.markdown("<div class='map-container'>", unsafe_allow_html=True)
    # Check if dataframe is valid and has required columns before creating map
    required_columns = ["Latitude", "Longitude", "Area", "Avg Rent (£)", "Transport Score"]
    
    if not filtered_df.empty and all(col in filtered_df.columns for col in required_columns):
        # Check for NaN values in coordinate columns
        filtered_df = filtered_df.dropna(subset=["Latitude", "Longitude"])
        
        if not filtered_df.empty:
            st.pydeck_chart(create_map(filtered_df, "Latitude", "Longitude", radius_metric, color_metric))
        else:
            st.warning("No valid coordinates found for the selected areas.")
    else:
        st.warning("No areas match your filters or required data is missing. Please adjust your criteria.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Display data table below map
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.subheader("Area Details")
    st.dataframe(filtered_df)
    st.markdown("</div>", unsafe_allow_html=True)