import sqlite3

def create_schema():
    # Conecatare la baza de date
    conn = sqlite3.connect('magazin_online.db')
    cursor = conn.cursor()

    print("Creare tabele...")

    # 1. Tabel Produse
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produse (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nume TEXT NOT NULL,
            categorie TEXT,
            pret REAL,
            stoc INTEGER
        )
    ''')

    # 2. Tabel Clienti
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clienti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nume TEXT NOT NULL,
            email TEXT UNIQUE,
            data_inregistrare TEXT
        )
    ''')

    # 3. Tabel Vanzari 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vanzari (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            produs_id INTEGER,
            cantitate INTEGER,
            data_vanzare TEXT,
            FOREIGN KEY (client_id) REFERENCES clienti (id),
            FOREIGN KEY (produs_id) REFERENCES produse (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Succes! Baza de date creata!")

if __name__ == '__main__':
    create_schema()