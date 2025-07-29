import re
from src import Route, WayPt
import streamlit as st


st.title("KML-to-GPX File Converter")
st.markdown("""
Upload one or many KML files from Google Maps to have them converted to GPX format for import into GPS Devices
""")

uploaded_files = st.file_uploader("Choose one or more KML files.", type=["kml"], accept_multiple_files=True)
if uploaded_files is not None:
    st.write("File(s) uploaded:", uploaded_file.name)
    for kml in uploaded_files:
        try:
            content = kml.read().decode("utf-8")
            #doc_name
            #Identify Placemarks: Record name, Point or Linestring, and Coordinate Array into appropriate class
            placemarks = re.findall(f're.escape()')


