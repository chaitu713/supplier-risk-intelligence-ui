import re
import sys
import os

from altair import value
from altair import value
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from plotly import colors
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import plotly.express as px
import numpy as np

from backend.blob_storage import upload_file_to_blob
from backend.document_intelligence import extract_document
from backend.data_append import process_extracted_document
from backend.document_history import log_document
from backend.ai_agent import ask_supplier_ai


############################################################
# PAGE CONFIG
############################################################

st.set_page_config(
    page_title="Responsible Sourcing & Supplier Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=DM+Mono:wght@400;500&family=Playfair+Display:wght@600;700&display=swap');

/* ─────────────────────────────────────────────
   ROOT DESIGN TOKENS
───────────────────────────────────────────── */
:root {
    /* Base */
    --bg:           #F4F6FB;
    --surface:      #FFFFFF;
    --surface-2:    #F8FAFD;
    --surface-3:    #EFF3FB;

    /* Borders */
    --border:       #E4EAF4;
    --border-2:     #D2DBF0;

    /* Text */
    --text-1:       #0D1B3E;
    --text-2:       #4A5878;
    --text-3:       #8A97B8;

    /* Primary accent — deep navy-blue */
    --primary:      #1B3FCC;
    --primary-2:    #1530A8;
    --primary-l:    #EBF0FF;
    --primary-xl:   #F4F6FF;

    /* Semantic */
    --green:        #0C9E6B;
    --green-l:      #E7F9F2;
    --green-border: #9AE0C7;

    --amber:        #D08700;
    --amber-l:      #FEF7E7;
    --amber-border: #F0C968;

    --red:          #D42B2B;
    --red-l:        #FEF0F0;
    --red-border:   #F5AAAA;

    --teal:         #0891B2;
    --teal-l:       #E0F6FB;

    /* Radius */
    --radius-sm:    8px;
    --radius-md:    14px;
    --radius-lg:    20px;
    --radius-xl:    28px;

    /* Shadows */
    --shadow-xs:    0 1px 2px rgba(13,27,62,.04);
    --shadow-sm:    0 2px 8px rgba(13,27,62,.06);
    --shadow-md:    0 6px 20px rgba(13,27,62,.08);
    --shadow-lg:    0 16px 48px rgba(13,27,62,.10);

    /* Sidebar width */
    --sidebar-w:    270px;

    color-scheme: light !important;
}

/* ─────────────────────────────────────────────
   GLOBAL RESET & BASE
───────────────────────────────────────────── */
html, body, .stApp {
    background: var(--bg) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text-1) !important;
    -webkit-font-smoothing: antialiased;
}

/* Remove streamlit top bar */
[data-testid="stHeader"] { display: none !important; }
[data-testid="stAppViewContainer"] { padding-top: 0 !important; }
[data-testid="stSidebarCollapseButton"] { display: none !important; }
.block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }

/* ─────────────────────────────────────────────
   SCROLLBAR
───────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-2); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-3); }
html, body, .stApp { overflow-x: hidden !important; }

/* ─────────────────────────────────────────────
   SIDEBAR
───────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: 2px 0 16px rgba(13,27,62,.05) !important;
}

section[data-testid="stSidebar"] > div {
    padding-top: 0 !important;
}

section[data-testid="stSidebar"]::-webkit-scrollbar { width: 3px; }
section[data-testid="stSidebar"]::-webkit-scrollbar-thumb { background: transparent; }

/* ─────────────────────────────────────────────
   SIDEBAR NAV — radio as nav pills
───────────────────────────────────────────── */
[data-testid="stSidebar"] .stRadio {
    width: 100%;
}

[data-testid="stSidebar"] .stRadio > label {
    display: none !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] {
    display: flex;
    flex-direction: column;
    gap: 3px;
    padding: 0 12px;
}

[data-testid="stSidebar"] div[role="radiogroup"] label {
    display: flex !important;
    align-items: center !important;
    width: 100% !important;
    min-height: 42px !important;
    padding: 10px 14px !important;
    border-radius: 10px !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    color: var(--text-2) !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    box-sizing: border-box !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
    display: none !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: var(--primary-xl) !important;
    color: var(--primary) !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: var(--primary-l) !important;
    color: var(--primary) !important;
    font-weight: 600 !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) span {
    color: var(--primary) !important;
    font-weight: 600 !important;
}

/* ─────────────────────────────────────────────
   SIDEBAR METRICS
───────────────────────────────────────────── */
[data-testid="stSidebar"] [data-testid="stMetric"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
}

[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    font-size: 20px !important;
    font-weight: 700 !important;
    color: var(--text-1) !important;
}

[data-testid="stSidebar"] [data-testid="stMetricLabel"] p {
    font-size: 11px !important;
    color: var(--text-3) !important;
    text-transform: uppercase !important;
    letter-spacing: .06em !important;
    font-weight: 600 !important;
}

[data-testid="stSidebar"] [data-testid="stMetric"] > div {
    position: static !important;
    transform: none !important;
    width: auto !important;
    text-align: left !important;
}

[data-testid="stSidebar"] [data-testid="stMetric"] {
    height: auto !important;
}

/* ─────────────────────────────────────────────
   GLOBAL METRICS (main area)
───────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 20px 22px !important;
    box-shadow: var(--shadow-xs);
    transition: box-shadow 0.2s ease, transform 0.2s ease;
    height: auto !important;
    position: relative !important;
}

[data-testid="stMetric"] > div {
    position: static !important;
    transform: none !important;
    width: auto !important;
    text-align: left !important;
}

[data-testid="stMetric"]:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}

[data-testid="stMetricLabel"] {
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: .08em !important;
    color: var(--text-3) !important;
    margin-bottom: 6px !important;
}

[data-testid="stMetricLabel"] p {
    color: var(--text-3) !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: .08em !important;
}

[data-testid="stMetricValue"] {
    font-size: 30px !important;
    font-weight: 700 !important;
    color: var(--text-1) !important;
    letter-spacing: -.02em !important;
    line-height: 1.1 !important;
}

/* ─────────────────────────────────────────────
   BUTTONS
───────────────────────────────────────────── */
.stButton > button {
    background: var(--primary) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 22px !important;
    height: auto !important;
    letter-spacing: .01em !important;
    transition: all 0.18s ease !important;
    box-shadow: 0 2px 8px rgba(27,63,204,.25) !important;
}

