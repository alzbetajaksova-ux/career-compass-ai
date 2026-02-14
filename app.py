import streamlit as st
import pandas as pd
import duckdb
import ast
import plotly.express as px
import plotly.graph_objects as go
import os



# --- KONFIGURÁCIA ---
st.set_page_config(page_title="CareerCompass AI", layout="wide", page_icon="🧭")

# --- SESSION STATE PRE DARK MODE ---
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# --- DYNAMIC COLORS ---
if st.session_state.dark_mode:
    bg_color = "#0b0e14"
    text_color = "#e0e0e0"
    card_bg = "rgba(255, 255, 255, 0.05)"
    plot_bg = "rgba(20,20,30,0.3)"
    accent_color = "#6366f1"
else:
    bg_color = "#f8f9fa"
    text_color = "#1a1a1a"
    card_bg = "rgba(0, 0, 0, 0.03)"
    plot_bg = "rgba(240,240,245,0.5)"
    accent_color = "#4f46e5"

# --- CUSTOM CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    div[data-testid="stMetric"] {{
        background: {card_bg};
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2);
    }}
    .main-title {{ 
        font-size: 3rem; font-weight: 800; 
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }}
    .sub-text {{ color: #9ca3af; margin-bottom: 2rem; }}
    .section-header {{
        font-size: 1.8rem; font-weight: 700; color: {accent_color}; margin-top: 1rem;
    }}
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_data():
    con = duckdb.connect("career_compass.db")
    try:
        df = con.execute("SELECT * FROM jobs").df()
        df['skills'] = df['skills'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
        df['salary_numeric'] = df['Plat'].astype(float)
        return df
    except:
        return pd.DataFrame()
    finally:
        con.close()

data = load_data()

if data.empty:
    st.warning("Databáza je prázdna. Spusti najskôr database.py!")
    st.stop()

# --- HEADER ---
st.markdown('<p class="main-title">CareerCompass AI </p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Analýza tech trhu s predpripravenými mesačnými platmi</p>', unsafe_allow_html=True)

# --- SIDEBAR (VRÁTENÝ SPÄŤ) ---
with st.sidebar:
    col_toggle1, col_toggle2 = st.columns([3, 1])
    with col_toggle1: st.markdown("### Nastavenia")
    with col_toggle2:
        if st.button("🌓"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    st.markdown("---")
    st.header("Platový Advisor")
    
    tab1, tab2 = st.tabs(["Odhad", "Trh"])
    
    with tab1:
        all_tech = sorted(list(set([s for sublist in data['skills'] for s in sublist])))
        user_skills = st.multiselect("Tvoje technológie", options=all_tech, default=all_tech[:3] if len(all_tech) > 3 else all_tech)
        years_exp = st.slider("Roky praxe", 0, 15, 3)
        
        if user_skills:
            relevant_jobs = data[data['skills'].apply(lambda x: any(s in x for s in user_skills))]
            if not relevant_jobs.empty:
                avg_val = int(relevant_jobs['salary_numeric'].mean())
                adjusted_val = int(avg_val * (1 + (years_exp * 0.05)))
                
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = adjusted_val,
                    delta = {'reference': avg_val, 'suffix': '€'},
                    gauge = {
                        'axis': {'range': [None, 8000]},
                        'bar': {'color': accent_color},
                        'steps': [{'range': [0, 2500], 'color': '#1f2937'}, {'range': [2500, 5000], 'color': '#374151'}]
                    }
                ))
                fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': text_color}, height=250)
                st.plotly_chart(fig_gauge, use_container_width=True)
                st.info(f"Odhadovaný plat: **{adjusted_val} € / mesiac**")
    with tab2:
        if user_skills:
            relevant_jobs = data[data['skills'].apply(lambda x: any(s in x for s in user_skills))]
            if not relevant_jobs.empty:
                market_avg = int(data['salary_numeric'].mean())
                user_avg = int(relevant_jobs['salary_numeric'].mean())
                diff = user_avg - market_avg
                
                # Výpočet podielu na trhu
                market_share = (len(relevant_jobs) / len(data)) * 100
                
                st.markdown(f"**Tvoje skilly vs. Trh**")
                st.metric("Priemer tvojich skillov", f"{user_avg} €", f"{diff} € vs priemer")
                st.metric("Podiel na trhu", f"{market_share:.1f} %", "všetkých ponúk")
                
                # Malý horizontálny bar pre vizualizáciu
                st.write("Dostupnosť pozícií:")
                st.progress(market_share / 100)
            else:
                st.write("Pre zvolené skilly nemáme dostatok dát.")
        else:
            st.write("Vyber si skilly v hornej časti panela.")

# --- HLAVNÉ METRIKY ---
m1, m2, m3, m4 = st.columns(4)
with m1: st.metric("Aktívne ponuky", len(data))
with m2: st.metric("Priemerný plat", f"{int(data['salary_numeric'].mean())} €")
with m3: 
    top_s_series = pd.Series([s for sublist in data['skills'] for s in sublist]).value_counts()
    st.metric("Top Skill", top_s_series.index[0] if not top_s_series.empty else "N/A")
with m4: st.metric("Max. ponuka", f"{int(data['salary_numeric'].max())} €")

st.write("---")

# --- MARKET POSITIONING (VYLEPŠENÝ GRAF) ---
st.markdown('<p class="section-header">Skill Market Positioning</p>', unsafe_allow_html=True)
st.markdown("Vzťah medzi dopytom (počet inzerátov) a priemerným ohodnotením.")

all_skills_flat = [s for sublist in data['skills'] for s in sublist]
skill_counts = pd.Series(all_skills_flat).value_counts()
top_20 = skill_counts.head(20).index
quad_data = []
for s in top_20:
    avg_p = data[data['skills'].apply(lambda x: s in x)]['salary_numeric'].mean()
    quad_data.append({'Skill': s, 'Priemerný Plat': avg_p, 'Dopyt': skill_counts[s]})

df_quad = pd.DataFrame(quad_data)

fig_market = px.scatter(
    df_quad, x="Dopyt", y="Priemerný Plat", text="Skill", size="Dopyt", color="Priemerný Plat",
    color_continuous_scale='Plasma', template="plotly_dark" if st.session_state.dark_mode else "plotly_white"
)
fig_market.update_traces(textposition='top center')
fig_market.update_layout(
    height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor=plot_bg, font_color=text_color,
    xaxis=dict(title="Dopyt (Počet inzerátov)"), yaxis=dict(title="Priemerný plat (€)")
)
st.plotly_chart(fig_market, use_container_width=True)

# --- DOPLNKOVÉ GRAFY ---
st.write("---")
c1, c2 = st.columns(2)
with c1:
    st.subheader("Distribúcia platov")
    fig_hist = px.histogram(data, x="salary_numeric", nbins=15, color_discrete_sequence=[accent_color])
    fig_hist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor=plot_bg, font_color=text_color, xaxis_title="Plat v €")
    st.plotly_chart(fig_hist, use_container_width=True)

with c2:
    st.subheader("Top 10 technológií")
    fig_bar = px.bar(top_s_series.head(10), orientation='h', color=top_s_series.head(10).values, color_continuous_scale='Viridis')
    fig_bar.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor=plot_bg, font_color=text_color, yaxis_title="")
    st.plotly_chart(fig_bar, use_container_width=True)

# --- TABUĽKA ---
st.write("---")
st.subheader("Prehľad inzerátov")
sorted_df = data.sort_values(by='salary_numeric', ascending=False)
st.dataframe(sorted_df[['Pozícia', 'Firma', 'Plat', 'category']], use_container_width=True, height=400)

# --- FOOTER ---
st.markdown(f"""
<div style='text-align: center; color: #6b7280; padding: 20px; margin-top: 40px;'>
    Made by <strong>Alžbeta Jakšová</strong> | <a href='#' style='color: {accent_color};'>GitHub</a>
</div>
""", unsafe_allow_html=True)