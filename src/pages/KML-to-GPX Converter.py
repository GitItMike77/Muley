import streamlit as st
from dataclasses import dataclass
from typing import List, Optional
import xml.etree.ElementTree as ET


@dataclass
class Route:
    name: str
    description: Optional[str]
    coordinates: List[List[float]]



@dataclass
class WayPt:
    name: str
    description: Optional[str]
    coordinates: List[float]

def get_routes_from_kml(kml_str: str) -> List[Route]:
    root = ET.fromstring(kml_str)
    routes = []

    for placemark in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
        # .// means recursive search, finds all descendants with the tag.
        if placemark.find('.//{http://www.opengis.net/kml/2.2}LineString') is not None:
            # Placemark is presumed to be a route
            name = placemark.find('.//{http://www.opengis.net/kml/2.2}name')
            if name.text == '':
                name = 'Unnamed Route'
            desc = name
            coords = []

            for coord in placemark.findall('.//{http://www.opengis.net/kml/2.2}coordinates'):
                if coord is not None:
                    coord_str = coord.text
                    coord_line = coord_str.splitlines()
                    for elem in coord_line:
                        if elem != '':
                            coord_arr = elem.strip().split(',')
                            if len(coord_arr) == 3:
                                lat = float(coord_arr[1])
                                lon = float(coord_arr[0])
                                coords.append([lat, lon])
                            # else:
                                # st.error(coord_arr)

            route = Route(name.text, desc.text, coords)
            routes.append(route)

        else:
            continue

    return routes


def get_waypts_from_kml(kml_str: str) -> List[WayPt]:
    root = ET.fromstring(kml_str)
    points = []

    for placemark in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
        if placemark.find('.//{http://www.opengis.net/kml/2.2}Point') is not None:
            # Placemark is presumed to be a waypoint
            name = placemark.find('.//{http://www.opengis.net/kml/2.2}name')
            if name.text == '':
                name = 'Unnamed Point'
            desc = name
            coord_str = placemark.find('.//{http://www.opengis.net/kml/2.2}coordinates')
            # st.text_area('coord_str', coord_str.text)
            coord_arr = coord_str.text.split(',')
            lat = float(coord_arr[1])
            lon = float(coord_arr[0])
            coord = [lat, lon]

            point = WayPt(name.text, desc.text, coord)
            points.append(point)

        else:
            continue

    return points

def write_gpx(routes: List[Route], waypts: List[WayPt]) -> str:
    gpx_str = '<gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd" version="1.1" creator="Mad at Em Hunt Planner">'
    for wpt in waypts:
        wpt_str = f'<wpt lat="{wpt.coordinates[0]}" lon="{wpt.coordinates[1]}"><name>{wpt.name}</name></wpt>'
        gpx_str = gpx_str + wpt_str
    for rte in routes:
        rte_str = f'<rte><name>{rte.name}</name><type>Line</type>'
        for rtept in rte.coordinates:
            rte_str = rte_str + f'<rtept lat="{rtept[0]}" lon="{rtept[1]}"/>'
        gpx_str = gpx_str + rte_str + '</rte>'
    return gpx_str + '</gpx>'


# Main Streamlit Page

if 'filename' not in st.session_state:
    st.session_state['filename']=''

st.title("KML-to-GPX File Converter")
st.markdown("""
Upload one or more KML files from Google Maps to have them converted to GPX format for import into GPS Devices
""")
oWayPts = []
oRoutes = []

uploaded_files = st.file_uploader("Choose one or more KML files.", type=["kml"], accept_multiple_files=True)
if uploaded_files:
    for kml in uploaded_files:
        kml_str: str = kml.read().decode('utf-8')
        try:
            oWayPts.extend(get_waypts_from_kml(kml_str))
        except Exception as e:
            st.error('An error occurred trying to extract waypoints.\n')
            st.exception(e)
        try:
            oRoutes.extend(get_routes_from_kml(kml_str))
        except Exception as e:
            st.error('An error occurred trying to extract routes.\n')
            st.exception(e)

    stats = st.container(border=True)
    stats.write('Data Harvest')
    stcol1, stcol2 = stats.columns(2)
    with stcol1:
        st.metric(label='Waypoints Found',
                  value=len(oWayPts))
    with stcol2:
        st.metric(label='Routes Found',
                  value=len(oRoutes))

    filename = st.text_input('Enter Filename',
                             value=st.session_state.get('filename'),
                             key='filename_input')
    st.session_state['filename'] = filename
    if filename.strip():
        st.download_button(
            label='Download GPX File',
            data=write_gpx(routes=oRoutes,
                           waypts=oWayPts),
            mime='text/gpx',
            file_name=filename + '.gpx',
            type='primary',
            icon=':material/download:')
