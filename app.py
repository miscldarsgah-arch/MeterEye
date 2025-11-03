import streamlit as st
import cv2, pytesseract, re, tempfile, numpy as np

st.set_page_config(page_title="MeterEye", page_icon="📟")
st.title("📟 MeterEye — Smart Meter Reading Extractor")
st.write("Upload your meter video to automatically extract readings using OCR.")

uploaded = st.file_uploader("Upload meter video", type=["mp4", "mov", "avi"])
if uploaded:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded.read())
    cap = cv2.VideoCapture(tfile.name)
    frame_interval = 30  # read every 30th frame
    readings = []

    st.info("Processing video... Please wait 1–2 minutes.")
    i = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if i % frame_interval == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)
            if text.strip():
                readings.append(text)
        i += 1
    cap.release()

    full_text = "\n".join(readings)

    # Extract key values
    units = re.findall(r"([\d\.]+)\s*kWh", full_text)
    md = re.findall(r"([\d\.]+)\s*kW", full_text)
    phases = re.findall(r"(R|Y|B)\s*:?[\s]*([\d\.]+)", full_text)

    st.subheader("📋 Extracted Readings")
    st.write("**Energy Consumption (kWh):**", units[-1] if units else "Not found")
    st.write("**Maximum Demand (kW):**", md[-1] if md else "Not found")
    if phases:
        st.write("**Phase-wise Data:**")
        for p, v in phases:
            st.write(f"{p} Phase → {v}")
    st.text_area("🧾 Raw Detected Text", full_text, height=200)
