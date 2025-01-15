CREATE TABLE pracownicy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    imie TEXT NOT NULL,
    nazwisko TEXT NOT NULL,
    stanowisko TEXT NOT NULL
);

CREATE TABLE produkty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nazwa TEXT NOT NULL,
    cena REAL NOT NULL
);

CREATE TABLE konto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    haslo TEXT NOT NULL,
    id_pracownika INTEGER,
    liczba_prob INTEGER DEFAULT 0,
    liczba_prob_data INTEGER DEFAULT 0,  -- Typ INTEGER do przechowywania timestampu
    FOREIGN KEY(id_pracownika) REFERENCES pracownicy(id)
);

CREATE TABLE sprzedaz (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pracownika INTEGER,
    id_produktu INTEGER,
    data_sprzedazy TEXT NOT NULL,
    FOREIGN KEY(id_pracownika) REFERENCES pracownicy(id),
    FOREIGN KEY(id_produktu) REFERENCES produkty(id)
);

INSERT INTO pracownicy (imie, nazwisko, stanowisko) VALUES
('Jan', 'Nowak', 'Zarzad'),
('Michal', 'Kowalski', 'Zarzad'),
('Aneta', 'Jurasik', 'Sklepowa');

INSERT INTO konto (login, haslo, id_pracownika) VALUES
('Jan12', 'cisco12345', 1),
('Michal14', 'zaq1@WSX', 2);

INSERT INTO produkty (nazwa, cena) VALUES
('Naszyjnik pozłacany', 250),
('Pierscionek zaręczynowy złoty', 1000);

INSERT INTO sprzedaz (id_pracownika, id_produktu, data_sprzedazy) VALUES
(3, 1, '2024-12-11'),
(3, 2, '2024-12-12');
