import os
from dotenv import load_dotenv
from google import genai

# 1.incarca cheile
load_dotenv()

# 2. Configureaza Clientul
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

def test_connection():
    print("Testez conexiunea cu Gemini 2.5 Flash...")
    
    try:
        # Folosim modelul confirmat din lista ta
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Salut! Confirmă-mi că ești conectat și funcțional."
        )
        print("\n✅ Răspuns primit de la AI:")
        print(response.text)
        
    except Exception as e:
        print(f"\n❌ Eroare: {e}")

if __name__ == "__main__":
    test_connection()