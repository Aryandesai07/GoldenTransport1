import streamlit as st

# Page setup
st.set_page_config(page_title="GoldenTransport1", page_icon="🚚", layout="wide")

st.title("Golden TamilNadu Transport")
st.subheader("Shonandh Gounder")

# Example dynamic content
col1, col2, col3 = st.columns(3)
col1.metric("Vehicles", "12 Active")
col2.metric("Orders", "45 Pending")
col3.metric("Revenue", "₹1.2M")

st.success("This is your first dynamic Streamlit app!")
