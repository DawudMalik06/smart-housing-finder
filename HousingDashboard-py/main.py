import streamlit as st

# Page setup
st.set_page_config(page_title="SmartHousing Sheffield", layout="wide")

# --- Custom CSS Styling ---
st.markdown("""
    <style>
    .hero {
        background-image: url('https://fakeimg.com/hero.jpg');
        background-size: cover;
        background-position: center;
        padding: 5rem 2rem;
        border-radius: 12px;
        color: white;
    }
    .metric-box {
        background-color: rgba(0, 0, 0, 0.65);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-top: 1rem;
    }
    .timeline {
        background-color: #16a085;
        padding: 1rem 2rem;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        margin-top: 3rem;
        display: flex;
        justify-content: space-around;
    }
    nav a {
        margin-right: 20px;
        color: #333;
        text-decoration: none;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- Navigation Bar ---
st.markdown("""
<nav style='background-color: #ffffff; padding: 1rem; display: flex; justify-content: space-between; align-items: center;'>
    <div style='font-size: 20px; font-weight: bold;'><img src='https://fakeimg.com/logo.png' height='30'> SmartHousing</div>
    <div>
        <a href="#">Home</a>
        <a href="#">About</a>
        <a href="#">Data Insights</a>
        <a href="#">Compare Areas</a>
        <a href="#">Contact</a>
    </div>
</nav>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("""
<div class='hero'>
    <h1>Find Smart Housing That Fits Your Budget</h1>
    <p>Explore affordable, efficient homes tailored for students, families, and low-income households across Sheffield.</p>
    <div style='margin-top: 1.5rem;'>
        <a href="#" style="padding: 12px 24px; background-color: #2ecc71; color: white; border-radius: 5px; margin-right: 15px; text-decoration: none;">Start Exploring</a>
        <a href="#" style="padding: 12px 24px; background-color: #34495e; color: white; border-radius: 5px; text-decoration: none;">Learn More</a>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Why Choose Us / Metrics Section ---
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class='metric-box'>
        <h4>💸 Avg Rent Saved</h4>
        <p>£250/month</p>
        <h4>🚉 Transport Access</h4>
        <p>90% Coverage</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class='metric-box'>
        <h4>🌳 Green Spaces Nearby</h4>
        <p>75% of Listings</p>
        <h4>📱 Smart Features</h4>
        <p>85% Enabled Homes</p>
    </div>
    """, unsafe_allow_html=True)

# --- Timeline Bar ---