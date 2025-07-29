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


def get_routes_from_kml(file_str: str) -> List[Route]:
    tree = ET.parse(file_str)
    root = tree.getroot()

    routes = []

    for placemark in root.findall('.//Placemark'):  # .// means recursive search, finds all descendants with the tag.
        if placemark.find('LineString') is not None:  # Placemark is presumed to be a route
            name = placemark.findtext('name', default='Unnamed Route')
            desc = placemark.findtext('name', default='Unnamed Route')
            coords = []

            for coord in placemark.findall('coordinates'):  # without the .//, only immediate children to the placemark
                if coord is not None:
                    coord_str = coord.text
                    coord_arr = coord_str.split(',')
                    lat = float(coord_arr[1])
                    lon = float(coord_arr[0])
                    coords.append([lat,lon])

            route = Route(name, desc, coords)
            routes.append(route)

        else:
            continue

    return routes


def get_waypts_from_kml(file_str: str) -> List[WayPt]:
    tree = ET.parse(file_str)
    root = tree.getroot()

    points = []

    for placemark in root.findall('.//Placemark'):
        if placemark.find('Point') is not None:  # Placemark is presumed to be a waypoint
            name = placemark.findtext('name', default='Unnamed Route')
            desc = placemark.findtext('name', default='Unnamed Route')
            coord_str = placemark.findtext('coordinates')
            coord_arr = coord_str.split(',')
            lat = float(coord_arr[1])
            lon = float(coord_arr[0])
            coord = [lat,lon]

            point = WayPt(name, desc, coord)
            points.append(point)

        else:
            continue

    return points


def write_gpx(filename: str, save_to_directory: str, routes: List[Route], waypts: List[WayPt]):
    start_str = '<gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd" version="1.1" creator="Mad at Em Hunt Planner">'
    end_str = '</gpx>'
