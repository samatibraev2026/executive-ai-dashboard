import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from data.demo_data import get_incidents, get_risks, get_projects, get_recommendations
from utils.helpers import kpi_row, show_table, section

st.set_page_config(page_title="CTO Dashboard", page_icon="🛠️", layout="wide")
st.markdown("<h1>🛠️ CTO Dashboard</h1><p style='color:#6E6E73'>Инфраструктура, кибербезопасность и технологические риски</p>", unsafe_allow_html=True)

incidents = pd.DataFrame(get_incidents())
risks     = pd.DataFrame(get_risks())
projects  = pd.DataFrame(get_projects())
recs      = pd.DataFrame(get_recommendations())

crit_inc   = (incidents['Критичность'] == 'Критический').sum()
cyber_risks= (risks['Категория'] == 'Кибербезопасность').sum()
tech_risks = (risks['Категория'] == 'Технологический').sum()
infra_proj = projects[projects['Роль'] == 'CTO']

kpi_row([
    ("Критических инцидентов", str(crit_inc),    "всего за период",     "red" if crit_inc > 3 else "orange"),
    ("Кибер-рисков",           str(cyber_risks), "в реестре",           "red" if cyber_risks > 2 else "orange"),
    ("Технологических рисков", str(tech_risks),  "требуют mitigation",  "orange"),
    ("Инфра-проектов",         str(len(infra_proj)), "в портфеле CTO",  "blue"),
])

section("Критические и высокие инциденты")
show_table(incidents[incidents['Критичность'].isin(['Критический','Высокий'])])

col1, col2 = st.columns(2)
with col1:
    section("Кибер-риски")
    show_table(risks[risks['Категория'] == 'Кибербезопасность'])
with col2:
    section("Технологические риски")
    show_table(risks[risks['Категория'] == 'Технологический'])

section("Инфра-проекты")
show_table(infra_proj)

section("Рекомендации для CTO")
show_table(recs[recs['Роль'] == 'CTO'])
