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

    <div class="highway">

        <div class="road-lines"></div>

        <div class="smoke smoke1"></div>
        <div class="smoke smoke2"></div>
        <div class="smoke smoke3"></div>

        <div class="truck">
            🚚
        </div>

    </div>

    <div class="loading-title">
        GOLDEN TAMILNADU TRANSPORT
    </div>

    <div class="loading-sub">
        Initializing Smart Logistics System...
    </div>

    <div class="loading-bar">

        <div class="loading-progress"></div>

    </div>

</div>

<style>

#loader{

    position:fixed;
    top:0;
    left:0;

    width:100%;
    height:100%;

    background:
    linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92)),
    url('https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?q=80&w=1920');

    background-size:cover;
    background-position:center;

    z-index:999999;

    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;

    overflow:hidden;

    animation:hideLoader 6s forwards;
    animation-delay:5s;
}

/* =====================================================
HIGHWAY
===================================================== */

.highway{

    position:relative;

    width:85%;
    height:180px;

    overflow:hidden;
}

/* =====================================================
ROAD
===================================================== */

.road-lines{

    position:absolute;
    bottom:25px;

    width:300%;
    height:12px;

    background:
    repeating-linear-gradient(
        to right,
        #FFD700 0px,
        #FFD700 100px,
        transparent 100px,
        transparent 180px
    );

    animation:roadMove 2s linear infinite;
}

/* =====================================================
TRUCK
===================================================== */

