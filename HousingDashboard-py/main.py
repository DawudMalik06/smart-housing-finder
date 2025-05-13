import streamlit as st

st.set_page_config(page_title="SmartHousing", layout="wide")

# CSS that animates full-page background via ::before on .stApp
st.markdown("""
    <style>
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        z-index: -1;
        animation: bgSlide 20s infinite;
        background-size: cover;
        background-position: center;
    }

    @keyframes bgSlide {
        0%   { background-image: url('https://i.postimg.cc/ncP3vLPb/House-Image-1.avif'); }
        33%  { background-image: url('https://i.postimg.cc/85LCbsHy/House-Image-2.avif'); }
        66%  { background-image: url('https://i.postimg.cc/8CMG296c/House-Image-3.avif'); }
        100% { background-image: url('https://i.postimg.cc/wMBSjG7h/House-Image-4.avif'); }
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
    </style>
""", unsafe_allow_html=True)

# --- NAVBAR ---
st.markdown("""
    <div class="navbar">
        <div><strong>SmartHousing</strong></div>
        <div>
            <a href="#">Home</a>
            <a href="#">About</a>
            <a href="#">Data Insights</a>
            <a href="#">Compare Areas</a>
            <a href="#">Contact</a>
        </div>
    </div>
""", unsafe_allow_html=True)

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
    st.markdown("""
        <div class='stat-card'>
            <h4>🎓 98% Graduate Employment</h4>
            <h4>🌍 45+ International Partners</h4>
            <h4>👩‍🏫 15:1 Student-Faculty Ratio</h4>
            <h4>📚 120+ Degree Programs</h4>
        </div>
    """, unsafe_allow_html=True)

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
