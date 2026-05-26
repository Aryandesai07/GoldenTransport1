import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Golden Tamilnadu Transport",
    page_icon="🚌",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f7fa;
    }

    .title {
        text-align: center;
        color: #d62828;
        font-size: 45px;
        font-weight: bold;
    }

    .sub-title {
        text-align: center;
        color: #264653;
        font-size: 20px;
        margin-bottom: 20px;
    }

    .card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }

    .success-box {
        background-color: #d8f3dc;
        padding: 15px;
        border-radius: 10px;
        color: #1b4332;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# TITLE SECTION
# ==========================================
st.markdown("<div class='title'>🚌 Golden Tamilnadu Transport</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Smart & Dynamic Transport Booking System</div>", unsafe_allow_html=True)

# ==========================================
# SIDEBAR MENU
# ==========================================
menu = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Book Ticket",
        "Live Bus Status",
        "Bus Timetable",
        "Passenger Details",
        "Admin Dashboard"
    ]
)

# ==========================================
# SAMPLE BUS DATA
# ==========================================
locations = [
    "Chennai",
    "Coimbatore",
    "Madurai",
    "Salem",
    "Trichy",
    "Erode",
    "Tirunelveli",
    "Vellore",
    "Thoothukudi",
    "Kanyakumari"
]

bus_names = [
    "Golden Express",
    "Tamil Star",
    "Royal Rider",
    "Fast King",
    "Super Deluxe",
    "Night Queen",
    "Southern Arrow",
    "Premium Rider"
]

# ==========================================
# HOME PAGE
# ==========================================
if menu == "Home":

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Daily Passengers", "12,540", "+12%")

    with col2:
        st.metric("Buses Running", "485", "+18")

    with col3:
        st.metric("Routes Available", "120", "+6")

    st.markdown("---")

    st.subheader("🚍 Available Premium Services")

    services = pd.DataFrame({
        "Service": [
            "AC Sleeper",
            "Non-AC Sleeper",
            "Luxury Coach",
            "Semi Sleeper",
            "Express Service"
        ],
        "Availability": ["Available", "Available", "Limited", "Available", "Available"],
        "Average Fare": [1200, 800, 1500, 950, 700]
    })

    st.dataframe(services, use_container_width=True)

    st.image(
        "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957",
        use_container_width=True
    )

