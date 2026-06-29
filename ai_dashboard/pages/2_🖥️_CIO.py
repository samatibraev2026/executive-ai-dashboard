import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from data.demo_data import get_systems, get_incidents, get_projects, get_recommendations
from utils.helpers import kpi_row, show_table, section

st.set_page_config(page_title="CIO Dashboard", page_icon="🖥️", layout="wide")
st.markdown("<h1>🖥️ CIO Dashboard</h1><p style='color:#6E6E73'>ИТ-системы, доступность, SLA, инциденты и проекты</p>", unsafe_allow_html=True)

systems   = pd.DataFrame(get_systems())
incidents = pd.DataFrame(get_incidents())
projects  = pd.DataFrame(get_projects())
recs      = pd.DataFrame(get_recommendations())

sla_viol  = (systems['Статус'] != '🟢 Норма').sum()
open_inc  = (incidents['Статус'] != 'Закрыт').sum()
avg_avail = round(systems['Доступность %'].mean(), 2)
it_proj   = projects[projects['Роль'] == 'CIO']

kpi_row([
    ("Средняя доступность",    f"{avg_avail}%", "по всем системам",       "green" if avg_avail >= 99 else "orange"),
    ("Нарушений SLA",          str(sla_viol),   "систем ниже целевого",   "red" if sla_viol > 2 else "orange"),
    ("Открытых инцидентов",    str(open_inc),   "все категории",          "red" if open_inc > 5 else "orange"),
    ("ИТ-проектов",            str(len(it_proj)),"под управлением CIO",   "blue"),
])

with st.sidebar:
    st.markdown("## Фильтры")
    status_f = st.selectbox("Статус системы", ["Все","🟢 Норма","🟡 Внимание","🔴 Критично"])
    crit_f   = st.selectbox("Критичность", ["Все","Критическая","Высокая","Средняя"])

sys_f = systems.copy()
if status_f != "Все": sys_f = sys_f[sys_f['Статус'] == status_f]
if crit_f   != "Все": sys_f = sys_f[sys_f['Критичность'] == crit_f]

section("Состояние ИТ-систем")
show_table(sys_f)

section("Инциденты")
show_table(incidents)

section("ИТ-проекты")
show_table(it_proj)

section("Рекомендации для CIO")
show_table(recs[recs['Роль'] == 'CIO'])
