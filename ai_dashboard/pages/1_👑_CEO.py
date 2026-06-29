import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from data.demo_data import get_projects, get_ai_initiatives, get_recommendations
from utils.helpers import kpi_row, show_table, section

st.set_page_config(page_title="CEO Dashboard", page_icon="👑", layout="wide")
st.markdown("<h1>👑 CEO Dashboard</h1><p style='color:#6E6E73'>Стратегический обзор цифрового контура компании</p>", unsafe_allow_html=True)

projects = pd.DataFrame(get_projects())
ai_init  = pd.DataFrame(get_ai_initiatives())
recs     = pd.DataFrame(get_recommendations())

ai_effect    = ai_init['Эффект (млн/мес)'].sum()
over_budget  = (projects['Отклонение %'] > 20).sum()
crit_proj    = (projects['Статус'] == '🔴 Критично').sum()
prod_ai      = ai_init[ai_init['Зрелость'].isin(['Производство','Масштабируется'])].shape[0]

kpi_row([
    ("Стабильность контура",   "—",              "см. сводку",                     "blue"),
    ("Критических инцидентов", "—",              "см. сводку",                     "red"),
    ("AI-эффект (млн/мес)",    f"{round(ai_effect,1)}", "суммарно по портфелю",   "blue"),
    ("Бюджетных превышений",   str(over_budget), "проектов >20% отклонения",       "red" if over_budget > 2 else "orange"),
])

section("Проектный портфель")
show_table(projects)

section("AI-портфель")
show_table(ai_init)

section("Рекомендации для CEO")
show_table(recs[recs['Роль'] == 'CEO'])
