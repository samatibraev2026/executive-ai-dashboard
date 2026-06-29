import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from data.demo_data import get_data_quality, get_risks, get_projects, get_recommendations
from utils.helpers import kpi_row, show_table, section

st.set_page_config(page_title="CDO Dashboard", page_icon="🗄️", layout="wide")
st.markdown("<h1>🗄️ CDO Dashboard</h1><p style='color:#6E6E73'>Качество данных, интеграции и data-риски</p>", unsafe_allow_html=True)

dq       = pd.DataFrame(get_data_quality())
risks    = pd.DataFrame(get_risks())
projects = pd.DataFrame(get_projects())
recs     = pd.DataFrame(get_recommendations())

avg_score  = round(dq['Индекс качества'].mean(), 1)
dq_ok      = (dq['Статус'] == '🟢 Норма').sum()
int_ok     = (dq['Интеграция'] == '✅ OK').sum()
data_risks = (risks['Категория'] == 'Данные').sum()

kpi_row([
    ("Средний индекс качества", f"{avg_score}%", "по всем источникам",   "green" if avg_score >= 90 else ("orange" if avg_score >= 75 else "red")),
    ("Источников в норме",      f"{dq_ok}/{len(dq)}", "остальные — внимание/критично", "green" if dq_ok == len(dq) else "orange"),
    ("Интеграций OK",           f"{int_ok}/{len(dq)}", "активных без ошибок",         "green" if int_ok == len(dq) else "orange"),
    ("Data-рисков",             str(data_risks), "в реестре рисков",               "red" if data_risks > 2 else "orange"),
])

section("Качество данных по источникам")
show_table(dq)

col1, col2 = st.columns(2)
with col1:
    section("Data-риски")
    show_table(risks[risks['Категория'] == 'Данные'])
with col2:
    section("CDO-проекты")
    show_table(projects[projects['Роль'] == 'CDO'])

section("Рекомендации для CDO")
show_table(recs[recs['Роль'] == 'CDO'])
