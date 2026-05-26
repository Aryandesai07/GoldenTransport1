import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Golden Tamilnadu Transport Broker System",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

/* Background */

.stApp {
    background:
    linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)),
    url("https://images.unsplash.com/photo-1519003722824-194d4455a60c");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Hide Streamlit */

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Header */

.main-header {
    background: rgba(0,0,0,0.55);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(12px);
    margin-bottom: 25px;
}

.company-title {
    font-size: 50px;
    font-weight: 800;
    text-align: center;
    color: #FFD700;
}

.company-sub {
    text-align: center;
    color: white;
    font-size: 22px;
    margin-top: 10px;
}

/* Glass Cards */

.glass-card {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.15);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    transition: 0.4s;
    margin-bottom: 20px;
}

.glass-card:hover {
    transform: translateY(-8px);
    background: rgba(255,215,0,0.15);
}

.card-title {
    color: #FFD700;
    font-size: 26px;
    font-weight: bold;
}

.card-text {
    color: white;
    margin-top: 12px;
    font-size: 16px;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.80);
}

section[data-testid="stSidebar"] * {
    color: white;
}

/* Footer */

.footer {
    text-align:center;
    color: rgba(255,255,255,0.5);
    margin-top:50px;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="main-header">

<div class="company-title">
🚛 Golden Tamilnadu Transport
</div>

<div class="company-sub">
Owner: Shonandh Gounder <br>
Smart Broker Management System for Lorry Transport & Load Handling
</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR MENU
# =========================================================

menu = st.sidebar.radio(
    "📌 Navigation",
    [
        "🏠 Home",
        "📦 Load Booking",
        "🚛 Driver & Lorry Management",
        "📍 Live Load Tracking",
        "💰 Broker Payments",
        "📊 Business Reports",
        "⚙️ Admin Dashboard"
    ]
)

# =========================================================
# SAMPLE DATA
# =========================================================

cities = [
    "Chennai",
    "Salem",
    "Erode",
    "Madurai",
    "Coimbatore",
    "Trichy",
    "Vellore",
    "Tirunelveli"
]

drivers = [
    "Ramesh",
    "Suresh",
    "Kumar",
    "Vijay",
    "Arun",
    "Dinesh"
]

lorries = [
    "Ashok Leyland",
    "Tata Truck",
    "Eicher Pro",
    "BharatBenz",
    "Mahindra Blazo"
]

# =========================================================
# HOME PAGE
# =========================================================

if menu == "🏠 Home":

    st.markdown("## 🚛 Business Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Today's Loads", "145", "+18")

    with col2:
        st.metric("Available Lorries", "62", "+5")

    with col3:
        st.metric("Active Drivers", "48", "+3")

    with col4:
        st.metric("Broker Revenue", "₹2.8L", "+14%")

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="glass-card">
        <div class="card-title">📦 Load Management</div>
        <div class="card-text">
        Manage transport loads from clients and assign them to lorry drivers instantly.
        </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="glass-card">
        <div class="card-title">🚛 Lorry Assignment</div>
        <div class="card-text">
        Assign available lorries and drivers for every transport order efficiently.
        </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="glass-card">
        <div class="card-title">💰 Broker Earnings</div>
        <div class="card-text">
        Track broker commission, payment collection, and transport billing reports.
        </div>
        </div>
        """, unsafe_allow_html=True)

    st.image(
        "https://images.unsplash.com/photo-1601584115197-04ecc0da31d7",
        use_container_width=True
    )

# =========================================================
# LOAD BOOKING
# =========================================================

elif menu == "📦 Load Booking":

    st.markdown("## 📦 Create New Load Booking")

    with st.form("load_form"):

        col1, col2 = st.columns(2)

        with col1:

            client = st.text_input("Client Name")
            pickup = st.selectbox("Pickup Location", cities)
            material = st.text_input("Material Type")

        with col2:

            drop = st.selectbox("Drop Location", cities)
            weight = st.number_input("Load Weight (Ton)", 1, 100)
            price = st.number_input("Transport Price ₹", 1000, 500000)

        submit = st.form_submit_button("Generate Load")

    if submit:

        load_id = f"LOAD-{random.randint(10000,99999)}"

        assigned_driver = random.choice(drivers)
        assigned_lorry = random.choice(lorries)

        st.success("Load Assigned Successfully")

        st.markdown(f"""
        <div class="glass-card">

        <div class="card-title">
        ✅ Load Booking Generated
        </div>

        <div class="card-text">

        Load ID: {load_id}<br><br>

        Client: {client}<br><br>

        Route: {pickup} ➜ {drop}<br><br>

        Material: {material}<br><br>

        Weight: {weight} Ton<br><br>

        Assigned Driver: {assigned_driver}<br><br>

        Assigned Lorry: {assigned_lorry}<br><br>

        Total Amount: ₹{price}

        </div>

        </div>
        """, unsafe_allow_html=True)

# =========================================================
# DRIVER & LORRY MANAGEMENT
# =========================================================

elif menu == "🚛 Driver & Lorry Management":

    st.markdown("## 🚛 Driver & Vehicle Management")

    records = []

    for i in range(10):

        records.append({
            "Driver": random.choice(drivers),
            "Lorry": random.choice(lorries),
            "Vehicle Number": f"TN-{random.randint(10,99)}-{random.randint(1000,9999)}",
            "Current City": random.choice(cities),
            "Availability": random.choice([
                "Available",
                "On Load",
                "Maintenance"
            ])
        })

    st.dataframe(
        pd.DataFrame(records),
        use_container_width=True
    )

# =========================================================
# LIVE LOAD TRACKING
# =========================================================

elif menu == "📍 Live Load Tracking":

    st.markdown("## 📍 Live Transport Tracking")

    tracking = []

    for i in range(12):

        tracking.append({
            "Load ID": f"LOAD-{random.randint(10000,99999)}",
            "Driver": random.choice(drivers),
            "Current Location": random.choice(cities),
            "Status": random.choice([
                "Loading",
                "In Transit",
                "Delivered",
                "Delayed"
            ]),
            "Speed": f"{random.randint(45,90)} km/h"
        })

    st.dataframe(
        pd.DataFrame(tracking),
        use_container_width=True
    )

    st.map(pd.DataFrame({
        "lat": [13.0827, 11.0168, 9.9252, 10.7905],
        "lon": [80.2707, 76.9558, 78.1198, 78.7047]
    }))

# =========================================================
# BROKER PAYMENTS
# =========================================================

elif menu == "💰 Broker Payments":

    st.markdown("## 💰 Broker Payment & Commission")

    payments = []

    for i in range(10):

        amount = random.randint(10000,90000)
        commission = int(amount * 0.08)

        payments.append({
            "Invoice": f"INV-{random.randint(1000,9999)}",
            "Client": random.choice([
                "RK Traders",
                "South Cargo",
                "National Logistics"
            ]),
            "Transport Amount": f"₹{amount}",
            "Broker Commission": f"₹{commission}",
            "Status": random.choice([
                "Paid",
                "Pending",
                "Processing"
            ])
        })

    st.dataframe(
        pd.DataFrame(payments),
        use_container_width=True
    )

# =========================================================
# REPORTS
# =========================================================

elif menu == "📊 Business Reports":

    st.markdown("## 📊 Transport Business Reports")

    report_data = pd.DataFrame({
        "Day": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
        "Loads": [45,52,60,70,85,95,110]
    })

    st.line_chart(report_data.set_index("Day"))

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Monthly Loads", "3,250", "+22%")

    with col2:
        st.metric("Monthly Revenue", "₹48L", "+18%")

# =========================================================
# ADMIN DASHBOARD
# =========================================================

elif menu == "⚙️ Admin Dashboard":

    st.markdown("## ⚙️ Broker Admin Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Registered Drivers", "86")

    with col2:
        st.metric("Lorries Active", "72")

    with col3:
        st.metric("Pending Loads", "18")

    st.markdown("---")

    logs = []

    for i in range(12):

        logs.append({
            "Time": (
                datetime.now() -
                timedelta(minutes=i*7)
            ).strftime("%H:%M:%S"),

            "Activity": random.choice([
                "New Load Created",
                "Lorry Assigned",
                "Payment Received",
                "Driver Updated",
                "Load Delivered"
            ])
        })

    st.table(pd.DataFrame(logs))

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

Golden Tamilnadu Transport © 2026 <br>
Driven by Trust • Powered by Technology

</div>
""", unsafe_allow_html=True)