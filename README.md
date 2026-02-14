je niečo čo mi v mojom readme chyba alebo niečo čo by som mala upraviť?
# 🧭 CareerCompass AI

> AI-powered job market intelligence platform pre data-driven career decisions na slovenskom tech trhu
##  MVP Prototyp

**Tento projekt je portfolio MVP (Minimum Viable Product)** vytvorený na demonštráciu end-to-end data science a development skills.

![header](image.png)
![graf](image-1.png)
![grafy](image-2.png)

### **Aktuálny scope:**
-  Scrapuje **Profesia.sk** pre pozície v IT
-  Analyzuje **~100 job postings** 
-  Fungujúca AI pipeline (Gemini/Gemma API) pre skill extraction
-  Interaktívny dashboard s core features

### **Pre production-ready verziu by bolo potrebné:**
-  Multi-source scraping (Indeed, LinkedIn, Startups.com)
-  Larger dataset (1000+ jobs) pre lepšiu statistical significance
-  Scheduled automation (daily/weekly refresh)
-  Time-series data pre trend analysis

**Cieľ tohto MVP:** Ukázať technickú schopnosť postaviť funkčný product od nuly, nie production-scale analytics platform.

---

## Problém

Job seekers na slovenskom trhu čelia veľkej neistote:
- **70% job postings** neuvádzajú konkrétny plat
- Každá firma píše requirements inak - chaos v dátach
- Ľudia nevedia či ich platové očakávania sú realistické
- Chýba prehľad o tom, ktoré skills sú skutočne žiadané

**CareerCompass AI rieši tento problém pomocou automatizovanej dátovej analýzy a AI.**

---

##  Riešenie

### **Čo projekt robí:**

1. **Automatický zber dát** - Scrapovania job postings z Profesia.sk, Indeed, Remote.co
2. **AI spracovanie** - Gemini API extrahuje skills, kategórie a seniority z neštruktúrovaných textov
3. **Analytika** - Identifikuje trendy, vypočítava priemerné platy, detekuje emerging technologies
4. **Platový advisor** - Odhaduje reálnu trhovú hodnotu na základe tvojich skills a skúseností
5. **Vizualizácie** - Interaktívny dashboard s real-time insights

---

##  Key Features

### **1. Market Intelligence Dashboard**
- **Top skills demand tracker** - Ktoré technológie sú najžiadanejšie
- **Salary distribution analysis** - Platové rozpätia pre rôzne role
- **Skill positioning matrix** - Kvadrantová analýza (dopyt vs. plat)

### **2. AI-Powered Salary Predictor**
- Zadáš svoje skills + roky praxe → dostaneš odhad platu
- Experience multiplier (+5% za každý rok)
- Porovnanie s celkovým trhom
- AI odporúčania na skill development

### **3. Real-time Insights**
-  **Highest Paid** - Top-paying technológie
-  **Most Demanded** - Najpopulárnejšie skills

### **4. Interactive Filters**
- Filter podľa platového rozpätia
- Filter podľa kategórie (Data/Dev/DevOps/QA)
- Full-text search pozícií/firiem
- Export do CSV


##  Tech Stack

### **Backend**
- **Python 3.11+** - Core language
- **Playwright** - Browser automation (anti-bot scraping)
- **Gemini 1.5 Flash API** - AI-powered NLP (skill extraction, categorization)
- **DuckDB** - Embedded analytical database (fast, zero-setup)
- **pandas** - Data manipulation

### **Frontend**
- **Streamlit** - Interactive web dashboard
- **Plotly** - Advanced visualizations (scatter, box plots, gauges)
- **Custom CSS** - Dark/Light mode, animated components

### **Data Pipeline**
```python
Job Sites → Scrapers → Raw HTML 
    ↓
Gemini API → Structured JSON (skills, salary, category)
    ↓
DuckDB → Analytics & Aggregations
    ↓
Streamlit → Interactive Dashboard
```


##  Quick Start

### **Prerequisites**
```bash
Python 3.11+
pip
Git
```

### **Installation**

1. **Clone repo**
```bash
git clone https://github.com/alzbetajaksova-ux/career-compass-ai.git
cd career-compass-ai
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup Gemini API Key**
```bash
# Get free API key: https://aistudio.google.com/app/apikey
# Add to process_data.py:
API_KEY = "your_gemini_api_key_here"
```

5. **Run scraper (collect data)**
```bash
# Scrape Profesia.sk for Python jobs
python scraper_test.py

# Process with AI
python process_data.py

# Build database
python database.py
```

6. **Launch dashboard**
```bash
streamlit run app.py
```

7. **Open browser**
```
http://localhost:8501
```




*Data refreshed weekly | Last update: February 2026*

</div>
