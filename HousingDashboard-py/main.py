# Rewriting and correcting the entire Streamlit code with fixed indentation and proper structure for map integration
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pydeck as pdk

st.set_page_config(page_title="SmartHousing", layout="wide")

# ✅ CSS override for the entire Streamlit app background
st.markdown("""
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
</style>
""", unsafe_allow_html=True)

# --- NAVBAR ---
page = st.selectbox("Navigate", ["Home", "Data Insights", "Compare Areas"])

# --- PAGE CONTENT SWITCHING ---
if page == "Home":
    st.title("🏠 Home Page")
    st.write("Welcome to the Smart Housing Finder")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<h1 class='shadow-text' style='color:white;'>Empowering Futures<br>Through Smart Housing</h1>", unsafe_allow_html=True)
        st.markdown("<p class='shadow-text' style='color:white; font-size:1.1rem;'>Explore affordable, energy-efficient homes tailored for students, families, and low-income households across Sheffield.</p>", unsafe_allow_html=True)
        colA, colB = st.columns([1, 1])
        with colA:
            st.button("Start Your Journey")
        with colB:
            st.button("Discover Programs")
    with col2:
        st.markdown("<div class='stat-card'><h4>🎓 98% Graduate Employment</h4><h4>🌍 45+ International Partners</h4><h4>👩‍🏫 15:1 Student-Faculty Ratio</h4><h4>📚 120+ Degree Programs</h4></div>", unsafe_allow_html=True)

elif page == "Data Insights":
    st.title("📊 Data Insights")
    st.markdown("Explore housing data across Sheffield:")

    try:
        csv_path = os.path.join(os.getcwd(), "data/housing_insights.csv")
        df = pd.read_csv(csv_path)
        st.success("✅ CSV loaded successfully!")

        # Charts
        sns.set(style="whitegrid")
        fig, axs = plt.subplots(2, 2, figsize=(12, 8))

        sns.barplot(x="Avg Rent (£)", y="Area", data=df, ax=axs[0, 0], palette="Blues_d")
        axs[0, 0].set_title("Average Rent by Area")
        sns.barplot(x="Transport Score", y="Area", data=df, ax=axs[0, 1], palette="Greens_d")
        axs[0, 1].set_title("Public Transport Accessibility")
        sns.barplot(x="Energy Rating A-B (%)", y="Area", data=df, ax=axs[1, 0], palette="Oranges_d")
        axs[1, 0].set_title("Energy-Efficient Homes")
        sns.barplot(x="Smart Homes (%)", y="Area", data=df, ax=axs[1, 1], palette="Purples_d")
        axs[1, 1].set_title("Smart Feature Adoption")

        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("### 🗺️ Interactive Housing Map")
        if {"Latitude", "Longitude"}.issubset(df.columns):
            df["icon_data"] = [{
                "url": "https://cdn-icons-png.flaticon.com/512/484/484167.png",
                "width": 512,
                "height": 512,
                "anchorY": 512
            } for _ in range(len(df))]

            icon_layer = pdk.Layer(
                type="IconLayer",
                data=df,
                get_icon="icon_data",
                get_position="[Longitude, Latitude]",
                get_size=4,
                size_scale=10,
                pickable=True
            )

            tooltip = {
                "html": "<b>{{Area}}</b><br>Rent: £{{Avg Rent (£)}}<br>Transport Score: {{Transport Score}}<br>Smart Homes: {{Smart Homes (%)}}%",
                "style": {"backgroundColor": "steelblue", "color": "white"}
            }

            view_state = pdk.ViewState(
                latitude=df["Latitude"].mean(),
                longitude=df["Longitude"].mean(),
                zoom=11,
                pitch=0
            )

            st.pydeck_chart(pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state=view_state,
                layers=[icon_layer],
                tooltip=tooltip
            ))
        else:
            st.warning("Map could not be displayed — latitude/longitude data missing.")

    except FileNotFoundError:
        st.error("❌ CSV file not found. Please check the path: `data/housing_insights.csv`")

elif page == "Compare Areas":
    st.title("📍 Compare Areas")
    st.write("Comparison feature coming soon!")

