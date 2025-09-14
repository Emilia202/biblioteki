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
# markery

def wyczysc_mape():
    for marker in wszystkie_markery:
        marker.delete()
    wszystkie_markery.clear()

def pokaz_wszystkie_biblioteki():
    wyczysc_mape()
    for b in biblioteki:
        b.marker = map_widget.set_marker(*b.coordinates, text=b.name)
        wszystkie_markery.append(b.marker)

# listy
def pokaz_biblioteki():
    listbox_biblioteki.delete(0, END)
    combobox_biblioteki.delete(0, END)
    combobox_biblioteki_klient.delete(0, END)
    for b in biblioteki:
        listbox_biblioteki.insert(END, f'{b.name} ({b.city})')
        combobox_biblioteki.insert(END, f'{b.name} ({b.city})')
        combobox_biblioteki_klient.insert(END, f'{b.name} ({b.city})')
    odswiez_liste_mapa()

def pokaz_pracownikow():
    listbox_pracownicy.delete(0, END)
    for b in biblioteki:
        for p in b.pracownicy:
            listbox_pracownicy.insert(END, f'{p.name} - {b.name}')
    odswiez_liste_mapa()

def pokaz_klientow():
    listbox_klienci.delete(0, END)
    for b in biblioteki:
        for k in b.klienci:
            listbox_klienci.insert(END, f'{k.name} - {b.name}')
    odswiez_liste_mapa()
# biblioteki

def dodaj_biblioteke():
    name = entry_biblioteka_nazwa.get()
    city = entry_biblioteka_miasto.get()
    street = entry_biblioteka_ulica.get()
    if not name or not city:
        return
    b = Biblioteka(name, city, street)
    if b.coordinates is None:
        print("Nie udało się pobrać współrzędnych – biblioteka nie zostanie dodana")
        return
    biblioteki.append(b)
    pokaz_biblioteki()
    entry_biblioteka_nazwa.delete(0, END)
    entry_biblioteka_miasto.delete(0, END)
    entry_biblioteka_ulica.delete(0, END)


def edytuj_biblioteke():
    i = listbox_biblioteki.curselection()
    if not i:
        return
    i = i[0]
    b = biblioteki[i]
    entry_biblioteka_nazwa.delete(0, END)
    entry_biblioteka_nazwa.insert(0, b.name)
    entry_biblioteka_miasto.delete(0, END)
    entry_biblioteka_miasto.insert(0, b.city)
    entry_biblioteka_ulica.delete(0, END)
    entry_biblioteka_ulica.insert(0, b.street)
    button_dodaj_biblioteke.config(text="Zapisz", command=lambda: zapisz_edycje_biblioteki(i))

def zapisz_edycje_biblioteki(i):
    name = entry_biblioteka_nazwa.get()
    city = entry_biblioteka_miasto.get()
    street = entry_biblioteka_ulica.get()
    if not name or not city:
        return
    b = biblioteki[i]
    b.name = name
    b.city = city
    b.street = street
    if b.marker:
        b.marker.delete()
    b.coordinates = b.get_coordinates()
    if b.coordinates:
        b.marker = map_widget.set_marker(*b.coordinates, text=name)
        wszystkie_markery.append(b.marker)
    pokaz_biblioteki()
    button_dodaj_biblioteke.config(text="Dodaj bibliotekę", command=dodaj_biblioteke)
    entry_biblioteka_nazwa.delete(0, END)
    entry_biblioteka_miasto.delete(0, END)
    entry_biblioteka_ulica.delete(0, END)


def usun_biblioteke():
    i = listbox_biblioteki.curselection()
    if not i:
        return
    i = i[0]
    b = biblioteki.pop(i)
    b.marker.delete()
    for p in b.pracownicy:
        p.marker.delete()
    for k in b.klienci:
        k.marker.delete()
    pokaz_biblioteki()
    pokaz_pracownikow()
    pokaz_klientow()

# pracownicy

def dodaj_pracownika():
    name = entry_pracownik_name.get()
    i = combobox_biblioteki.curselection()
    city = entry_pracownik_city.get()
    street = entry_pracownik_street.get()
    if not name or not i:
        return
    biblioteka = biblioteki[i[0]]
    p = Pracownik(name, biblioteka, city, street)
    if p.coordinates is None:
        print("Nie udało się pobrać współrzędnych – pracownik nie zostanie dodany")
        return
    biblioteka.pracownicy.append(p)
    pokaz_pracownikow()
    entry_pracownik_name.delete(0, END)
    entry_pracownik_city.delete(0, END)
    entry_pracownik_street.delete(0, END)


