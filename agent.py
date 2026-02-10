import os
import sqlite3
from dotenv import load_dotenv
from google import genai

#CONFIGURARe
load_dotenv()
# Folosim cheia din .env
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
DB_NAME = "magazin_online.db"

# FUNCȚII AJUTĂTOARE

def get_db_schema():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Interogam sqlite_master pentru a afla structura
    tables = cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';").fetchall()
    
    schema_str = ""
    for table in tables:
        if table[0]:
            schema_str += table[0] + "\n"
        
    conn.close()
    return schema_str

def ask_ai_for_sql(question, schema):
    # Aici este "Prompt Engineering"-ul.Cum se comporta AI
    prompt = f"""
    Ești un expert în Data Science și SQL.
    
    Sarcina ta: Convertește întrebarea utilizatorului într-o interogare SQL validă pentru SQLite.
    
    SCHEMA BAZEI DE DATE:
    {schema}
    
    ÎNTREBAREA UTILIZATORULUI: "{question}"
    
    REGULI FOARTE IMPORTANTE:
    1. Returnează DOAR codul SQL. Fără explicații, fără introduceri gen 'Iată codul'.
    2. Nu folosi formatare Markdown (fără ```sql ... ```).
    3. Folosește doar comenzi de citire (SELECT). NU ai voie să faci DELETE, UPDATE sau DROP.
    4. Dacă întrebarea nu are legătură cu datele, returnează textul "Eroare: Întrebare irelevantă".
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        # curatam răspunsul
        sql_query = response.text.strip().replace('```sql', '').replace('```', '')
        return sql_query
    except Exception as e:
        print(f"Eroare de comunicare cu AI: {e}")
        return None

def execute_query(sql_query):
    """
    Execută SQL-ul primit pe baza de date.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute(sql_query)
        results = cursor.fetchall()
        
        # Obținem și numele coloanelor pentru a le afișa frumos
        if cursor.description:
            column_names = [description[0] for description in cursor.description]
        else:
            column_names = []
            
        conn.close()
        return column_names, results
    except Exception as e:
        return None, f"Eroare la execuția SQL: {e}"

# --- 3. PROGRAMUL PRINCIPAL (Interfața în consolă) ---

def main():
    print("==========================================")
    print("🤖 AI SALES AGENT - Interoghează baza de date")
    print("Scrie 'exit' pentru a ieși.")
    print("==========================================\n")
    
    # 1. Încărcăm schema o singură dată la început
    print("Rețeaua neuronală citește structura bazei de date...")
    schema = get_db_schema()
    print("Agentul este pregătit! Ce vrei să afli?\n")
    
    while True:
        user_input = input("Întrebare > ")
        if user_input.lower() in ['exit', 'quit', 'pa']:
            print("La revedere!")
            break
            
        if not user_input.strip():
            continue

        print("⏳ Gândesc...")
        
        # 2. Obținem SQL-ul de la AI
        sql_code = ask_ai_for_sql(user_input, schema)
        
        if not sql_code or "Eroare" in sql_code:
            print("Nu am putut genera o interogare validă.")
            continue
            
        print(f"💻 SQL Generat: {sql_code}")
        
        # 3. Executăm
        columns, data = execute_query(sql_code)
        
        # 4. Afișăm rezultatul
        if isinstance(data, str) and "Eroare" in data:
            print(f"❌ {data}")
        else:
            print("\nREZULTATE:")
            if columns:
                print(f"| {' | '.join(columns)} |")
                print("-" * (len(str(columns)) + 10))
            
            if len(data) == 0:
                print("Nu s-au găsit rezultate.")
            else:
                for row in data:
                    print(row)
            print("\n" + "="*30 + "\n")

if __name__ == "__main__":
    main()