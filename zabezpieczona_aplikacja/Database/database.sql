CREATE TABLE konto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    haslo TEXT NOT NULL,
    id_pracownika INTEGER,
    FOREIGN KEY(id_pracownika) REFERENCES pracownicy(id)
);
CREATE TABLE pracownicy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    imie TEXT NOT NULL,
    nazwisko TEXT NOT NULL,
    stanowisko TEXT NOT NULL
);

CREATE TABLE sprzedaz (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pracownika INTEGER,
    id_produktu INTEGER,
    data_sprzedazy TEXT NOT NULL,
    FOREIGN KEY(id_pracownika) REFERENCES pracownicy(id),
    FOREIGN KEY(id_produktu) REFERENCES produkty(id)
);
CREATE TABLE produkty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nazwa TEXT NOT NULL,
    cena REAL NOT NULL,
    opis TEXT
);
