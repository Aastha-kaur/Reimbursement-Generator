# utils/maps.py
import urllib.parse

def generate_google_maps_link(from_address, to_address):
    origin = urllib.parse.quote(from_address)
    destination = urllib.parse.quote(to_address)
    return f"https://www.google.com/maps/dir/{origin}/{destination}"
