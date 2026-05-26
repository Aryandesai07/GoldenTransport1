import streamlit as st
import subprocess
import sys

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Golden Tamilnadu Transport",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

/* =====================================================
BACKGROUND
===================================================== */

.stApp {

    background:
    linear-gradient(rgba(0,0,0,0.78), rgba(0,0,0,0.78)),
    url("https://images.unsplash.com/photo-1502877338535-766e1452684a");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* =====================================================
HIDE STREAMLIT DEFAULT
===================================================== */

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* =====================================================
TOP HEADER
===================================================== */

.top-header {

    display:flex;
    justify-content:space-between;
    align-items:center;

    background: rgba(0,0,0,0.55);

    padding:20px 40px;

    border-radius:20px;

    backdrop-filter: blur(10px);

    border:1px solid rgba(255,255,255,0.1);

    margin-bottom:40px;
}

.logo {

    color:#FFD700;
    font-size:34px;
    font-weight:800;
}

.owner {

    color:white;
    font-size:18px;
}

/* =====================================================
HERO SECTION
===================================================== */

.hero {

    text-align:center;

    padding-top:80px;
    padding-bottom:70px;

    animation: fadeIn 1.2s ease-in;
}

.hero-title {

    color:white;

    font-size:82px;

    font-weight:900;

    line-height:1.2;
}

.hero-sub {

    color:#FFD700;

    font-size:30px;

    margin-top:25px;

    font-weight:600;
}

.hero-desc {

    color:#e0e0e0;

    font-size:20px;

    margin-top:25px;

    line-height:1.8;

    padding-left:160px;
    padding-right:160px;
}

/* =====================================================
FEATURE CARDS
===================================================== */

.feature-card {

    background: rgba(20,20,20,0.82);

    border:1px solid rgba(255,215,0,0.15);

    border-radius:22px;

    padding:35px;

    text-align:center;

    backdrop-filter: blur(12px);

    transition:0.4s;

    height:320px;
}

.feature-card:hover {

    transform:translateY(-10px);

    background: rgba(35,35,35,0.95);
}

.card-icon {

    font-size:60px;
}

.card-title {

    color:#FFD700;

    font-size:28px;

    font-weight:bold;

    margin-top:18px;
}

.card-text {

    color:white;

    margin-top:18px;

    line-height:1.8;

    font-size:16px;
}

/* =====================================================
BUTTON
===================================================== */

.stButton > button {

    background:#FFD700;

    color:black;

    border:none;

    border-radius:12px;

    font-size:22px;

    font-weight:bold;

    padding:16px 45px;

    transition:0.3s;

    width:100%;
}

.stButton > button:hover {

    background:white;

    transform:scale(1.03);
}

/* =====================================================
BOTTOM TAG
===================================================== */

.bottom-tag {

    text-align:center;

    color:rgba(255,255,255,0.55);

    margin-top:80px;

    font-size:24px;

    letter-spacing:2px;

    font-style:italic;
}

/* =====================================================
ANIMATION
===================================================== */

@keyframes fadeIn {

    from {
        opacity:0;
        transform:translateY(20px);
    }

    to {
        opacity:1;
        transform:translateY(0px);
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TOP HEADER
# =========================================================

st.markdown("""
<div class="top-header">

<div class="logo">
🚛 Golden Tamilnadu Transport
</div>

<div class="owner">
Owner : Shonandh Gounder
</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# HERO SECTION
# =========================================================

st.markdown("""
<div class="hero">

<div class="hero-title">
SMART TRANSPORT <br>
BROKER MANAGEMENT
</div>

<div class="hero-sub">
Fast • Secure • Trusted Logistics Solutions
</div>

<div class="hero-desc">

Golden Tamilnadu Transport is a professional transport broker management platform
designed for lorry owners, transport businesses, and logistics operators.
Manage transport operations professionally with smart workflow management,
driver coordination, and secure administration systems.

</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# FEATURES
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("""
    <div class="feature-card">

    <div class="card-icon">📦</div>

    <div class="card-title">
    Load Management
    </div>

    <div class="card-text">

    Efficiently manage transport loads,
    booking operations, and shipment assignments
    with professional workflow systems.

    </div>

    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class="feature-card">

    <div class="card-icon">🚛</div>

    <div class="card-title">
    Driver & Lorry Control
    </div>

    <div class="card-text">

    Manage drivers, vehicles,
    route operations, and logistics
    with advanced management tools.

    </div>

    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown("""
    <div class="feature-card">

    <div class="card-icon">📊</div>

    <div class="card-title">
    Business Analytics
    </div>

    <div class="card-text">

    Monitor revenue, transport activities,
    broker commissions, and business performance
    in real time.

    </div>

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# LOGIN BUTTON
# =========================================================

st.markdown("<br><br>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1,1,1])

with c2:

    if st.button("🔐 Open Admin Login"):

        try:

            subprocess.Popen([sys.executable, "login.py"])

            st.success("Login Window Opened Successfully")

        except Exception as e:

            st.error(f"Error Opening Login Window: {e}")

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="bottom-tag">

Driven by Trust • Powered by Technology

</div>
""", unsafe_allow_html=True)