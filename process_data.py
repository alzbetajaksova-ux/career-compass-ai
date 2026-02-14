import pandas as pd
from google import genai
import time
import json

API_KEY = "AIzaSyBi4s_zW54xS1IOEHOmzlTC-5hUKw_BJcc"
client = genai.Client(api_key=API_KEY)

def clean_job_data(csv_file):
    df = pd.read_csv(csv_file)
    cleaned_data = []

    batch_size = 25

    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]

        jobs_list = []

        for _, row in batch.iterrows():
            jobs_list.append(f"Pozícia: {row['Pozícia']}, Firma: {row['Firma']}")

        combined_prompt = f"""Analyzuj tento zoznam pracovných ponúk a pre každú rozhodni, či ide o IT/Software/Data prácu.

        Zoznam:
        {jobs_list}

        Vráť výsledok ako JSON pole objektov so štruktúrou:
        [

          {{"original_title": "názov", "is_tech": bool, "category": "...", "skills": []}},

          ...

        ]
        """

        try:
            print(f"Posielam súbor inzerátov {i+1} až {i+len(batch)}...")
            response = client.models.generate_content(
                model='gemma-3-4b-it',
                contents=combined_prompt
            )

            clean_json = response.text.replace('```json', '').replace('```', '').strip()
            batch_results = json.loads(clean_json)
            cleaned_data.extend(batch_results)

            print(f"Dávka spracovaná úspešne.")
            time.sleep(12)

        except Exception as e:
            print(f"Chyba pri dávke: {e}")
            time.sleep(20) # Pri chybe počkáme dlhšie

    if cleaned_data:
        pd.DataFrame(cleaned_data).to_csv("cleaned_tech_jobs.csv", index=False, encoding='utf-8-sig')
        print("Dáta uložené do cleaned_tech_jobs.csv")

if __name__ == "__main__":
    clean_job_data("test_data.csv")