.stButton > button * { color: #FFFFFF !important; }

.stButton > button:hover {
    background: var(--primary-2) !important;
    box-shadow: 0 4px 16px rgba(27,63,204,.35) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ─────────────────────────────────────────────
   INPUTS & SELECTS
───────────────────────────────────────────── */
[data-testid="stTextInput"] input,
[data-testid="stTextAreaInput"] textarea {
    background: var(--surface) !important;
    color: var(--text-1) !important;
    border: 1.5px solid var(--border-2) !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    transition: border-color 0.15s ease !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stTextAreaInput"] textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(27,63,204,.08) !important;
}

/* Selectbox */
[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background: var(--surface) !important;
    border: 1.5px solid var(--border-2) !important;
    border-radius: 10px !important;
}

[data-testid="stSelectbox"] div[data-baseweb="select"]:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(27,63,204,.08) !important;
}

[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    border: none !important;
}

[data-testid="stSelectbox"] input { caret-color: transparent !important; }

div[data-baseweb="select"] span,
div[data-baseweb="select"] svg { display: none !important; }

div[data-baseweb="select"] * { border-right: none !important; }

[data-baseweb="menu"] {
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
    box-shadow: var(--shadow-md) !important;
    overflow: hidden !important;
}

[data-baseweb="menu"] > div { overflow: hidden !important; }
[data-baseweb="menu"] * { scrollbar-width: none !important; }
[data-baseweb="menu"] *::-webkit-scrollbar { display: none !important; }
[data-baseweb="menu"] { max-height: none !important; }

/* ─────────────────────────────────────────────
   FILE UPLOADER
───────────────────────────────────────────── */
[data-testid="stFileUploader"],
[data-testid="stFileUploader"] * {
    background: var(--surface) !important;
    color: var(--text-1) !important;
    border-color: var(--border) !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: var(--surface-2) !important;
    border: 2px dashed var(--border-2) !important;
    border-radius: 12px !important;
    padding: 24px 20px !important;
    transition: all 0.2s ease !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    background: var(--primary-xl) !important;
    border-color: var(--primary) !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stFileUploaderDropzoneInstructions"] small {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text-2) !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] span { font-size: 13.5px !important; font-weight: 500 !important; }
[data-testid="stFileUploaderDropzoneInstructions"] small { font-size: 12px !important; }

[data-testid="stFileUploader"] button {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

[data-testid="stFileUploaderFile"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 8px 12px !important;
    margin-top: 8px !important;
}

[data-testid="stFileUploaderFileData"] span { font-size: 12px !important; color: var(--text-1) !important; }
[data-testid="stFileUploaderFileData"] small { font-size: 11px !important; color: var(--text-3) !important; }
[data-testid="stFileUploaderDeleteBtn"] button { background: transparent !important; color: var(--text-3) !important; }
[data-testid="stFileUploaderDeleteBtn"] button:hover { color: var(--red) !important; }

/* ─────────────────────────────────────────────
   DATAFRAME
───────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    box-shadow: var(--shadow-xs) !important;
    overflow: hidden !important;
}

[data-testid="stDataFrameToolbar"] {
    background: var(--surface-2) !important;
    border-bottom: 1px solid var(--border) !important;
}

[data-testid="stDataFrame"] canvas { background: var(--surface) !important; }

[data-testid="stDataFrame"] div[role="columnheader"] {
    background: var(--surface-2) !important;
    color: var(--text-2) !important;
    font-weight: 600 !important;
    font-size: 12px !important;
    letter-spacing: .04em !important;
}

[data-testid="stDataFrame"] div[role="gridcell"] {
    color: var(--text-1) !important;
    font-size: 13px !important;
}

[data-testid="stDataFrame"] div[role="row"]:hover { background: var(--surface-3) !important; }

/* ─────────────────────────────────────────────
   CHAT
───────────────────────────────────────────── */
/* Entire chat input container */
div[data-testid="stChatInput"] {
    background: #FFFFFF !important;
    border: 1px solid #E6EAF2 !important;
    border-radius: 16px !important;
    padding: 8px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
}

/* Text area */
div[data-testid="stChatInput"] textarea {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    font-size: 14px !important;
}

/* Send button */
div[data-testid="stChatInput"] button {
    background: #2563EB !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 6px 10px !important;
}

/* Remove weird inner borders */
div[data-testid="stChatInput"] div {
    border: none !important;
}

/* Chat message container spacing */
div[data-testid="stChatMessage"] {
    margin-bottom: 12px;
}

/* Assistant message card */
div[data-testid="stChatMessage"][data-testid*="assistant"] > div {
    background: #FFFFFF;
    border: 1px solid #E6EAF2;
    border-radius: 14px;
    padding: 14px;
}

/* Remove excessive spacing inside markdown */
div[data-testid="stMarkdownContainer"] p {
    margin-bottom: 6px;
}

/* Headings tighter */
div[data-testid="stMarkdownContainer"] h3 {
    margin-bottom: 8px;
    margin-top: 12px;
}

/* Remove ugly horizontal lines */
hr {
    margin: 10px 0 !important;
    opacity: 0.2;
}
            
/* Headings (Key Insights, etc.) */
div[data-testid="stMarkdownContainer"] strong,
div[data-testid="stMarkdownContainer"] h3 {
    font-size: 16px !important;
    font-weight: 600 !important;
    color: #0F172A;
}

/* Content text */
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] li {
    font-size: 13px !important;
    color: #334155;
    line-height: 1.5;
}

/* Reduce spacing */
div[data-testid="stMarkdownContainer"] ul {
    margin-top: 4px;
    margin-bottom: 6px;
}
            
/* Chat message container */
div[data-testid="stChatMessage"] {
    margin-bottom: 10px;
}

/* USER avatar (question - blue) */
div[data-testid="stChatMessage"]:has(div[data-testid="stMarkdownContainer"]:first-child) img {
    background-color: #2563EB !important;
    border-radius: 8px;
    padding: 4px;
}

/* ASSISTANT avatar (answer - light blue) */
div[data-testid="stChatMessage"]:has(div[data-testid="stMarkdownContainer"]:last-child) img {
    background-color: #EFF6FF !important;
    border-radius: 8px;
    padding: 4px;
}

/* ─────────────────────────────────────────────
   SEGMENTED CONTROL (dataset selector)
───────────────────────────────────────────── */
[data-testid="stSegmentedControl"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 3px !important;
}

[data-testid="stSegmentedControl"] label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* ─────────────────────────────────────────────
   PROGRESS BAR
───────────────────────────────────────────── */
[data-testid="stProgressBar"] > div > div {
    background: var(--primary) !important;
    border-radius: 99px !important;
}

[data-testid="stProgressBar"] > div {
    background: var(--primary-l) !important;
    border-radius: 99px !important;
}

/* ─────────────────────────────────────────────
   TYPOGRAPHY
───────────────────────────────────────────── */
h1 {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 26px !important;
    font-weight: 700 !important;
    color: var(--text-1) !important;
    letter-spacing: -.03em !important;
}

h2 {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 19px !important;
    font-weight: 700 !important;
    color: var(--text-1) !important;
    letter-spacing: -.02em !important;
}

h3 {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
}

p, label, span {
    font-family: 'DM Sans', sans-serif !important;
}
            
/* ───────── TRUE CENTER SIDEBAR NAV ───────── */

/* Center the whole group */
[data-testid="stSidebar"] div[role="radiogroup"] {
    display: flex;
    flex-direction: column;
    align-items: center !important;
    gap: 10px;
    border-left: 15px solid transparent; !important /* for consistent width */
}

/* 🔥 KEY FIX: shrink label width */
[data-testid="stSidebar"] div[role="radiogroup"] label {
    display: inline-flex !important;   /* not full width anymore */
    justify-content: center !important;
    align-items: center !important;

    width: fit-content !important;     /* 🔥 THIS fixes it */
    min-width: 220px;                  /* optional: uniform size */

    text-align: left !important;
    padding: 10px 16px !important;
    border-radius: 10px;
}
            
 /* ───────── REMOVE ALL SCROLLBARS ───────── */

/* Chrome, Edge, Safari */
::-webkit-scrollbar {
    width: 0px !important;
    height: 0px !important;
}

/* Firefox */
* {
    scrollbar-width: none !important;
}

/* Prevent horizontal scroll */
html, body, .stApp {
    overflow-x: hidden !important;
}

</style>
""", unsafe_allow_html=True)

############################################################
# COMPONENT HELPERS
############################################################

def kpi_card(label, value, subtitle, color, icon):

    palette = {
        "accent": ("#1B3FCC", "#EBF0FF"),
        "green":  ("#0C9E6B", "#E7F9F2"),
        "amber":  ("#D08700", "#FEF7E7"),
        "red":    ("#D42B2B", "#FEF0F0"),
        "teal":   ("#0891B2", "#E0F6FB"),
    }
    fg, bg = palette.get(color, palette["accent"])

    html = f"""
    <div style="
        background:#FFFFFF;
        border:1px solid #E4EAF4;
        border-radius:14px;
        padding:20px;
        height:148px;
        display:flex;
        flex-direction:column;
        justify-content:space-between;
        box-shadow:0 2px 8px rgba(13,27,62,.05);
        transition:all 0.2s ease;
        position:relative;
        overflow:hidden;
    ">
        <div style="
            position:absolute;top:-16px;right:-16px;
            width:80px;height:80px;border-radius:50%;
            background:{bg};opacity:0.6;
        "></div>
        <div style="display:flex;align-items:center;gap:10px;position:relative;">
            <div style="
                width:38px;height:38px;border-radius:10px;
                background:{bg};
                display:flex;align-items:center;justify-content:center;
                font-size:17px;flex-shrink:0;
            ">{icon}</div>
            <div style="font-size:11px;color:#8A97B8;font-weight:700;
                        text-transform:uppercase;letter-spacing:.07em;">
                {label}
            </div>
        </div>
        <div style="font-size:28px;font-weight:700;color:#0D1B3E;
                    letter-spacing:-.03em;line-height:1;position:relative;">
            {value}
        </div>
        <div style="font-size:11.5px;color:#8A97B8;position:relative;">
            {subtitle}
        </div>
    </div>
    """
    return html


def section_header(title, subtitle=""):
    return f"""
    <div style="margin:24px 0 16px 0;">
      <h2 style="font-family:'DM Sans',sans-serif;font-size:17px;font-weight:700;
                 color:#0D1B3E;letter-spacing:-.025em;margin:0 0 3px 0;">{title}</h2>
      {f'<p style="font-family:\'DM Sans\',sans-serif;font-size:13px;color:#8A97B8;margin:0;">{subtitle}</p>' if subtitle else ''}
    </div>"""


def badge(text, variant="default"):
    styles = {
        "default": ("background:#F0F4FB;color:#4A5878;border:1px solid #D8E0F0;"),
        "success": ("background:#E7F9F2;color:#0C9E6B;border:1px solid #9AE0C7;"),
        "warning": ("background:#FEF7E7;color:#D08700;border:1px solid #F0C968;"),
        "danger":  ("background:#FEF0F0;color:#D42B2B;border:1px solid #F5AAAA;"),
        "info":    ("background:#EBF0FF;color:#1B3FCC;border:1px solid #A8BEFF;"),
    }
    s = styles.get(variant, styles["default"])
    return f"""<span style="display:inline-block;padding:3px 10px;border-radius:99px;
                             font-family:'DM Sans',sans-serif;
                             font-size:11px;font-weight:700;letter-spacing:.03em;{s}">{text}</span>"""


def page_title(icon, title, subtitle):
    st.markdown(f"""
    <div style="
        background:linear-gradient(135deg, #FFFFFF 0%, #F4F6FB 100%);
        border:1px solid #E4EAF4;
        border-radius:18px;
        padding:28px 32px;
        margin-bottom:28px;
        box-shadow:0 2px 12px rgba(13,27,62,.06);
        display:flex;
        align-items:center;
        gap:20px;
        position:relative;
        overflow:hidden;
    ">
        <div style="
            position:absolute;right:-40px;top:-40px;
            width:180px;height:180px;border-radius:50%;
            background:linear-gradient(135deg,rgba(27,63,204,.06),rgba(67,56,202,.04));
        "></div>
        <div style="
            width:58px;height:58px;border-radius:14px;
            background:linear-gradient(140deg,#1B3FCC,#4338CA);
            display:flex;align-items:center;justify-content:center;
            font-size:24px;color:#FFFFFF;flex-shrink:0;
            box-shadow:0 6px 20px rgba(27,63,204,.30);
        ">{icon}</div>
        <div>
            <div style="
                font-family:'DM Sans',sans-serif;
                font-size:22px;font-weight:700;color:#0D1B3E;
                letter-spacing:-.03em;margin:0 0 4px 0;line-height:1.1;
            ">{title}</div>
            <div style="font-family:'DM Sans',sans-serif;font-size:13.5px;color:#8A97B8;margin:0;">
                {subtitle}
            </div>
        </div>
    </div>""", unsafe_allow_html=True)


############################################################
# LOAD DATA
############################################################

@st.cache_data(ttl=30)
def load_data():
    suppliers    = pd.read_csv("data/suppliers.csv")
    esg          = pd.read_csv("data/esg_metrics.csv")
    transactions = pd.read_csv("data/transactions.csv")
    return suppliers, esg, transactions

suppliers, esg, transactions = load_data()

############################################################
# BUILD PERFORMANCE DATASET
############################################################

performance = transactions.groupby("supplier_id").agg(
    avg_delay=("delivery_delay_days", "mean"),
    avg_defect=("defect_rate", "mean"),
    avg_cost_variance=("cost_variance", "mean")
).reset_index()

performance["risk_score"] = (
    performance["avg_delay"] * 0.4
    + performance["avg_defect"] * 100 * 0.4
    + abs(performance["avg_cost_variance"]) * 0.2
)

performance = performance.merge(
    suppliers[["supplier_id", "supplier_name", "country", "category"]],
    on="supplier_id"
)

############################################################
# PLOTLY THEME — SHARED
############################################################

PLOTLY_LAYOUT = dict(
    font=dict(family="DM Sans, sans-serif", color="#4A5878"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#F8FAFD",
    title_font=dict(family="DM Sans, sans-serif", size=15, color="#0D1B3E"),
    margin=dict(t=48, b=32, l=16, r=16),
    xaxis=dict(
        gridcolor="#EAF0FA",
        gridwidth=1,
        linecolor="#E4EAF4",
        tickfont=dict(size=12),
        title_font=dict(size=13),
    ),
    yaxis=dict(
        gridcolor="#EAF0FA",
        gridwidth=1,
        linecolor="#E4EAF4",
        tickfont=dict(size=12),
        title_font=dict(size=13),
    ),
    hoverlabel=dict(
        bgcolor="white",
        bordercolor="#E4EAF4",
        font_family="DM Sans, sans-serif",
        font_size=13,
    ),
    legend=dict(
        bgcolor="rgba(255,255,255,0.85)",
        bordercolor="#E4EAF4",
        borderwidth=1,
        font=dict(size=12),
    ),
)

############################################################
# SIDEBAR
############################################################

with st.sidebar:

    # ── Brand header ──────────────────────────────────────
    st.markdown("""
    <div style="padding:24px 16px 16px 16px;">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">
            <div style="
                width:40px;height:40px;border-radius:12px;
                background:linear-gradient(140deg,#1B3FCC,#4338CA);
                display:flex;align-items:center;justify-content:center;
                font-size:18px;color:#FFFFFF;flex-shrink:0;
                box-shadow:0 4px 12px rgba(27,63,204,.28);
            ">⬡</div>
            <div>
                <div style="
                    font-family:'DM Sans',sans-serif;
                    font-size:15px;font-weight:700;color:#0D1B3E;
                    letter-spacing:-.02em;line-height:1.15;
                ">
                    TCS Envirozone<sup style='font-size:10px;vertical-align:super;'>AI</sup> 4.0
                </div>
                <div style="font-family:'DM Sans',sans-serif;font-size:11.5px;color:#8A97B8;font-weight:500;line-height:1.3;margin-top:1px;">
                    Responsible Sourcing & Supplier Intelligence
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Divider + nav label
    st.markdown("""
    <div style="height:1px;background:#E4EAF4;margin:0 16px 14px 16px;"></div>
    <div style="
        font-family:'DM Sans',sans-serif;
        font-size:10px;font-weight:700;letter-spacing:.12em;
        text-transform:uppercase;color:#8A97B8;
        padding:0 16px;margin-bottom:6px;
    ">Navigation</div>
    """, unsafe_allow_html=True)

    # Nav radio
    page = st.radio(
        "Navigate",
        [
            "📄  Document Ingestion",
            "🔎  Data Explorer",
            "📊  Overview Dashboard",
            "⚠️  Risk Monitoring",
            "👾  Supplier Advisor AI"
        ],
        label_visibility="collapsed"
    )

    # Divider + status label
    st.markdown("""
    <div style="height:1px;background:#E4EAF4;margin:14px 16px 14px 16px;"></div>
    <div style="
        font-family:'DM Sans',sans-serif;
        font-size:10px;font-weight:700;letter-spacing:.12em;
        text-transform:uppercase;color:#8A97B8;
        padding:0 16px;margin-bottom:10px;
    ">System Status</div>
    """, unsafe_allow_html=True)

    history_df = pd.read_csv("data/document_history.csv")

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Suppliers",   len(suppliers))
        st.metric("Docs",        len(history_df))
    with c2:
        st.metric("Transactions", len(transactions))
        high_risk_count = len(performance[performance["risk_score"] > 8])
        st.metric("High Risk",   high_risk_count)



############################################################
# MATPLOTLIB STYLE
############################################################

CHART_STYLE = {
    "figure.facecolor":   "#FFFFFF",
    "axes.facecolor":     "#F8FAFD",
    "axes.edgecolor":     "#E4EAF4",
    "axes.labelcolor":    "#4A5878",
    "axes.labelsize":     11,
    "axes.titlesize":     13,
    "axes.titleweight":   "600",
    "axes.titlecolor":    "#0D1B3E",
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "axes.grid":          True,
    "grid.color":         "#EAF0FA",
    "grid.linestyle":     "--",
    "grid.alpha":         0.7,
    "xtick.color":        "#8A97B8",
    "ytick.color":        "#8A97B8",
    "xtick.labelsize":    10,
    "ytick.labelsize":    10,
    "font.family":        "sans-serif",
    "text.color":         "#0D1B3E",
    "patch.linewidth":    0,
}


############################################################
# ── PAGE: DOCUMENT INGESTION ──────────────────────────────
############################################################

if "📄" in page:

    page_title("📄", "Document Ingestion",
               "Upload and process supplier, ESG, and transaction PDF documents through the AI pipeline.")

    # Pipeline visual
    st.markdown("""
    <div style="
        background:#FFFFFF;border:1px solid #E4EAF4;border-radius:14px;
        padding:20px 28px;margin-bottom:28px;
        box-shadow:0 2px 8px rgba(13,27,62,.05);
    ">
        <div style="display:flex;align-items:center;justify-content:space-between;">
            <div style="text-align:center;flex:1;">
                <div style="
                    width:44px;height:44px;border-radius:12px;
                    background:#EBF0FF;margin:0 auto 8px auto;
                    display:flex;align-items:center;justify-content:center;font-size:20px;
                ">📤</div>
                <div style="font-size:12px;font-weight:600;color:#0D1B3E;margin-bottom:2px;">Upload</div>
                <div style="font-size:11px;color:#8A97B8;">PDF files</div>
            </div>
            <div style="flex:1;height:2px;background:linear-gradient(90deg,#E4EAF4,#A8BEFF);margin:0 8px;border-radius:2px;"></div>
            <div style="text-align:center;flex:1;">
                <div style="
                    width:44px;height:44px;border-radius:12px;
                    background:#EBF0FF;margin:0 auto 8px auto;
                    display:flex;align-items:center;justify-content:center;font-size:20px;
                ">☁️</div>
                <div style="font-size:12px;font-weight:600;color:#0D1B3E;margin-bottom:2px;">Blob</div>
                <div style="font-size:11px;color:#8A97B8;">Azure storage</div>
            </div>
            <div style="flex:1;height:2px;background:linear-gradient(90deg,#A8BEFF,#E4EAF4);margin:0 8px;border-radius:2px;"></div>
            <div style="text-align:center;flex:1;">
                <div style="
                    width:44px;height:44px;border-radius:12px;
                    background:#EBF0FF;margin:0 auto 8px auto;
                    display:flex;align-items:center;justify-content:center;font-size:20px;
                ">🔍</div>
                <div style="font-size:12px;font-weight:600;color:#0D1B3E;margin-bottom:2px;">Extract</div>
                <div style="font-size:11px;color:#8A97B8;">Doc Intelligence</div>
            </div>
            <div style="flex:1;height:2px;background:linear-gradient(90deg,#E4EAF4,#A8BEFF);margin:0 8px;border-radius:2px;"></div>
            <div style="text-align:center;flex:1;">
                <div style="
                    width:44px;height:44px;border-radius:12px;
                    background:#EBF0FF;margin:0 auto 8px auto;
                    display:flex;align-items:center;justify-content:center;font-size:20px;
                ">⚙️</div>
                <div style="font-size:12px;font-weight:600;color:#0D1B3E;margin-bottom:2px;">Process</div>
                <div style="font-size:11px;color:#8A97B8;">Structure data</div>
            </div>
            <div style="flex:1;height:2px;background:linear-gradient(90deg,#A8BEFF,#E4EAF4);margin:0 8px;border-radius:2px;"></div>
            <div style="text-align:center;flex:1;">
                <div style="
                    width:44px;height:44px;border-radius:12px;
                    background:#E7F9F2;margin:0 auto 8px auto;
                    display:flex;align-items:center;justify-content:center;font-size:20px;
                ">💾</div>
                <div style="font-size:12px;font-weight:600;color:#0D1B3E;margin-bottom:2px;">Store</div>
                <div style="font-size:11px;color:#8A97B8;">Update datasets</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Upload cards
    col1, col2, col3 = st.columns(3)

    def upload_card(title, icon, desc, col_bg="#EBF0FF"):
        st.markdown(f"""
        <div style="
            background:#FFFFFF;border:1px solid #E4EAF4;border-radius:14px;
            padding:18px;margin-bottom:10px;
            box-shadow:0 2px 8px rgba(13,27,62,.05);
        ">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
                <div style="
                    width:38px;height:38px;border-radius:10px;
                    background:{col_bg};
                    display:flex;align-items:center;justify-content:center;
                    font-size:18px;flex-shrink:0;
                ">{icon}</div>
                <div>
                    <div style="font-family:'DM Sans',sans-serif;font-weight:600;font-size:14px;color:#0D1B3E;">{title}</div>
                    <div style="font-family:'DM Sans',sans-serif;font-size:11.5px;color:#8A97B8;">{desc}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col1:
        upload_card("Supplier Document", "🏭", "Company & supplier data", "#EBF0FF")
        supplier_file = st.file_uploader(
            "Upload Supplier PDF",
            type=["pdf"],
            label_visibility="collapsed",
            key="sup"
        )

    with col2:
        upload_card("ESG Document", "🌿", "Environmental & social metrics", "#E7F9F2")
        esg_file = st.file_uploader(
            "Upload ESG PDF",
            type=["pdf"],
            label_visibility="collapsed",
            key="esg_up"
        )

    with col3:
        upload_card("Transaction Document", "💳", "Order & transaction records", "#FEF7E7")
        transaction_file = st.file_uploader(
            "Upload Transaction PDF",
            type=["pdf"],
            label_visibility="collapsed",
            key="txn"
        )

    # Processing state
    if "logs" not in st.session_state:
        st.session_state.logs = []

    def log(msg):
        st.session_state.logs.append(msg)

    # Run pipeline
    if supplier_file and esg_file and transaction_file:

        if st.button("🚀  Process Documents", use_container_width=True):

            progress = st.progress(0)
            status = st.empty()
            log_container = st.empty()

            def update_logs():
                log_container.markdown(
                    "<br>".join([f"• {l}" for l in st.session_state.logs]),
                    unsafe_allow_html=True
                )

            try:
                os.makedirs("uploads", exist_ok=True)

                status.markdown("**📤 Uploading files...**")
                supplier_path = os.path.join("uploads", supplier_file.name)
                esg_path = os.path.join("uploads", esg_file.name)
                transaction_path = os.path.join("uploads", transaction_file.name)

                for path, fobj in [
                    (supplier_path, supplier_file),
                    (esg_path, esg_file),
                    (transaction_path, transaction_file)
                ]:
                    with open(path, "wb") as f:
                        f.write(fobj.read())

                progress.progress(15)
                update_logs()

                status.markdown("**☁️ Uploading to Azure Blob...**")
                supplier_blob = upload_file_to_blob(supplier_path, supplier_file.name)
                esg_blob = upload_file_to_blob(esg_path, esg_file.name)
                transaction_blob = upload_file_to_blob(transaction_path, transaction_file.name)

                progress.progress(35)
                update_logs()

                status.markdown("**🔍 Extracting documents (Azure AI)...**")
                supplier_text = extract_document(supplier_blob)
                esg_text = extract_document(esg_blob)
                transaction_text = extract_document(transaction_blob)

                progress.progress(60)
                update_logs()

                status.markdown("**⚙️ Processing structured data...**")
                doc_type1, count1 = process_extracted_document(supplier_text)
                doc_type2, count2 = process_extracted_document(esg_text)
                doc_type3, count3 = process_extracted_document(transaction_text)

                progress.progress(80)
                update_logs()

                status.markdown("**🧾 Logging ingestion history...**")
                log_document(supplier_file.name, doc_type1, count1)
                log_document(esg_file.name, doc_type2, count2)
                log_document(transaction_file.name, doc_type3, count3)

                progress.progress(100)
                update_logs()

                status.markdown("### ✅ Pipeline Completed Successfully")

                st.markdown(f"""
                <div style="
                    background:#E7F9F2;border:1px solid #9AE0C7;
                    border-radius:12px;padding:20px;margin-top:10px;
                ">
                    <div style="font-family:'DM Sans',sans-serif;font-weight:700;color:#0C9E6B;
                                font-size:14px;margin-bottom:12px;display:flex;align-items:center;gap:8px;">
                        <span>✅</span> Documents Processed Successfully
                    </div>
                    <div style="display:flex;gap:28px;font-family:'DM Sans',sans-serif;font-size:13.5px;color:#0D1B3E;">
                        <div>🏭 Supplier: <b>{count1}</b> records</div>
                        <div>🌿 ESG: <b>{count2}</b> records</div>
                        <div>💳 Transactions: <b>{count3}</b> records</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                status.error(f"❌ Error: {str(e)}")

    # History table
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown(section_header("Processing History", "Recent document ingestion activity"),
            unsafe_allow_html=True)

    history = pd.read_csv("data/document_history.csv")
    history = history.sort_values("timestamp", ascending=False).reset_index(drop=True)
    history = history.head(9)

    history_display = history.rename(columns={
        "document_name": "Document Name",
        "document_type": "Type",
        "status": "Status",
        "records_added": "Records",
        "timestamp": "Processed At"
    })

    def render_table(df):
        html = '''<div style="background:#FFFFFF;border:1px solid #E4EAF4;border-radius:14px;
                              overflow:hidden;box-shadow:0 2px 8px rgba(13,27,62,.05);">'''
        html += '''<table style="width:100%;border-collapse:collapse;
                                 font-family:'DM Sans',sans-serif;font-size:13px;">'''
        html += '''<thead><tr style="background:#F8FAFD;">'''
        for col in df.columns:
            html += f'''<th style="text-align:left;padding:13px 16px;
                                   border-bottom:1px solid #E4EAF4;
                                   color:#8A97B8;font-weight:700;
                                   font-size:11px;text-transform:uppercase;
                                   letter-spacing:.06em;">{col}</th>'''
        html += '</tr></thead><tbody>'
        for _, row in df.iterrows():
            html += '''<tr style="transition:background 0.15s;"
                          onmouseover="this.style.background='#F4F6FB'"
                          onmouseout="this.style.background='white'">'''
            for val in row:
                html += f'''<td style="padding:13px 16px;border-bottom:1px solid #F0F4FA;
                                       color:#0D1B3E;font-size:13px;">{val}</td>'''
            html += '</tr>'
        html += '</tbody></table></div>'
        return html

    st.markdown(render_table(history_display), unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# DATA EXPLORER
# ─────────────────────────────────────────────────────────
elif "🔎" in page:

    page_title("🔎", "Data Explorer", "Browse and inspect raw supplier, ESG, and transaction datasets")

    dataset = st.segmented_control(
        "Select Dataset",
        ["Suppliers", "ESG", "Transactions"]
    )

    if dataset == "Suppliers":
        df = suppliers
    elif dataset == "ESG":
        df = esg
    else:
        df = transactions

    # Quick stats
    c1, c2 = st.columns(2)
    c1.metric("Total Rows", f"{len(df):,}")
    c2.metric("Columns", len(df.columns))

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    def render_table(df):
        html = '''<div style="background:#FFFFFF;border:1px solid #E4EAF4;border-radius:14px;
                              overflow:auto;box-shadow:0 2px 8px rgba(13,27,62,.05);">'''
        html += '''<table style="width:100%;border-collapse:collapse;
                                 font-family:'DM Sans',sans-serif;font-size:13px;">'''
        html += '''<thead><tr style="background:#F8FAFD;">'''
        for col in df.columns:
            html += f'''<th style="text-align:left;padding:12px 16px;
                                   border-bottom:1px solid #E4EAF4;
                                   color:#8A97B8;font-weight:700;
                                   font-size:11px;text-transform:uppercase;
                                   letter-spacing:.06em;white-space:nowrap;">{col}</th>'''
        html += '</tr></thead><tbody>'
        for _, row in df.iterrows():
            html += '''<tr style="transition:background 0.15s;"
                          onmouseover="this.style.background='#F4F6FB'"
                          onmouseout="this.style.background='white'">'''
            for val in row:
                html += f'''<td style="padding:11px 16px;border-bottom:1px solid #F0F4FA;
                                       color:#0D1B3E;font-size:13px;">{val}</td>'''
            html += '</tr>'
        html += '</tbody></table></div>'
        return html

    st.markdown(render_table(df.head(100)), unsafe_allow_html=True)


############################################################
# ── PAGE: OVERVIEW DASHBOARD ──────────────────────────────
############################################################

elif "📊" in page:

    page_title("📊", "Overview Dashboard", "High-level metrics and distribution insights across the supplier network")

    # KPI data
    total_suppliers = suppliers.shape[0]
    avg_esg         = round(esg["esg_score"].mean(), 1)
    avg_delay       = round(transactions["delivery_delay_days"].mean(), 1)
    avg_defect      = round(transactions["defect_rate"].mean() * 100, 2)
    high_risk_n     = len(performance[performance["risk_score"] > 8])

    # KPI row
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.markdown(kpi_card("Total Suppliers", total_suppliers, "Active in network", "accent", "🏭"), unsafe_allow_html=True)
    c2.markdown(kpi_card("Avg ESG Score", avg_esg, "Environmental & social", "green", "🌿"), unsafe_allow_html=True)
    c3.markdown(kpi_card("Avg Delay", f"{avg_delay}d", "Delivery performance", "amber", "🕐"), unsafe_allow_html=True)
    c4.markdown(kpi_card("Avg Defect Rate", f"{avg_defect}%", "Quality metric", "teal", "⚠️"), unsafe_allow_html=True)
    c5.markdown(kpi_card("High Risk", high_risk_n, "Require attention", "red", "🚨"), unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        if "country" in suppliers.columns:
            country_counts = (
                suppliers["country"]
                .value_counts()
                .reset_index()
                .head(7)
            )
            country_counts.columns = ["Country", "No. of Suppliers"]

            fig = px.bar(
                country_counts,
                x="No. of Suppliers",
                y="Country",
                orientation="h",
                title="Suppliers by Country",
                color_discrete_sequence=["#1B3FCC"],
            )
            PLOTLY_LAYOUT["yaxis"] = dict(autorange="reversed")
            fig.update_layout(**PLOTLY_LAYOUT)

            fig.update_traces(
                marker_color="#1B3FCC",
                marker_opacity=0.85,
                hovertemplate="<b>%{y}</b><br>Suppliers: %{x}<extra></extra>"
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if "esg_score" in esg.columns:
            fig = px.histogram(
                x=esg["esg_score"],
                nbins=20,
                title="ESG Score Distribution",
                labels={"x": "ESG Score", "y": "Suppliers"},
                color_discrete_sequence=["#1B3FCC"]
            )
            fig.update_layout(
            yaxis=dict(
                autorange=True,
                showgrid=False,
                zeroline=False,
                title="Number of Suppliers"
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            **{
                k: v for k, v in PLOTLY_LAYOUT.items()
                if k not in ["yaxis", "yaxis_title", "paper_bgcolor", "plot_bgcolor"]
            }
            )
            fig.update_traces(
                marker_color="#1B3FCC",
                marker_opacity=0.82,
                hovertemplate="<b>ESG Range:</b> %{x}<br><b>Suppliers:</b> %{y}<extra></extra>"
            )
            st.plotly_chart(fig, use_container_width=True)


############################################################
# ── PAGE: RISK MONITORING ─────────────────────────────────
############################################################

elif "⚠️" in page:

    page_title("⚠️", "Risk Monitoring", "Identify, segment, and investigate supplier risk exposure")

    df = performance.copy()
    df["risk_score"] = pd.to_numeric(df["risk_score"], errors="coerce")

    high_risk   = df[df["risk_score"] > 8]
    medium_risk = df[(df["risk_score"] > 5) & (df["risk_score"] <= 8)]
    low_risk    = df[df["risk_score"] <= 5]
    top_risk    = high_risk.sort_values("risk_score", ascending=False).head(10)

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(kpi_card("High Risk",      len(high_risk),   "Score > 8",     "red",    "🚨"), unsafe_allow_html=True)
    c2.markdown(kpi_card("Medium Risk",    len(medium_risk), "Score 5–8",     "amber",  "⚠️"), unsafe_allow_html=True)
    c3.markdown(kpi_card("Low Risk",       len(low_risk),    "Score ≤ 5",     "green",  "✅"), unsafe_allow_html=True)
    c4.markdown(kpi_card("Avg Risk Score", round(df["risk_score"].mean(), 2), "Fleet average", "teal", "📊"), unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # Charts row
    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(
            x=df["risk_score"],
            nbins=7,
            title="Risk Score Distribution",
            color_discrete_sequence=["#1B3FCC"]
        )
        fig.update_layout(
        xaxis=dict(
            title="Risk Score",
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            title="Number of Suppliers",
            showgrid=False,
            zeroline=False
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        **{k: v for k, v in PLOTLY_LAYOUT.items() if k not in ["xaxis", "yaxis", "plot_bgcolor", "paper_bgcolor"]},
    )
        fig.update_traces(
            marker_color="#1B3FCC",
            marker_opacity=0.82,
            hovertemplate="<b>Risk Score:</b> %{x}<br><b>Suppliers:</b> %{y}<extra></extra>"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        risk_counts = pd.DataFrame({
            "Risk Level": ["High", "Medium", "Low"],
            "No. of Suppliers": [len(high_risk), len(medium_risk), len(low_risk)]
        })
        color_map = {
            "High":   "#D42B2B",
            "Medium": "#D08700",
            "Low":    "#0C9E6B"
        }
        fig = px.pie(
            risk_counts,
            names="Risk Level",
            values="No. of Suppliers",
            hole=0.52,
            title="Risk Segmentation",
            color="Risk Level",
            color_discrete_map=color_map
        )
        fig.update_layout(**PLOTLY_LAYOUT)
        fig.update_traces(
            hovertemplate="<b>%{label}</b><br>Suppliers: %{value}<br>Share: %{percent}<extra></extra>",
            textfont=dict(family="DM Sans, sans-serif", size=13),
        )
        st.plotly_chart(fig, use_container_width=True)

     # TOP RISKY SUPPLIERS
    # -------------------------------

    top_risk = high_risk.sort_values("risk_score", ascending=False).head(10)

    fig = px.bar(
        top_risk,
        x="risk_score",
        y="supplier_name",   # ⚠️ make sure this column exists
        orientation="h",
        title="🚨 Top 10 High-Risk Suppliers",
        color_discrete_sequence=["#1B3FCC"]
    )

    PLOTLY_LAYOUT["yaxis"] = dict(autorange="reversed")
    fig.update_layout(
        xaxis_title="Risk Score",
        yaxis_title="Supplier", **PLOTLY_LAYOUT
    )


    fig.update_traces(
            marker_color="#1B3FCC",
            hovertemplate=
            "<b>Risk Score:</b> %{x}<br>" +
            "<b>Supplier:</b> %{y}<extra></extra>"
        )

    st.plotly_chart(fig, use_container_width=True)

    # Due Diligence Agent
    from backend.due_diligence_agent import run_due_diligence

    st.markdown(section_header("🧠 Supplier Due Diligence Agent",
                               "AI-powered deep analysis for any high-risk supplier"),
                unsafe_allow_html=True)

    supplier_list = top_risk["supplier_name"].unique()

    selected_supplier = st.selectbox(
        "Search supplier",
        supplier_list,
        index=None,
        placeholder="Select or search a supplier name..."
    )

    if st.button("Run Due Diligence"):
        with st.spinner("Running AI evaluation..."):
            result = run_due_diligence(selected_supplier, performance, esg, suppliers)

        st.markdown(f"""
        <div style="
            background:#FFFFFF;border:1px solid #E4EAF4;border-radius:14px;
            padding:24px;margin-top:16px;
            box-shadow:0 2px 12px rgba(13,27,62,.06);
        ">
            <div style="font-family:'DM Sans',sans-serif;font-size:18px;font-weight:700;
                        color:#0D1B3E;margin-bottom:16px;border-bottom:1px solid #F0F4FA;
                        padding-bottom:12px;">{result['supplier']}</div>
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:16px;">
                <div style="background:#ebeef8;border:1px solid #ebeef8;border-radius:10px;padding:14px;">
                    <div style="font-size:10px;font-weight:700;color:#1B3FCC;text-transform:uppercase;
                                letter-spacing:.07em;margin-bottom:5px;">Operational Risk</div>
                    <div style="font-size:14px;font-weight:600;color:#0D1B3E;">{result['op_risk']}</div>
                </div>
                <div style="background:#ebeef8;border:1px solid #ebeef8;border-radius:10px;padding:14px;">
                    <div style="font-size:10px;font-weight:700;color:#1B3FCC;text-transform:uppercase;
                                letter-spacing:.07em;margin-bottom:5px;">ESG Risk</div>
                    <div style="font-size:14px;font-weight:600;color:#0D1B3E;">{result['esg_risk']}</div>
                </div>
                <div style="background:#ebeef8;border:1px solid #ebeef8;border-radius:10px;padding:14px;">
                    <div style="font-size:10px;font-weight:700;color:#1B3FCC;text-transform:uppercase;
                                letter-spacing:.07em;margin-bottom:5px;">Overall Risk</div>
                    <div style="font-size:14px;font-weight:600;color:#0D1B3E;">{result['overall']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**⚠️ Key Issues**")
        for i in result["issues"]:
            st.write(f"- {i}")

        st.markdown("**💡 Recommendation**")
        st.write(result["ai_summary"])


############################################################
# ── PAGE: AI INSIGHTS ─────────────────────────────────────
############################################################

elif "👾" in page:

    page_title(
        "🤖",
        "Supplier Advisor AI",
        "AI-powered guidance across supplier risk, ESG, and performance"
    )

    # Example prompts
    st.markdown("""
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:20px;">
        <div style="background:#F4F6FB;border:1px solid #E4EAF4;border-radius:99px;
                    padding:7px 15px;font-family:'DM Sans',sans-serif;
                    font-size:12.5px;color:#4A5878;font-weight:500;
                    transition:all 0.15s ease;cursor:default;">
            💬 Which suppliers have the highest risk scores?
        </div>
        <div style="background:#F4F6FB;border:1px solid #E4EAF4;border-radius:99px;
                    padding:7px 15px;font-family:'DM Sans',sans-serif;
                    font-size:12.5px;color:#4A5878;font-weight:500;cursor:default;">
            💬 Which countries have the most high-risk suppliers?
        </div>
        <div style="background:#F4F6FB;border:1px solid #E4EAF4;border-radius:99px;
                    padding:7px 15px;font-family:'DM Sans',sans-serif;
                    font-size:12.5px;color:#4A5878;font-weight:500;cursor:default;">
            💬 Recommend low-risk suppliers for sourcing
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Chat state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    def format_ai_response(text):
        text = re.sub(r'#+', '', text)
        text = text.replace("**", "")
        text = re.sub(r'\n(?!-|\*)', ' ', text)
        text = re.sub(r'\(\s+', '(', text)
        text = re.sub(r'\s+\)', ')', text)
        text = re.sub(r'\b\d+\.\s*', '', text)
        text = text.replace("Key Insights", "\n\n🧠 Key Insights\n")
        text = text.replace("Risk Alerts", "\n\n⚠️ Risk Alerts\n")
        text = text.replace("Recommendations", "\n\n💡 Recommendations\n")
        return text.strip()

    chat_container = st.container()

    with chat_container:
        if not st.session_state.messages:
            st.markdown("""
            <div style="
                text-align:center;padding:52px 24px;
                background:#F8FAFD;border:1.5px dashed #D2DBF0;
                border-radius:16px;margin-bottom:16px;
            ">
                <div style="
                    width:64px;height:64px;border-radius:18px;
                    background:linear-gradient(140deg,#1B3FCC,#4338CA);
                    margin:0 auto 16px auto;
                    display:flex;align-items:center;justify-content:center;
                    font-size:28px;color:white;
                    box-shadow:0 8px 24px rgba(27,63,204,.28);
                ">🤖</div>
                <div style="font-family:'DM Sans',sans-serif;font-size:16px;font-weight:700;
                            color:#0D1B3E;margin-bottom:6px;">
                    Supplier Advisor AI Ready
                </div>
                <div style="font-family:'DM Sans',sans-serif;font-size:13.5px;color:#8A97B8;max-width:360px;margin:0 auto;line-height:1.5;">
                    Ask anything about supplier risk, ESG performance, or operational insights.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    with st.chat_message("user", avatar="🧑‍💼"):
                        st.write(message["content"])
                else:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.markdown(format_ai_response(message["content"]))

    # Chat input
    question = st.chat_input("Ask about your supplier network...")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.write(question)

        with st.spinner("Analyzing supplier data..."):
            response = ask_supplier_ai(question, performance)

        st.session_state.messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant"):
            st.markdown("""
            <div style="font-family:'DM Sans',sans-serif;font-size:11.5px;color:#8A97B8;margin-bottom:6px;">
            AI-generated insights based on supplier performance data
            </div>
            """, unsafe_allow_html=True)
            st.markdown(format_ai_response(response))

        st.rerun()


############################################################
# FOOTER
############################################################

if "👾" not in page:
    st.markdown("""
    <div style="
        margin-top:48px;
        padding:16px 24px;
        background:#FFFFFF;
        border:1px solid #E4EAF4;
        border-radius:14px;
        display:flex;
        align-items:center;
        justify-content:space-between;
        box-shadow:0 1px 4px rgba(13,27,62,.04);
    ">
        <div style="font-family:'DM Sans',sans-serif;font-size:13px;color:#8A97B8;display:flex;align-items:center;gap:8px;">
            <div style="
                width:26px;height:26px;border-radius:7px;
                background:linear-gradient(140deg,#1B3FCC,#4338CA);
                display:flex;align-items:center;justify-content:center;
                font-size:12px;color:white;
            ">⬡</div>
            <span>
                <strong style="color:#0D1B3E;font-weight:700;">
                    TCS Envirozone<sup style='font-size:9px;'>AI</sup> 4.0
                </strong>
                &nbsp;·&nbsp; Responsible Sourcing &amp; Supplier Intelligence
            </span>
        </div>
        <div style="display:flex;align-items:center;gap:14px;">
            <span style="font-family:'DM Sans',sans-serif;font-size:12px;color:#8A97B8;">
                Azure Document Intelligence &amp; Gemini 2.5 Flash
            </span>
            <div style="
                background:#E7F9F2;border:1px solid #9AE0C7;border-radius:99px;
                padding:4px 12px;
                display:flex;align-items:center;gap:6px;
            ">
                <div style="width:6px;height:6px;border-radius:50%;background:#0C9E6B;
                            box-shadow:0 0 0 2px rgba(12,158,107,.2);"></div>
                <span style="font-family:'DM Sans',sans-serif;font-size:11.5px;font-weight:700;color:#0C9E6B;">Live</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)