.truck{

    position:absolute;

    bottom:40px;
    left:-250px;

    font-size:130px;

    animation:truckMove 5s ease-in-out forwards;

    filter:drop-shadow(0px 0px 25px #FFD700);
}

/* =====================================================
SMOKE
===================================================== */

.smoke{

    position:absolute;

    width:25px;
    height:25px;

    background:rgba(255,255,255,0.25);

    border-radius:50%;

    bottom:85px;

    left:120px;

    animation:smoke 3s infinite;
}

.smoke2{
    animation-delay:1s;
}

.smoke3{
    animation-delay:2s;
}

/* =====================================================
TITLE
===================================================== */

.loading-title{

    color:#FFD700;

    font-size:62px;

    font-weight:900;

    margin-top:50px;

    letter-spacing:4px;

    text-shadow:0px 0px 25px #FFD700;

    animation:pulse 2s infinite;
}

.loading-sub{

    color:white;

    font-size:24px;

    margin-top:20px;
}

/* =====================================================
LOADING BAR
===================================================== */

.loading-bar{

    width:420px;
    height:16px;

    background:rgba(255,255,255,0.1);

    border-radius:30px;

    margin-top:35px;

    overflow:hidden;

    border:1px solid rgba(255,215,0,0.3);
}

.loading-progress{

    width:0%;
    height:100%;

    background:linear-gradient(90deg,#FFD700,#ff9d00);

    animation:loadProgress 5s forwards;

    box-shadow:0px 0px 20px #FFD700;
}

/* =====================================================
MAIN PAGE DESIGN
===================================================== */

html, body, [class*="css"] {

    font-family:'Segoe UI', sans-serif;
}

/* =====================================================
BACKGROUND
===================================================== */

.stApp {

    background:
    linear-gradient(rgba(0,0,0,0.82), rgba(0,0,0,0.85)),
    url("https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?q=80&w=1920");

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
PARTICLES
===================================================== */

.particles{

    position:fixed;
    top:0;
    left:0;

    width:100%;
    height:100%;

    z-index:-1;

    overflow:hidden;
}

.particles span{

    position:absolute;

    width:6px;
    height:6px;

    background:#FFD700;

    border-radius:50%;

    animation:particle 15s linear infinite;

    bottom:-150px;
}

.particles span:nth-child(1){
left:10%;
animation-duration:10s;
}

.particles span:nth-child(2){
left:20%;
animation-duration:15s;
}

.particles span:nth-child(3){
left:35%;
animation-duration:11s;
}

.particles span:nth-child(4){
left:50%;
animation-duration:18s;
}

.particles span:nth-child(5){
left:65%;
animation-duration:12s;
}

.particles span:nth-child(6){
left:80%;
animation-duration:14s;
}

.particles span:nth-child(7){
left:90%;
animation-duration:20s;
}

/* =====================================================
TOP HEADER
===================================================== */

.top-header{

    display:flex;
    justify-content:space-between;
    align-items:center;

    background:rgba(0,0,0,0.45);

    padding:25px 40px;

    border-radius:22px;

    backdrop-filter:blur(10px);

    border:1px solid rgba(255,215,0,0.2);

    margin-bottom:50px;

    animation:fadeUp 1.5s ease;
}

.logo{

    color:#FFD700;

    font-size:38px;

    font-weight:900;

    text-shadow:0px 0px 15px #FFD700;
}

.owner{

    color:white;

    font-size:18px;
}

/* =====================================================
HERO SECTION
===================================================== */

.hero{

    text-align:center;

    padding-top:90px;
    padding-bottom:80px;

    animation:fadeUp 2s ease;
}

.hero-title{

    color:white;

    font-size:88px;

    font-weight:900;

    line-height:1.2;
}

.hero-sub{

    color:#FFD700;

    font-size:32px;

    margin-top:25px;

    font-weight:700;
}

.hero-desc{

    color:#e0e0e0;

    font-size:20px;

    margin-top:35px;

    line-height:1.9;

    padding-left:150px;
    padding-right:150px;
}

/* =====================================================
FEATURE CARDS
===================================================== */

.feature-card{

    background:rgba(20,20,20,0.78);

    border:1px solid rgba(255,215,0,0.2);

    border-radius:25px;

    padding:35px;

    text-align:center;

    height:330px;

    transition:0.4s;

    backdrop-filter:blur(12px);

    animation:fadeUp 2.5s ease;
}

.feature-card:hover{

    transform:translateY(-12px);

    box-shadow:0px 0px 25px rgba(255,215,0,0.3);

    border:1px solid #FFD700;
}

.card-icon{

    font-size:65px;

    animation:float 3s infinite ease-in-out;
}

.card-title{

    color:#FFD700;

    font-size:30px;

    font-weight:bold;

    margin-top:18px;
}

.card-text{

    color:white;

    margin-top:18px;

    line-height:1.8;

    font-size:16px;
}

/* =====================================================
BUTTON
===================================================== */

.stButton > button{

    background:linear-gradient(45deg,#FFD700,#ffb300);

    color:black;

    border:none;

    border-radius:14px;

    font-size:22px;

    font-weight:bold;

    padding:16px 45px;

    transition:0.4s;

    width:100%;

    box-shadow:0px 0px 20px rgba(255,215,0,0.4);
}

.stButton > button:hover{

    background:white;

    transform:scale(1.05);

    box-shadow:0px 0px 30px white;
}

/* =====================================================
FOOTER
===================================================== */

.bottom-tag{

    text-align:center;

    color:rgba(255,255,255,0.55);

    margin-top:90px;

    font-size:24px;

    letter-spacing:2px;

    font-style:italic;
}

/* =====================================================
ANIMATIONS
===================================================== */

@keyframes truckMove{

    0%{
        left:-250px;
    }

    100%{
        left:110%;
    }
}

@keyframes roadMove{

    0%{
        transform:translateX(0);
    }

    100%{
        transform:translateX(-50%);
    }
}

@keyframes smoke{

    0%{
        transform:translate(0,0) scale(1);
        opacity:0.5;
    }

    100%{
        transform:translate(-100px,-80px) scale(2.5);
        opacity:0;
    }
}

@keyframes pulse{

    0%{
        opacity:0.6;
    }

    50%{
        opacity:1;
    }

    100%{
        opacity:0.6;
    }
}

@keyframes loadProgress{

    0%{
        width:0%;
    }

    100%{
        width:100%;
    }
}

@keyframes hideLoader{

    to{
        opacity:0;
        visibility:hidden;
    }
}

@keyframes fadeUp{

    from{
        opacity:0;
        transform:translateY(40px);
    }

    to{
        opacity:1;
        transform:translateY(0px);
    }
}

@keyframes float{

    0%{
        transform:translateY(0px);
    }

    50%{
        transform:translateY(-10px);
    }

    100%{
        transform:translateY(0px);
    }
}

@keyframes particle{

    0%{
        transform:translateY(0);
        opacity:0;
    }

    10%{
        opacity:1;
    }

    100%{
        transform:translateY(-1000px);
        opacity:0;
    }
}

</style>
"""

# =========================================================
# SHOW LOADING HTML
# =========================================================

components.html(loading_html, height=0)

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
    shipment tracking,
    and smart workflow management.

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

    Monitor vehicles,
    drivers,
    GPS operations,
    and transport coordination.

    </div>

    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown("""
    <div class="feature-card">

    <div class="card-icon">📊</div>

    <div class="card-title">
    Live Analytics
    </div>

    <div class="card-text">

    Track transport revenue,
    broker commissions,
    and business growth in real time.

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