import streamlit as st
import streamlit.components.v1 as components
import subprocess
import sys
import time

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
# FULL SCREEN LOADING ANIMATION
# =========================================================

loading_html = """
<div id="loader">
    <div class="truck-container">
        <div class="road"></div>
        <div class="truck">🚛</div>
    </div>

    <div class="loading-text">
        GOLDEN TAMILNADU TRANSPORT
    </div>

    <div class="sub-loading">
        Smart Logistics System Initializing...
    </div>
</div>

<style>

#loader{
    position:fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    background:black;
    z-index:999999;

    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;

    animation:hideLoader 5s forwards;
    animation-delay:3.8s;
}

.truck-container{
    width:80%;
    position:relative;
}

.road{
    width:100%;
    height:8px;
    background:#FFD700;
    border-radius:20px;
    margin-top:40px;
    overflow:hidden;
}

.truck{
    font-size:90px;
    position:absolute;
    top:-70px;
    left:-10%;
    animation:moveTruck 4s linear forwards;
}

.loading-text{
    color:#FFD700;
    font-size:55px;
    font-weight:900;
    margin-top:60px;
    letter-spacing:3px;

    animation:pulse 1.5s infinite;
}

.sub-loading{
    color:white;
    margin-top:20px;
    font-size:24px;
}

@keyframes moveTruck{
    0%{
        left:-10%;
    }

    100%{
        left:90%;
    }
}

@keyframes pulse{
    0%{
        opacity:0.4;
    }

    50%{
        opacity:1;
    }

    100%{
        opacity:0.4;
    }
}

@keyframes hideLoader{
    to{
        opacity:0;
        visibility:hidden;
    }
}

</style>
"""

components.html(loading_html, height=0)

# =========================================================
# MAIN CSS
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"] {

    font-family: 'Segoe UI', sans-serif;
    scroll-behavior:smooth;
}

/* =====================================================
BACKGROUND VIDEO EFFECT
===================================================== */

.stApp {

    background:
    linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.82)),
    url("https://images.unsplash.com/photo-1502877338535-766e1452684a");

    background-size:cover;
    background-position:center;
    background-attachment:fixed;
}

/* =====================================================
HIDE STREAMLIT
===================================================== */

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* =====================================================
FLOATING PARTICLES
===================================================== */

.particles {

    position:fixed;
    width:100%;
    height:100%;
    top:0;
    left:0;
    z-index:-1;
    overflow:hidden;
}

.particles span {

    position:absolute;
    display:block;
    width:6px;
    height:6px;
    background:#FFD700;
    border-radius:50%;

    animation:animate 15s linear infinite;
    bottom:-150px;
}

.particles span:nth-child(1){
left:10%;
animation-duration:10s;
width:4px;
height:4px;
}

.particles span:nth-child(2){
left:20%;
animation-duration:12s;
}

.particles span:nth-child(3){
left:35%;
animation-duration:18s;
}

.particles span:nth-child(4){
left:50%;
animation-duration:9s;
}

.particles span:nth-child(5){
left:65%;
animation-duration:16s;
}

.particles span:nth-child(6){
left:80%;
animation-duration:11s;
}

.particles span:nth-child(7){
left:90%;
animation-duration:20s;
}

@keyframes animate {

    0%{
        transform:translateY(0) rotate(0deg);
        opacity:0;
    }

    10%{
        opacity:1;
    }

    100%{
        transform:translateY(-1000px) rotate(720deg);
        opacity:0;
    }
}

/* =====================================================
TOP HEADER
===================================================== */

.top-header {

    display:flex;
    justify-content:space-between;
    align-items:center;

    padding:25px 50px;

    border-radius:25px;

    background:rgba(0,0,0,0.45);

    backdrop-filter:blur(12px);

    border:1px solid rgba(255,215,0,0.2);

    animation:slideTop 1.2s ease;
}

.logo {

    color:#FFD700;
    font-size:38px;
    font-weight:900;

    text-shadow:0px 0px 15px #FFD700;
}

.owner {

    color:white;
    font-size:20px;
}

/* =====================================================
HERO SECTION
===================================================== */

.hero {

    text-align:center;

    padding-top:120px;
    padding-bottom:90px;

    animation:fadeUp 1.5s ease;
}

.hero-title {

    color:white;

    font-size:90px;

    font-weight:900;

    line-height:1.1;

    text-shadow:0px 0px 20px rgba(255,215,0,0.4);
}

.hero-sub {

    color:#FFD700;

    font-size:34px;

    margin-top:30px;

    font-weight:700;
}

