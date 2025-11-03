import requests
import json
SHEET_WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyCXcakkA0QUntf-a00AHOEUg8hgsw7daAvAX0rE7u5SAYNiAL8Mrcprl2lmfXkPbf8/exec"
import streamlit as st
from PIL import Image
import pytesseract
import re
import io
import numpy as np

st.set_page_config(page_title="MeterEye Dashboard", page_icon="⚡", layout="wide")

st.title("⚡ MeterEye – Smart Meter Reading Extractor")

uploaded = st.file_uploader("Upload meter image (JPG/PNG)", type=["jpg", "jpeg", "png"])
if uploaded:
    image = Image.open(uploaded)
    st.image(image, caption="Uploaded Meter Image", use_container_width=True)

    # OCR text extraction
    text = pytesseract.image_to_string(image)

    # Try to pick useful readings
    units = re.findall(r"[\d]+\.\d+\s?kWh", text)
    max_demand = re.findall(r"[\d]+\.\d+\s?kW", text)

    st.subheader("📄 Raw OCR Text")
    st.text(text)

    st.subheader("🔍 Extracted Readings")
    st.write({
        "Units (kWh)": units[0] if units else "Not detected",
        "Max Demand (kW)": max_demand[0] if max_demand else "Not detected"
    })

    # Save to CSV (for Sheet sync later)
    if st.button("Save Reading"):
    payload = {
        "fileName": uploaded.name if uploaded is not None else "",
        "units": (units[0] if isinstance(units, list) and units else "") ,
        "maxDemand": (max_demand[0] if isinstance(max_demand, list) and max_demand else "")
    }
    try:
        r = requests.post(SHEET_WEB_APP_URL, json=payload, timeout=15)
        if r.status_code == 200:
            # Apps Script returns "Success" (or 200) on success
            st.success("✅ Reading saved to Google Sheet!")
        else:
            st.error(f"⚠️ Failed to save. Server returned {r.status_code}")
            st.write(r.text)
    except requests.exceptions.Timeout:
        st.error("⚠️ Request timed out. Check your network or Apps Script URL.")
    except Exception as e:
        st.error(f"Error while saving: {e}")

