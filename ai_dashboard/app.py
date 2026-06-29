import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from data.demo_data import (get_systems, get_incidents, get_risks,
                              get_projects, get_data_quality,
                              get_ai_initiatives, get_recommendations)
from utils.helpers import kpi_row, show_table, section

st.set_page_config(
    page_title="Executive AI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
  [data-testid="stAppViewContainer"] { background: #F5F5F7; }
  [data-testid="stSidebar"] { background: #fff; }
  h1,h2,h3 { font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
               letter-spacing: -0.02em; }
  .block-container { padding-top: 2rem; }
</style>""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
systems      = pd.DataFrame(get_systems())
incidents    = pd.DataFrame(get_incidents())
risks        = pd.DataFrame(get_risks())
projects     = pd.DataFrame(get_projects())
data_quality = pd.DataFrame(get_data_quality())
ai_init      = pd.DataFrame(get_ai_initiatives())
recs         = pd.DataFrame(get_recommendations())

# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎛️ Фильтры")
    period = st.selectbox("Период (инциденты)", ["Весь период","7 дней","30 дней","90 дней"])
    sys_filter = st.selectbox("Система", ["Все"] + list(systems['Система']))
    status_f   = st.selectbox("Статус", ["Все","🟢 Норма","🟡 Внимание","🔴 Критично"])
    crit_f     = st.selectbox("Критичность", ["Все","Критическая","Высокая","Средняя"])
    st.divider()
    st.caption("Executive AI Dashboard v1.0 · 29.06.2026")

# Apply filters
inc_f = incidents.copy()
if period != "Весь период":
    # simplified: filter by index position as demo proxy
    days = {"7 дней":2, "30 дней":8, "90 дней":14}
    inc_f = inc_f.head(days.get(period, len(inc_f)))
if sys_filter != "Все":
    inc_f = inc_f[inc_f['Система'] == sys_filter]

sys_f = systems.copy()
if status_f != "Все":
    sys_f = sys_f[sys_f['Статус'] == status_f]
if crit_f != "Все":
    sys_f = sys_f[sys_f['Критичность'] == crit_f]

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:32px 0 24px">
  <h1 style="font-size:42px;font-weight:700;margin:0">Executive AI Dashboard</h1>
  <p style="color:#6E6E73;font-size:18px;margin-top:8px">Единый экран управления цифровым контуром компании</p>
</div>""", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
norm_sys  = (systems['Статус'] == '🟢 Норма').sum()
total_sys = len(systems)
open_inc  = (incidents['Статус'] != 'Закрыт').sum()
crit_inc  = ((incidents['Критичность'] == 'Критический') & (incidents['Статус'] != 'Закрыт')).sum()
high_risks= (risks['Уровень'] >= 15).sum()
delay_proj= (projects['Статус'] == '🔴 Критично').sum()
ai_effect = ai_init['Эффект (млн/мес)'].sum()

kpi_row([
    ("Систем в норме",        f"{norm_sys}/{total_sys}", f"{round(norm_sys/total_sys*100)}% в пределах SLA", "green"),
    ("Открытых инцидентов",   str(open_inc),  f"{crit_inc} критических",         "red" if crit_inc else "orange"),
    ("Рисков высокого уровня",str(high_risks),"требуют решения",                 "red" if high_risks > 3 else "orange"),
    ("Проектов с отклонением",str(delay_proj),"статус: критично",                "red" if delay_proj > 2 else "orange"),
    ("Эффект AI-портфеля",    f"{round(ai_effect,1)}","млн руб/мес суммарно",    "blue"),
])

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_names = ["📋 ИТ-системы","🚨 Инциденты","⚠️ Риски","📁 Проекты","🗄️ Качество данных","🤖 AI-инициативы","✅ Рекомендации"]
tabs = st.tabs(tab_names)

with tabs[0]:
    section("Состояние ИТ-систем")
    show_table(sys_f)

with tabs[1]:
    section("Инциденты")
    show_table(inc_f)

with tabs[2]:
    section("Реестр рисков")
    show_table(risks)

with tabs[3]:
    section("Проектный портфель")
    show_table(projects)

with tabs[4]:
    section("Качество данных")
    show_table(data_quality)

with tabs[5]:
    section("AI-инициативы")
    show_table(ai_init)
    total_eff = ai_init['Эффект (млн/мес)'].sum()
    prod_cnt  = ai_init[ai_init['Зрелость'].isin(['Производство','Масштабируется'])].shape[0]
    st.info(f"**Суммарный эффект:** {round(total_eff,1)} млн руб/мес · **В производстве/масштабируется:** {prod_cnt} из {len(ai_init)}")

with tabs[6]:
    section("Управленческие рекомендации")
    show_table(recs)