def edytuj_pracownika():
    i = listbox_pracownicy.curselection()
    if not i:
        return
    idx = i[0]
    licznik = 0
    for b in biblioteki:
        for j, p in enumerate(b.pracownicy):
            if licznik == idx:
                entry_pracownik_name.delete(0, END)
                entry_pracownik_name.insert(0, p.name)
                entry_pracownik_city.delete(0, END)
                entry_pracownik_city.insert(0, p.city)
                entry_pracownik_street.delete(0, END)
                entry_pracownik_street.insert(0, p.street)
                combobox_biblioteki.select_set(biblioteki.index(b))
                button_dodaj_pracownika.config(text="Zapisz", command=lambda bibl=b, index=j: zapisz_edycje_pracownika(bibl, index))
                return
            licznik += 1


def zapisz_edycje_pracownika(bibl, index):
    name = entry_pracownik_name.get()
    city = entry_pracownik_city.get()
    street = entry_pracownik_street.get()
    if not name:
        return
    pracownik = bibl.pracownicy[index]
    pracownik.name = name
    pracownik.city = city
    pracownik.street = street
    if pracownik.marker:
        pracownik.marker.delete()
    pracownik.coordinates = pracownik.get_coordinates()
    if pracownik.coordinates:
        pracownik.marker = map_widget.set_marker(*pracownik.coordinates, text=pracownik.name)
        wszystkie_markery.append(pracownik.marker)
    pokaz_pracownikow()
    button_dodaj_pracownika.config(text="Dodaj pracownika", command=dodaj_pracownika)
    entry_pracownik_name.delete(0, END)
    entry_pracownik_city.delete(0, END)
    entry_pracownik_street.delete(0, END)


def usun_pracownika():
    i = listbox_pracownicy.curselection()
    if not i:
        return
    idx = i[0]
    licznik = 0
    for b in biblioteki:
        for j, p in enumerate(b.pracownicy):
            if licznik == idx:
                p.marker.delete()
                b.pracownicy.pop(j)
                pokaz_pracownikow()
                return
            licznik += 1

# klienci

def dodaj_klienta():
    name = entry_klient_name.get()
    i = combobox_biblioteki_klient.curselection()
    city = entry_klient_city.get()
    street = entry_klient_street.get()
    if not name or not i:
        return
    biblioteka = biblioteki[i[0]]
    k = Klient(name, biblioteka, city, street)
    if k.coordinates is None:
        print("Nie udało się pobrać współrzędnych – klient nie zostanie dodany")
        return
    biblioteka.klienci.append(k)
    pokaz_klientow()
    entry_klient_name.delete(0, END)
    entry_klient_city.delete(0, END)
    entry_klient_street.delete(0, END)


def edytuj_klienta():
    i = listbox_klienci.curselection()
    if not i:
        return
    idx = i[0]
    licznik = 0
    for b in biblioteki:
        for j, k in enumerate(b.klienci):
            if licznik == idx:
                entry_klient_name.delete(0, END)
                entry_klient_name.insert(0, k.name)
                entry_klient_city.delete(0, END)
                entry_klient_city.insert(0, k.city)
                entry_klient_street.delete(0, END)
                entry_klient_street.insert(0, k.street)
                combobox_biblioteki_klient.select_set(biblioteki.index(b))
                button_dodaj_klienta.config(text="Zapisz", command=lambda bibl=b, index=j: zapisz_edycje_klienta(bibl, index))
                return
            licznik += 1

def zapisz_edycje_klienta(bibl, index):
    name = entry_klient_name.get()
    city = entry_klient_city.get()
    street = entry_klient_street.get()
    if not name:
        return
    klient = bibl.klienci[index]
    klient.name = name
    klient.city = city
    klient.street = street
    if klient.marker:
        klient.marker.delete()
    klient.coordinates = klient.get_coordinates()
    if klient.coordinates:
        klient.marker = map_widget.set_marker(*klient.coordinates, text=klient.name)
        wszystkie_markery.append(klient.marker)
    pokaz_klientow()
    button_dodaj_klienta.config(text="Dodaj klienta", command=dodaj_klienta)
    entry_klient_name.delete(0, END)
    entry_klient_city.delete(0, END)
    entry_klient_street.delete(0, END)

