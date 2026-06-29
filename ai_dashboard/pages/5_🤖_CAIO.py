import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from data.demo_data import get_ai_initiatives, get_risks, get_projects, get_recommendations
from utils.helpers import kpi_row, show_table, section

st.set_page_config(page_title="CAIO Dashboard", page_icon="🤖", layout="wide")
st.markdown("<h1>🤖 CAIO Dashboard</h1><p style='color:#6E6E73'>AI use-cases, зрелость внедрения и AI-риски</p>", unsafe_allow_html=True)

ai_init  = pd.DataFrame(get_ai_initiatives())
risks    = pd.DataFrame(get_risks())
projects = pd.DataFrame(get_projects())
recs     = pd.DataFrame(get_recommendations())

ai_prod   = ai_init[ai_init['Зрелость'].isin(['Производство','Масштабируется'])].shape[0]
ai_effect = round(ai_init['Эффект (млн/мес)'].sum(), 1)
avg_adopt = round(ai_init['Внедрение %'].mean())
ai_risks  = (risks['Категория'] == 'AI').sum()

kpi_row([
    ("Зрелых AI-инициатив",  f"{ai_prod}/{len(ai_init)}", "в производстве / масштабируется", "green"),
    ("AI-эффект (млн/мес)",  str(ai_effect),              "суммарно по портфелю",            "blue"),
    ("Среднее внедрение",     f"{avg_adopt}%",             "по портфелю",                     "green" if avg_adopt >= 60 else "orange"),
    ("AI-рисков",             str(ai_risks),               "в реестре рисков",                "red" if ai_risks > 2 else "orange"),
])

section("AI-портфель")
show_table(ai_init)

col1, col2 = st.columns(2)
with col1:
    section("AI-риски")
    show_table(risks[risks['Категория'] == 'AI'])
with col2:
    section("AI-проекты")
    show_table(projects[projects['Роль'] == 'CAIO'])

section("Рекомендации для CAIO")
show_table(recs[recs['Роль'] == 'CAIO'])
