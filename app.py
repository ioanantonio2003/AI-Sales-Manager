import streamlit as st
import os
import sqlite3
from dotenv import load_dotenv
from google import genai

# CONFIGURARE
st.set_page_config(page_title="AI Sales Manager", page_icon="🤖", layout="wide")
load_dotenv()

# Verificarea cheia API
if not os.getenv("GOOGLE_API_KEY"):
    st.error("Lipseste cheia GOOGLE_API_KEY din fisierul .env!")
    st.stop()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
DB_NAME = "magazin_online.db"

# FUNCȚIILE

def get_db_schema():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    tables = cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';").fetchall()
    schema_str = ""
    for table in tables:
        if table[0]:
            schema_str += table[0] + "\n"
    conn.close()
    return schema_str

def ask_ai_for_sql(question, schema):
    prompt = f"""
    Ești un expert SQL.
    Schema bazei de date:
    {schema}
    
    Întrebarea: "{question}"
    
    Returnează DOAR codul SQL (fără markdown, fără ```sql). Doar SELECT.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        return response.text.strip().replace('```sql', '').replace('```', '')
    except Exception as e:
        return f"Eroare AI: {e}"

def execute_query(sql_query):
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        
        if rows:
            # trasnformam datele pentru afisare
            data = [dict(row) for row in rows]
            conn.close()
            return data, None # returnam datele
        else:
            conn.close()
            return [], None
    except Exception as e:
        return None, str(e)

# --- INTERFATA Streamlit

st.title("🤖 AI Sales Manager")
st.markdown("Interoghează baza de date folosind **limbaj natural**.")

# 1. Sidebar
with st.sidebar:
    st.header("🔧 Baza de Date")
    if st.button("Arată Schema(SQL)"):
        st.text(get_db_schema())
    st.info("Folosește acest agent pentru a analiza vânzările, clienții și stocurile.")

# 2. Initializare istoric chat 
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Afișarea mesajelor vechi din sesiune
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Dacă mesajul are și date (tabel), le afișăm
        if "data" in message and message["data"]:
            st.dataframe(message["data"])
        # Dacă are eroare sql
        if "error" in message and message["error"]:
            st.error(message["error"])

# 4. Input-ul Utilizatorului
if prompt := st.chat_input("Ce vrei să afli? (ex: Top 3 cele mai scumpe produse)"):
    # Afișăm întrebarea utilizatorului
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Procesăm răspunsul AI
    with st.chat_message("assistant"):
        with st.spinner("Generez SQL..."):
            schema = get_db_schema()
            sql_code = ask_ai_for_sql(prompt, schema)
            
            st.code(sql_code, language="sql") # Arătăm codul generat
            
            # Executăm
            data, error = execute_query(sql_code)
            
            if error:
                st.error(f"Eroare SQL: {error}")
                st.session_state.messages.append({"role": "assistant", "content": f"Am generat SQL: `{sql_code}`", "error": error})
            elif data:
                st.dataframe(data) # Tabel interactiv!
                st.session_state.messages.append({"role": "assistant", "content": "Iată datele găsite:", "data": data})
            else:
                st.warning("Nu am găsit rezultate.")
                st.session_state.messages.append({"role": "assistant", "content": "Nu am găsit rezultate pentru interogarea ta."})