def usun_klienta():
    i = listbox_klienci.curselection()
    if not i:
        return
    idx = i[0]
    licznik = 0
    for b in biblioteki:
        for j, k in enumerate(b.klienci):
            if licznik == idx:
                k.marker.delete()
                b.klienci.pop(j)
                pokaz_klientow()
                return
            licznik += 1
def pokaz_na_mapie():
    wyczysc_mape()
    wybor = listbox_mapa_wybor.curselection()
    if not wybor:
        return
    wybor = listbox_mapa_wybor.get(wybor[0])

    if wybor == "Biblioteki":
        for b in biblioteki:
            if b.coordinates:
                b.marker = map_widget.set_marker(*b.coordinates, text=b.name)
                wszystkie_markery.append(b.marker)

    elif wybor == "Wszyscy pracownicy":
        for b in biblioteki:
            for p in b.pracownicy:
                if p.coordinates:
                    p.marker = map_widget.set_marker(*p.coordinates, text=p.name)
                    wszystkie_markery.append(p.marker)

    elif wybor == "Wszyscy klienci":
        for b in biblioteki:
            for k in b.klienci:
                if k.coordinates:
                    k.marker = map_widget.set_marker(*k.coordinates, text=k.name)
                    wszystkie_markery.append(k.marker)

    elif wybor.startswith("Pracownicy - "):
        nazwa_biblioteki = wybor.replace("Pracownicy - ", "")
        for b in biblioteki:
            if b.name == nazwa_biblioteki:
                for p in b.pracownicy:
                    if p.coordinates:
                        p.marker = map_widget.set_marker(*p.coordinates, text=p.name)
                        wszystkie_markery.append(p.marker)

    elif wybor.startswith("Klienci - "):
        nazwa_biblioteki = wybor.replace("Klienci - ", "")
        for b in biblioteki:
            if b.name == nazwa_biblioteki:
                for k in b.klienci:
                    if k.coordinates:
                        k.marker = map_widget.set_marker(*k.coordinates, text=k.name)
                        wszystkie_markery.append(k.marker)



def odswiez_liste_mapa():
    listbox_mapa_wybor.delete(0, END)
    listbox_mapa_wybor.insert(END, "Biblioteki")
    listbox_mapa_wybor.insert(END, "Wszyscy pracownicy")
    listbox_mapa_wybor.insert(END, "Wszyscy klienci")

    for b in biblioteki:
        listbox_mapa_wybor.insert(END, f"Pracownicy - {b.name}")
        listbox_mapa_wybor.insert(END, f"Klienci - {b.name}")


# GUI