# ==========================================
# BOOK TICKET PAGE
# ==========================================
elif menu == "Book Ticket":

    st.subheader("🎫 Book Your Ticket")

    with st.form("booking_form"):

        col1, col2 = st.columns(2)

        with col1:
            source = st.selectbox("Select Source", locations)
            travel_date = st.date_input("Journey Date")
            passengers = st.number_input("Number of Passengers", 1, 10, 1)

        with col2:
            destination = st.selectbox("Select Destination", locations)
            bus_type = st.selectbox(
                "Bus Type",
                [
                    "AC Sleeper",
                    "Non-AC Sleeper",
                    "Luxury Coach",
                    "Semi Sleeper"
                ]
            )

            seat_type = st.radio(
                "Seat Preference",
                ["Window", "Middle", "Aisle"]
            )

        submit = st.form_submit_button("Search Buses")

    if submit:

        if source == destination:
            st.error("Source and Destination cannot be same.")

        else:

            st.success("Available buses found successfully!")

            available_buses = []

            for i in range(5):
                bus = {
                    "Bus Name": random.choice(bus_names),
                    "Departure": f"{random.randint(1,12)}:{random.choice(['00','15','30','45'])} {'AM' if random.randint(0,1)==0 else 'PM'}",
                    "Arrival": f"{random.randint(1,12)}:{random.choice(['00','15','30','45'])} {'AM' if random.randint(0,1)==0 else 'PM'}",
                    "Fare": random.randint(500, 1800),
                    "Seats Available": random.randint(5, 40)
                }

                available_buses.append(bus)

            bus_df = pd.DataFrame(available_buses)

            st.dataframe(bus_df, use_container_width=True)

            selected_bus = st.selectbox(
                "Select Bus",
                bus_df["Bus Name"]
            )

            if st.button("Confirm Booking"):

                booking_id = f"GTN{random.randint(10000,99999)}"

                st.markdown(
                    f"""
                    <div class='success-box'>
                    ✅ Booking Confirmed Successfully!<br><br>
                    Booking ID: {booking_id}<br>
                    Passenger Count: {passengers}<br>
                    Route: {source} ➜ {destination}<br>
                    Bus: {selected_bus}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# ==========================================
# LIVE BUS STATUS PAGE
# ==========================================
elif menu == "Live Bus Status":

    st.subheader("📍 Live Bus Tracking")

    live_buses = []

    for i in range(10):
        live_buses.append({
            "Bus Number": f"TN-{random.randint(10,99)}-{random.randint(1000,9999)}",
            "Bus Name": random.choice(bus_names),
            "Current Location": random.choice(locations),
            "Speed (km/h)": random.randint(40, 100),
            "Status": random.choice(["On Time", "Delayed", "Arriving Soon"])
        })

    live_df = pd.DataFrame(live_buses)

    st.dataframe(live_df, use_container_width=True)

    st.map(pd.DataFrame({
        'lat': [13.0827, 11.0168, 9.9252, 10.7905],
        'lon': [80.2707, 76.9558, 78.1198, 78.7047]
    }))

# ==========================================
# BUS TIMETABLE PAGE
# ==========================================
elif menu == "Bus Timetable":

    st.subheader("⏰ Bus Timetable")

    timetable = []

    current_time = datetime.now()

    for i in range(15):

        departure = current_time + timedelta(minutes=i * 45)

        timetable.append({
            "Bus": random.choice(bus_names),
            "Route": f"{random.choice(locations)} ➜ {random.choice(locations)}",
            "Departure": departure.strftime("%I:%M %p"),
            "Platform": random.randint(1, 15)
        })

    time_df = pd.DataFrame(timetable)

    st.table(time_df)

# ==========================================
# PASSENGER DETAILS PAGE
# ==========================================
elif menu == "Passenger Details":

    st.subheader("👤 Passenger Information")

    with st.form("passenger_form"):

        name = st.text_input("Passenger Name")
        age = st.number_input("Age", 1, 100, 18)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        mobile = st.text_input("Mobile Number")
        email = st.text_input("Email Address")

        submit_passenger = st.form_submit_button("Save Passenger")

    if submit_passenger:

        st.success("Passenger details saved successfully!")

        passenger_data = {
            "Name": name,
            "Age": age,
            "Gender": gender,
            "Mobile": mobile,
            "Email": email
        }

        st.json(passenger_data)

# ==========================================
# ADMIN DASHBOARD PAGE
# ==========================================
elif menu == "Admin Dashboard":

    st.subheader("📊 Admin Dashboard")

    total_buses = random.randint(400, 600)
    active_routes = random.randint(80, 150)
    bookings_today = random.randint(1000, 4000)
    revenue = random.randint(500000, 2000000)

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"🚌 Total Buses: {total_buses}")
        st.success(f"🛣️ Active Routes: {active_routes}")

    with col2:
        st.warning(f"🎫 Bookings Today: {bookings_today}")
        st.error(f"💰 Revenue Today: ₹{revenue}")

    chart_data = pd.DataFrame({
        "Bookings": [1200, 1800, 2100, 2400, 3000, 3500, 4000],
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    })

    st.line_chart(chart_data.set_index("Day"))

    st.subheader("🚦 System Activity")

    logs = []

    for i in range(8):
        logs.append({
            "Time": (datetime.now() - timedelta(minutes=i*5)).strftime("%H:%M:%S"),
            "Activity": random.choice([
                "New Booking",
                "Ticket Cancelled",
                "Bus Departed",
                "Route Updated",
                "Passenger Registered"
            ])
        })

    st.table(pd.DataFrame(logs))

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.markdown(
    "<center>© 2026 Golden Tamilnadu Transport | Developed with Streamlit 🚍</center>",
    unsafe_allow_html=True
)
