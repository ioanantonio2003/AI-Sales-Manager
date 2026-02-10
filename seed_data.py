import sqlite3

def seed_data():
    conn = sqlite3.connect('magazin_online.db')
    cursor = conn.cursor()

    print("Se introduc datele de test...")

    # Inserare Produse
    produse = [
        ('Laptop Gaming X', 'Electronice', 4500.00, 10),
        ('Mouse Wireless', 'Accesorii', 120.50, 50),
        ('Monitor 24 inch', 'Electronice', 850.00, 20),
        ('Tastatura Mecanica', 'Accesorii', 300.00, 30),
        ('Casti Noise Cancelling', 'Audio', 550.00, 15),
        ('Scaun Birou Ergonomic', 'Mobilier', 1200.00, 5),
        ('Webcam HD', 'Accesorii', 250.00, 25)
    ]
    cursor.executemany('''
        INSERT INTO produse (nume, categorie, pret, stoc) 
        VALUES (?, ?, ?, ?)
    ''', produse)

    # Inserare Clienți
    clienti = [
        ('Ion Popescu', 'ion.popescu@email.com', '2023-10-15'),
        ('Maria Ionescu', 'maria.i@email.com', '2023-11-20'),
        ('Andrei Radu', 'andrei.r@email.com', '2023-12-05'),
        ('Elena Dumitrescu', 'elena.d@email.com', '2024-01-10')
    ]
    cursor.executemany('''
        INSERT INTO clienti (nume, email, data_inregistrare) 
        VALUES (?, ?, ?)
    ''', clienti)

    vanzari = [
        (1, 1, 1, '2024-01-15'), # Ion a luat 1 Laptop
        (1, 2, 2, '2024-01-15'), # Ion a luat si 2 Mouse-uri
        (2, 3, 1, '2024-01-20'), # Maria a luat 1 Monitor
        (3, 5, 1, '2024-02-01'), # Andrei a luat Casti
        (4, 1, 1, '2024-02-10'), # Elena a luat 1 Laptop
        (2, 2, 1, '2024-02-15')  # Maria a mai luat 1 Mouse
    ]
    cursor.executemany('''
        INSERT INTO vanzari (client_id, produs_id, cantitate, data_vanzare) 
        VALUES (?, ?, ?, ?)
    ''', vanzari)

    conn.commit()
    conn.close()
    print("Succes! Datele au fost introduse în 'magazin_online.db'.")

if __name__ == '__main__':
    seed_data()