def show_main_app():
    global root, map_widget
    root = Tk()
    root.geometry("1200x800")
    root.title('System zarządzania bibliotekami')

    # zakładki
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # --- Zakładka 1: Biblioteki ---
    tab_biblioteki = Frame(notebook)
    notebook.add(tab_biblioteki, text="Biblioteki")

    frame_left = Frame(tab_biblioteki)
    frame_left.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

    frame_right = Frame(tab_biblioteki)
    frame_right.pack(side=RIGHT, fill=Y, padx=10, pady=10)

    Label(frame_left, text="Lista bibliotek").pack()
    global listbox_biblioteki
    listbox_biblioteki = Listbox(frame_left, width=50, height=20)
    listbox_biblioteki.pack()
    Button(frame_left, text="Edytuj", command=edytuj_biblioteke).pack(pady=2)
    Button(frame_left, text="Usuń", command=usun_biblioteke).pack(pady=2)

    Label(frame_right, text="Dodaj / Edytuj bibliotekę").pack()
    global entry_biblioteka_nazwa, entry_biblioteka_miasto, entry_biblioteka_ulica, button_dodaj_biblioteke
    Label(frame_right, text="Nazwa:").pack()
    entry_biblioteka_nazwa = Entry(frame_right)
    entry_biblioteka_nazwa.pack()
    Label(frame_right, text="Miasto:").pack()
    entry_biblioteka_miasto = Entry(frame_right)
    entry_biblioteka_miasto.pack()
    Label(frame_right, text="Ulica i nr domu:").pack()
    entry_biblioteka_ulica = Entry(frame_right)
    entry_biblioteka_ulica.pack()
    button_dodaj_biblioteke = Button(frame_right, text="Dodaj bibliotekę", command=dodaj_biblioteke)
    button_dodaj_biblioteke.pack(pady=5)

    # --- Zakładka 2: Pracownicy ---
    tab_pracownicy = Frame(notebook)
    notebook.add(tab_pracownicy, text="Pracownicy")

    frame_left = Frame(tab_pracownicy)
    frame_left.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

    frame_right = Frame(tab_pracownicy)
    frame_right.pack(side=RIGHT, fill=Y, padx=10, pady=10)

    Label(frame_left, text="Lista pracowników").pack()
    global listbox_pracownicy
    listbox_pracownicy = Listbox(frame_left, width=50, height=20)
    listbox_pracownicy.pack()
    Button(frame_left, text="Edytuj", command=edytuj_pracownika).pack(pady=2)
    Button(frame_left, text="Usuń", command=usun_pracownika).pack(pady=2)

    Label(frame_right, text="Dodaj / Edytuj pracownika").pack()
    global entry_pracownik_name, combobox_biblioteki, entry_pracownik_city, entry_pracownik_street, button_dodaj_pracownika
    Label(frame_right, text="Imię i nazwisko:").pack()
    entry_pracownik_name = Entry(frame_right)
    entry_pracownik_name.pack()
    Label(frame_right, text="Biblioteka:").pack()
    combobox_biblioteki = Listbox(frame_right, height=5, exportselection=False)
    combobox_biblioteki.pack()
    Label(frame_right, text="Miasto:").pack()
    entry_pracownik_city = Entry(frame_right)
    entry_pracownik_city.pack()
    Label(frame_right, text="Ulica i nr domu:").pack()
    entry_pracownik_street = Entry(frame_right)
    entry_pracownik_street.pack()

    button_dodaj_pracownika = Button(frame_right, text="Dodaj pracownika", command=dodaj_pracownika)
    button_dodaj_pracownika.pack(pady=5)

    # --- Zakładka 3: Klienci ---
    tab_klienci = Frame(notebook)
    notebook.add(tab_klienci, text="Klienci")

    frame_left = Frame(tab_klienci)
    frame_left.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

    frame_right = Frame(tab_klienci)
    frame_right.pack(side=RIGHT, fill=Y, padx=10, pady=10)

    Label(frame_left, text="Lista klientów").pack()
    global listbox_klienci
    listbox_klienci = Listbox(frame_left, width=50, height=20)
    listbox_klienci.pack()
    Button(frame_left, text="Edytuj", command=edytuj_klienta).pack(pady=2)
    Button(frame_left, text="Usuń", command=usun_klienta).pack(pady=2)

    Label(frame_right, text="Dodaj / Edytuj klienta").pack()
    global entry_klient_name, combobox_biblioteki_klient, entry_klient_city, entry_klient_street, button_dodaj_klienta
    Label(frame_right, text="Imię i nazwisko:").pack()
    entry_klient_name = Entry(frame_right)
    entry_klient_name.pack()
    Label(frame_right, text="Biblioteka:").pack()
    combobox_biblioteki_klient = Listbox(frame_right, height=5, exportselection=False)
    combobox_biblioteki_klient.pack()
    Label(frame_right, text="Miasto:").pack()
    entry_klient_city = Entry(frame_right)
    entry_klient_city.pack()
    Label(frame_right, text="Ulica i nr domu:").pack()
    entry_klient_street = Entry(frame_right)
    entry_klient_street.pack()

    button_dodaj_klienta = Button(frame_right, text="Dodaj klienta", command=dodaj_klienta)
    button_dodaj_klienta.pack(pady=5)

    # --- Zakładka 4: Mapa ---
    tab_mapa = Frame(notebook)
    notebook.add(tab_mapa, text="Mapa")

    frame_top = Frame(tab_mapa)
    frame_top.pack(side=TOP, fill=X, pady=5)

    Label(tab_mapa, text="Wybierz co pokazać na mapie:").pack()

    global listbox_mapa_wybor
    listbox_mapa_wybor = Listbox(tab_mapa, height=15, width=40, exportselection=False)
    listbox_mapa_wybor.pack(pady=10)

    Button(tab_mapa, text="Pokaż na mapie", command=pokaz_na_mapie).pack()

    frame_map = Frame(tab_mapa)
    frame_map.pack(fill=BOTH, expand=True)

    global map_widget
    map_widget = tkintermapview.TkinterMapView(frame_map, width=1200, height=500)
    map_widget.pack(fill=BOTH, expand=True)
    map_widget.set_position(52.2297, 21.0122)
    map_widget.set_zoom(6)

    root.mainloop()
