import streamlit as st
import requests
import datetime

# --- Page Config ---
st.set_page_config(page_title="MeterEye Dashboard", page_icon="⚡", layout="wide")

# --- Title ---
st.title("⚡ MeterEye - Smart Electricity Reading Dashboard")

# --- Sidebar ---
st.sidebar.header("📊 Input Panel")

# Input fields
meter_id = st.sidebar.text_input("Meter ID", "")
reading = st.sidebar.number_input("Current Reading (kWh)", min_value=0.0, step=0.1)
remarks = st.sidebar.text_area("Remarks", "")

# Submit button
if st.sidebar.button("💾 Save Reading"):
    if meter_id and reading > 0:
        # Google Apps Script URL (👇 यही तुम्हारे Apps Script से मिला हुआ URL डालो)
        script_url = "https://script.google.com/macros/s/AKfycbyCXcakkA0QUntf-a00AHOEUg8hgsw7daAvAX0rE7u5SAYNiAL8Mrcprl2lmfXkPbf8/exec"

        payload = {
            "MeterID": meter_id,
            "Reading": reading,
            "Remarks": remarks,
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            response = requests.post(script_url, data=payload)
            if response.status_code == 200:
                st.success("✅ Reading saved successfully!")
            else:
                st.error(f"❌ Failed to save reading. Error code: {response.status_code}")
        except Exception as e:
            st.error(f"⚠️ Connection error: {e}")
    else:
        st.warning("Please fill Meter ID and Reading properly!")

# --- Data Display Section ---
st.subheader("📈 Recent Readings")

st.info("यह सेक्शन Google Sheet से auto-load किया जाएगा (Next Step में)।")
