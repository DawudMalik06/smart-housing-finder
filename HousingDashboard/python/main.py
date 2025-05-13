import streamlit as st

# Set the page configuration
st.set_page_config(page_title="Smart Housing Finder", layout="wide")

# Header
st.markdown("<h1 style='text-align: left; color: white;'>Empowering Futures Through Smart Housing</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left; color: white;'>Find affordable smart housing options tailored to your needs.</p>", unsafe_allow_html=True)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.button("Start Your Journey")
    st.button("Discover Programs")

with col2:
    st.markdown("<h3 style='color: white;'>Why Choose Us</h3>", unsafe_allow_html=True)
    st.markdown("""
    <ul style='color: white;'>
        <li>Affordable Housing Market Areas</li>
        <li>Demographic Profiles</li>
        <li>Public Transport Accessibility</li>
        <li>Air Quality and Green Spaces</li>
        <li>Local Development Plans</li>
    </ul>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white;'>Upcoming Events</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white;'>NOV 15 - Open House Day | DEC 5 - Application Workshop | JAN 10 - Orientation</p>", unsafe_allow_html=True)

# Background styling
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('YOUR_IMAGE_URL_HERE');
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)