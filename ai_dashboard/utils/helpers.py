import streamlit as st
import pandas as pd

STATUS_COLORS = {
    '🟢 Норма': 'green',
    '🟡 Внимание': 'orange',
    '🔴 Критично': 'red',
}

def kpi_row(items):
    cols = st.columns(len(items))
    for col, (label, value, sub, color) in zip(cols, items):
        with col:
            st.markdown(f"""
            <div style="background:#fff;border-radius:14px;padding:20px 22px;
                        box-shadow:0 2px 16px rgba(0,0,0,0.07);border:1px solid rgba(0,0,0,0.05)">
              <div style="font-size:13px;color:#6E6E73;font-weight:500;margin-bottom:8px">{label}</div>
              <div style="font-size:34px;font-weight:700;letter-spacing:-0.03em;color:#1D1D1F;line-height:1">{value}</div>
              <div style="font-size:12px;color:#6E6E73;margin-top:6px">{sub}</div>
            </div>""", unsafe_allow_html=True)
    st.write("")

def status_filter(df, col='Статус'):
    opt = st.selectbox('Статус', ['Все', '🟢 Норма', '🟡 Внимание', '🔴 Критично'], key=f'sf_{col}_{id(df)}')
    if opt != 'Все':
        df = df[df[col] == opt]
    return df

def show_table(df):
    st.dataframe(df, use_container_width=True, hide_index=True)

def progress_col(df, col):
    return df

def section(title):
    st.markdown(f"### {title}")