.hero-desc {

    color:#e0e0e0;

    font-size:21px;

    margin-top:35px;

    line-height:1.9;

    padding-left:180px;
    padding-right:180px;
}

/* =====================================================
FEATURE CARDS
===================================================== */

.feature-card {

    background:rgba(20,20,20,0.72);

    border:1px solid rgba(255,215,0,0.2);

    border-radius:25px;

    padding:40px;

    text-align:center;

    height:340px;

    transition:0.5s;

    backdrop-filter:blur(15px);

    animation:fadeUp 2s ease;
}

.feature-card:hover {

    transform:translateY(-15px) scale(1.03);

    box-shadow:0px 0px 30px rgba(255,215,0,0.4);

    border:1px solid #FFD700;
}

.card-icon {

    font-size:70px;

    animation:float 3s infinite ease-in-out;
}

.card-title {

    color:#FFD700;

    font-size:30px;

    font-weight:800;

    margin-top:20px;
}

.card-text {

    color:white;

    margin-top:20px;

    line-height:1.9;

    font-size:17px;
}

/* =====================================================
BUTTON
===================================================== */

.stButton > button {

    background:linear-gradient(45deg,#FFD700,#ffae00);

    color:black;

    border:none;

    border-radius:15px;

    font-size:24px;

    font-weight:800;

    padding:18px 40px;

    transition:0.4s;

    width:100%;

    box-shadow:0px 0px 20px rgba(255,215,0,0.4);
}

.stButton > button:hover {

    transform:scale(1.05);

    background:white;

    box-shadow:0px 0px 35px rgba(255,255,255,0.6);
}

/* =====================================================
BOTTOM FOOTER
===================================================== */

.bottom-tag {

    text-align:center;

    color:rgba(255,255,255,0.6);

    margin-top:100px;

    margin-bottom:50px;

    font-size:24px;

    letter-spacing:3px;

    animation:fadeUp 2.5s ease;
}

/* =====================================================
ANIMATIONS
===================================================== */

@keyframes fadeUp {

    from{
        opacity:0;
        transform:translateY(40px);
    }

    to{
        opacity:1;
        transform:translateY(0);
    }
}

@keyframes slideTop {

    from{
        opacity:0;
        transform:translateY(-50px);
    }

    to{
        opacity:1;
        transform:translateY(0);
    }
}

@keyframes float {

    0%{
        transform:translateY(0px);
    }

    50%{
        transform:translateY(-12px);
    }

    100%{
        transform:translateY(0px);
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# FLOATING PARTICLES
# =========================================================

st.markdown("""
<div class="particles">

<span></span>
<span></span>
<span></span>
<span></span>
<span></span>
<span></span>
<span></span>

</div>
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
NEXT GEN <br>
TRANSPORT MANAGEMENT
</div>

<div class="hero-sub">
AI Powered • Smart Logistics • Real-Time Operations
</div>

<div class="hero-desc">

Golden Tamilnadu Transport is an advanced transport broker management platform
built for modern logistics businesses. Manage loads, drivers, vehicles,
analytics, and transport operations with futuristic workflow automation
and intelligent business management systems.

</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# FEATURE CARDS
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("""
    <div class="feature-card">

    <div class="card-icon">📦</div>

    <div class="card-title">
    Smart Load System
    </div>

    <div class="card-text">

    AI-powered load allocation,
    shipment management,
    and automated workflow tracking
    for faster transport operations.

    </div>

    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class="feature-card">

    <div class="card-icon">🚛</div>

    <div class="card-title">
    Fleet Monitoring
    </div>

    <div class="card-text">

    Real-time lorry monitoring,
    driver management,
    GPS operations,
    and logistics coordination.

    </div>

    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown("""
    <div class="feature-card">

    <div class="card-icon">📊</div>

    <div class="card-title">
    Live Business Analytics
    </div>

    <div class="card-text">

    Track transport revenue,
    commissions,
    operational performance,
    and business growth instantly.

    </div>

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# LOGIN BUTTON
# =========================================================

st.markdown("<br><br><br>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1,1,1])

with c2:

    if st.button("🔐 ENTER ADMIN PANEL"):

        with st.spinner("Launching Admin Panel..."):

            time.sleep(1)

            try:

                subprocess.Popen([sys.executable, "login.py"])

                st.success("Admin Login Window Opened Successfully")

            except Exception as e:

                st.error(f"Error Opening Login Window: {e}")

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="bottom-tag">

Driven by Innovation • Powered by Intelligence

</div>
""", unsafe_allow_html=True)