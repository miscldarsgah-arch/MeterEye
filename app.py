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
        with open("readings.csv", "a") as f:
            f.write(f"{uploaded.name},{units},{max_demand}\n")
        st.success("Saved locally! (Will sync to Sheet)")
