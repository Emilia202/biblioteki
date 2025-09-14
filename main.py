from tkinter import *
from tkinter import ttk
import tkintermapview
import requests

# logowanie
valid_users = {
    "admin": "admin123",
    "user": "user123",
    "": ""
}

biblioteki = []
wszystkie_markery = []

class Biblioteka:
    def __init__(self, name, city, street):
        self.name = name
        self.city = city
        self.street = street
        self.coordinates = self.get_coordinates()
        self.marker = None
        if self.coordinates:
            self.marker = map_widget.set_marker(*self.coordinates, text=self.name)
            wszystkie_markery.append(self.marker)
        self.pracownicy = []
        self.klienci = []

    def get_coordinates(self):
        try:
            url = "https://nominatim.openstreetmap.org/search"
            query = f"{self.street}, {self.city}" if self.street else self.city
            params = {"q": query, "format": "json"}
            headers = {"User-Agent": "BibliotekaApp/1.0"}
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            if data:
                return [float(data[0]["lat"]), float(data[0]["lon"])]
            return None
        except Exception as e:
            print("Błąd geokodowania:", e)
            return None


class Pracownik:
    def __init__(self, name, biblioteka, city=None, street=None):
        self.name = name
        self.biblioteka = biblioteka
        self.city = city
        self.street = street
        self.coordinates = self.get_coordinates()
        self.marker = None
        if self.coordinates:
            self.marker = map_widget.set_marker(*self.coordinates, text=self.name)
            wszystkie_markery.append(self.marker)

    def get_coordinates(self):
        try:
            if not self.city and not self.street:
                # domyślnie bierzemy adres biblioteki
                return self.biblioteka.coordinates
            url = "https://nominatim.openstreetmap.org/search"
            query = f"{self.street}, {self.city}" if self.street else self.city
            params = {"q": query, "format": "json"}
            headers = {"User-Agent": "BibliotekaApp/1.0"}
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            if data:
                return [float(data[0]["lat"]), float(data[0]["lon"])]
            return self.biblioteka.coordinates
        except Exception as e:
            print("Błąd geokodowania pracownika:", e)
            return self.biblioteka.coordinates


class Klient:
    def __init__(self, name, biblioteka, city=None, street=None):
        self.name = name
        self.biblioteka = biblioteka
        self.city = city
        self.street = street
        self.coordinates = self.get_coordinates()
        self.marker = None
        if self.coordinates:
            self.marker = map_widget.set_marker(*self.coordinates, text=self.name)
            wszystkie_markery.append(self.marker)

    def get_coordinates(self):
        try:
            if not self.city and not self.street:
                return self.biblioteka.coordinates
            url = "https://nominatim.openstreetmap.org/search"
            query = f"{self.street}, {self.city}" if self.street else self.city
            params = {"q": query, "format": "json"}
            headers = {"User-Agent": "BibliotekaApp/1.0"}
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            if data:
                return [float(data[0]["lat"]), float(data[0]["lon"])]
            return self.biblioteka.coordinates
        except Exception as e:
            print("Błąd geokodowania klienta:", e)
            return self.biblioteka.coordinates
