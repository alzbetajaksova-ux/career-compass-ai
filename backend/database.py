import duckdb
import pandas as pd
import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "career_compass.db")
RAW_DATA_PATH = os.path.join(BASE_DIR, "..", "data", "test_data.csv")
AI_DATA_PATH = os.path.join(BASE_DIR, "..", "data", "cleaned_tech_jobs.csv")

def clean_salary(salary_str):
    """
    Vyčistí textový plat a vráti čisté číslo reprezentujúce mesačnú mzdu.
    """
    if pd.isna(salary_str) or salary_str == "Neuvedený":
        return None
    
    s = str(salary_str).lower().replace('\xa0', '').replace(' ', '')
    s = s.replace('od', '').replace(',', '.')
    
    is_hourly = any(keyword in s for keyword in ["hod", "/h", "hour"])
    
    nums = re.findall(r'\d+\.?\d*', s)
    
    if not nums:
        return None
    
    nums = [float(n) for n in nums]
    
    if len(nums) >= 2:
        base_val = sum(nums) / len(nums)
    else:
        base_val = nums[0]
    
    if is_hourly:
        if base_val < 500:
            base_val = base_val * 160
            
    return int(base_val)

def update_database():
    con = duckdb.connect(DB_PATH)

    try:
        df_raw = pd.read_csv(RAW_DATA_PATH)
        df_ai = pd.read_csv(AI_DATA_PATH)

        df_final = pd.concat([df_raw, df_ai[['is_tech', 'category', 'skills']]], axis=1)
        
        df_final = df_final[df_final['is_tech'] == True].copy()
        
        # --- ČISTENIE PLATU PRED ULOŽENÍM ---
        df_final['salary_numeric'] = df_final['Plat'].apply(clean_salary)
        
        df_final['Plat'] = df_final['salary_numeric']
        
        df_final = df_final.dropna(subset=['Plat'])
        
        df_final['scraped_at'] = pd.Timestamp.now()

        con.execute("DROP TABLE IF EXISTS jobs")
        con.execute("CREATE TABLE jobs AS SELECT * FROM df_final")
        
        # Odstránenie duplikátov
        con.execute("""
            CREATE TABLE temp_jobs AS 
            SELECT * FROM (
                SELECT *, ROW_NUMBER() OVER(PARTITION BY Pozícia, Firma ORDER BY scraped_at DESC) as rn
                FROM jobs
            ) WHERE rn = 1;
            DROP TABLE jobs;
            ALTER TABLE temp_jobs DROP rn;
            ALTER TABLE temp_jobs RENAME TO jobs;
        """)

        count = con.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
        avg_salary = con.execute("SELECT AVG(Plat) FROM jobs").fetchone()[0]
        
        print(f"\nDatabáza úspešne aktualizovaná!")
        print(f"Počet IT pozícií: {count}")
        print(f"Priemerný mesačný plat v DB: {int(avg_salary)} €")

    except Exception as e:
        print(f"Chyba pri ukladaní do databázy: {e}")
    finally:
        con.close()

if __name__ == "__main__":
    update_database()