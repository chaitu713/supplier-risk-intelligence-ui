import re
import sys
import os

from altair import value
from altair import value
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ─────────────────────────────────────────────
   ROOT DESIGN TOKENS
───────────────────────────────────────────── */
:root {
    
    /* Base */
    --bg:        #F7F9FC;
    --surface:   #FFFFFF;
    --surface-2: #F1F5F9;

    /* Borders */
    --border:    #E6EAF2;
    --border-2:  #D6DCE8;

    /* Text */
    --text-1:    #0F172A;
    --text-2:    #475569;
    --text-3:    #94A3B8;

    /* Primary */
    --primary:   #2563EB;
    --primary-2: #1E40AF;
    --primary-l: #EFF6FF;

    /* Semantic */
    --green:     #059669;
    --green-l:   #ECFDF5;

    --amber:     #D97706;
    --amber-l:   #FFFBEB;

    --red:       #DC2626;
    --red-l:     #FEF2F2;

    /* Radius */
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;

    /* Shadows */
    --shadow-sm: 0 1px 2px rgba(0,0,0,0.04);
    --shadow-md: 0 4px 12px rgba(0,0,0,0.06);
    --shadow-lg: 0 10px 30px rgba(0,0,0,0.08);
    
    color-scheme: light !important;
}

/* REMOVE TOP SPACE */
.block-container {
    padding-top: 1.5rem !important;
}

/* Sidebar container */
section[data-testid="stSidebar"] > div {
    padding-top: 0rem !important;
}

/* Remove extra spacing above first element */
section[data-testid="stSidebar"] div:first-child {
    margin-top: 0 !important;
    padding-top: 0 !important;
}   

/* ─────────────────────────────────────────────
   GLOBAL
───────────────────────────────────────────── */
html, body,
.stApp {
    background: var(--bg) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text-1) !important;
}

/* ─────────────────────────────────────────────
   SIDEBAR
───────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

/* ─────────────────────────────────────────────
   TYPOGRAPHY
───────────────────────────────────────────── */
h1 {
    font-size: 24px !important;
    font-weight: 700 !important;
}

h2 {
    font-size: 18px !important;
    font-weight: 600 !important;
}

p, label {
    font-size: 14px !important;
    color: var(--text-2) !important;
}

/* ─────────────────────────────────────────────
   CARDS
───────────────────────────────────────────── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 20px;
    box-shadow: var(--shadow-sm);
    transition: all 0.2s ease;
}

.card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}

/* ─────────────────────────────────────────────
   METRICS
───────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 18px;
}

[data-testid="stMetricValue"] {
    font-size: 28px !important;
    font-weight: 700 !important;
}

/* ─────────────────────────────────────────────
   BUTTONS
───────────────────────────────────────────── */
.stButton > button {
    background: var(--primary) !important;
    color: white !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
}

.stButton > button:hover {
    background: var(--primary-2) !important;
}

/* ─────────────────────────────────────────────
   INPUTS
───────────────────────────────────────────── */
input, textarea {
    border-radius: 8px !important;
    border: 1px solid var(--border-2) !important;
}

/* ─────────────────────────────────────────────
   DATAFRAME
───────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: var(--radius-md);
    border: 1px solid var(--border);
}

/* ─────────────────────────────────────────────
   CHAT
───────────────────────────────────────────── */
[data-testid="stChatMessage"] {
    border-radius: 12px;
    border: 1px solid var(--border);
}

/* ─────────────────────────────────────────────
   SCROLLBAR
───────────────────────────────────────────── */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background: var(--border-2);
    border-radius: 10px;
}
            
/* ===================== FIXES ===================== */

/* REMOVE TOP BLACK HEADER */
[data-testid="stHeader"] {
    display: none !important;
}

/* FIX TOP SPACING */
[data-testid="stAppViewContainer"] {
    padding-top: 0 !important;
}

/* FORCE LIGHT MODE */
html, body {
    background-color: #F7F9FC !important;
}

/* FILE UPLOADER FIX */
[data-testid="stFileUploader"],
[data-testid="stFileUploader"] * {
    background: #FFFFFF !important;
    color: #0F172A !important;
    border-color: #E6EAF2 !important;
}

/* DROPZONE */
[data-testid="stFileUploaderDropzone"] {
    background: #F8FAFC !important;
    border: 1.5px dashed #CBD5F5 !important;
    border-radius: 12px !important;
}

/* ───────── DATAFRAME LIGHT THEME FIX ───────── */

/* Outer container */
[data-testid="stDataFrame"] {
    background: #FFFFFF !important;
    border: 1px solid #E6EAF2 !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
}

/* Toolbar */
[data-testid="stDataFrameToolbar"] {
    background: #F8FAFC !important;
    border-bottom: 1px solid #E6EAF2 !important;
}

/* Canvas background (critical fix) */
[data-testid="stDataFrame"] canvas {
    background: #FFFFFF !important;
}

/* Header styling */
[data-testid="stDataFrame"] div[role="columnheader"] {
    background: #F8FAFC !important;
    color: #475569 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}

/* Cell text */
[data-testid="stDataFrame"] div[role="gridcell"] {
    color: #0F172A !important;
    font-size: 13px !important;
}

/* Row hover */
[data-testid="stDataFrame"] div[role="row"]:hover {
    background: #F1F5F9 !important;
}
            
/* FIX UPLOADER TEXT CONSISTENCY */
[data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stFileUploaderDropzoneInstructions"] small {
    font-family: 'Sora', sans-serif !important;
    font-size: 13.5px !important;
    color: #475569 !important;
}

/* MAIN TEXT */
[data-testid="stFileUploaderDropzoneInstructions"] {
    font-size: 14px !important;
    font-weight: 500 !important;
}

/* FILE NAME TEXT */
[data-testid="stFileUploaderFile"] span {
    font-size: 13px !important;
    font-family: 'Sora', sans-serif !important;
}

/* FORCE BUTTON TEXT WHITE */
/* 🔥 HARD OVERRIDE BUTTON */
.stButton > button {
    background: #2563EB !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    height: 48px !important;
    border-radius: 10px !important;
    border: none !important;
}

/* FIX INNER TEXT (important for Streamlit) */
.stButton > button * {
    color: #FFFFFF !important;
}
            
/* FILE CHIP CONTAINER */
[data-testid="stFileUploaderFile"] {
    background: #FFFFFF !important;
    border: 1px solid #E6EAF2 !important;
    border-radius: 10px !important;
    padding: 10px 12px !important;
    margin-top: 8px !important;
}

/* FILE TEXT */
[data-testid="stFileUploaderFileData"] span {
    font-size: 13px !important;
    color: #0F172A !important;
    font-family: 'Sora', sans-serif !important;
}

/* FILE SIZE TEXT */
[data-testid="stFileUploaderFileData"] small {
    color: #64748B !important;
    font-size: 11px !important;
}

/* REMOVE BUTTON (X) */
[data-testid="stFileUploaderDeleteBtn"] button {
    background: transparent !important;
    color: #64748B !important;
}

/* REMOVE BUTTON HOVER */
[data-testid="stFileUploaderDeleteBtn"] button:hover {
    color: #DC2626 !important;
}
            
[data-testid="stFileUploaderDropzone"] {
    background: #F8FAFC !important;
    border: 1.5px dashed #CBD5F5 !important;
    border-radius: 14px !important;
    padding: 20px !important;
    transition: all 0.2s ease !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    background: #EFF6FF !important;
    border-color: #2563EB !important;
}
            
/* FIX BROWSE FILES BUTTON */
[data-testid="stFileUploader"] button {
    font-size: 13px !important;
    font-weight: 500 !important;
    font-family: 'Sora', sans-serif !important;
    padding: 6px 14px !important;
}
            
/* FILE NAME */
[data-testid="stFileUploaderFileData"] span {
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* FILE SIZE */
[data-testid="stFileUploaderFileData"] small {
    font-size: 11px !important;
}
            
/* DRAG & DROP TEXT */
[data-testid="stFileUploaderDropzoneInstructions"] span {
    font-size: 14px !important;
    font-weight: 500 !important;
}

/* SUBTEXT */
[data-testid="stFileUploaderDropzoneInstructions"] small {
    font-size: 12px !important;
}

/* FORCE OVERRIDE FILE CHIP TEXT */

[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] * {
    font-family: 'Sora', sans-serif !important;
}

/* FILE NAME (MAIN FIX) */
[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] span {
    font-size: 12px !important;
    font-weight: 400 !important;
    color: #1E293B !important;
}

/* FILE SIZE */
[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] small {
    font-size: 10.5px !important;
    color: #94A3B8 !important;
}

/* REDUCE OVERALL CHIP HEIGHT */
[data-testid="stFileUploaderFile"] {
    padding: 6px 8px !important;
}
            
/* ───────── SIDEBAR BUTTON FIX ───────── */
            
/* Navigation buttons */
[data-testid="stSidebar"] .stButton {
    width: 100%;
    display: flex;
    justify-content: center;  /* centers button inside container */
}

/* Actual button styling */
[data-testid="stSidebar"] .stButton > button {
    width: 85%;              /* control width */
    text-align: center;      /* center text */
    justify-content: center; /* center icon + text */
    border-radius: 10px;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #e2e8f0;
    transform: translateY(-1px);
}

            
section[data-testid="stSidebar"] {
    overflow-y: auto;  /* keep scroll only if needed */
}

section[data-testid="stSidebar"]::-webkit-scrollbar {
    width: 4px;
}

section[data-testid="stSidebar"]::-webkit-scrollbar-thumb {
    background: transparent;   /* hide visually */
}

/* ───────── UNIFORM NAV BUTTONS ───────── */
            
[data-testid="stSidebar"] .stRadio {
    width: 100%;
    display: flex;
    justify-content: center;   /* ✅ CENTER GROUP */
}

[data-testid="stSidebar"] .stRadio label {
    display: flex !important;
    align-items: center !important;
    width: 100% !important;
    min-height: 44px !important;
    padding: 10px 14px !important;
    border-radius: 10px !important;
    box-sizing: border-box !important;
    
}
                
            
/* ───────── TRUE CENTER SIDEBAR NAV ───────── */

/* Center the whole group */
[data-testid="stSidebar"] div[role="radiogroup"] {
    display: flex;
    flex-direction: column;
    align-items: center !important;
    gap: 10px;
    border-left: 30px solid transparent; !important /* for consistent width */
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

/* Hover */
[data-testid="stSidebar"] .stRadio label:hover {
    background: #F1F5F9 !important;
}

/* ACTIVE ITEM (same size, just colored) */
[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: #EFF6FF !important;
    border: 1px solid #BFDBFE !important;
}

/* Active text */
[data-testid="stSidebar"] .stRadio label:has(input:checked) span {
    color: #2563EB !important;
    font-weight: 600 !important;
}
            
[data-testid="stSidebar"] .stRadio > label {
    display: none !important;
}
            
/* ───────── HIDE RADIO CIRCLE ───────── */

/* ───────── HIDE RADIO CIRCLE (WORKING) ───────── */

/* Hide the circle element */
[data-testid="stSidebar"] .stRadio label > div:first-child {
    display: none !important;
}

/* Remove extra spacing caused by circle */
[data-testid="stSidebar"] .stRadio label {
    padding-left: 12px !important;
}

/* INPUT FIX (LIGHT THEME) */

[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #E6EAF2 !important;
    border-radius: 10px !important;
} 

/* ───────── SELECTBOX BORDER FIX ───────── */

/* Normal state */
[data-testid="stSelectbox"] div[data-baseweb="select"] {
    border: 1px solid #00008B !important;
    border-radius: 10px !important;
    background: #FFFFFF !important;
}

/* Focus state (when clicked) */
[data-testid="stSelectbox"] div[data-baseweb="select"]:focus-within {
    border: 1px solid #00008B !important;   /* 🔥 BLUE */
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1) !important;
}  

/* ───────── REMOVE INPUT CARET / BAR ───────── */

[data-testid="stSelectbox"] input {
    caret-color: transparent !important;   /* hides blinking cursor */
}

/* Remove weird inner divider */
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    border: none !important;
} 

/* ───────── REMOVE BASEWEB SCROLL INDICATOR ───────── */

[data-baseweb="menu"] {
    overflow: hidden !important;
}

/* Also target inner scroll container */
[data-baseweb="menu"] > div {
    overflow: hidden !important;
}

[data-baseweb="menu"] * {
    scrollbar-width: none !important;
}

[data-baseweb="menu"] *::-webkit-scrollbar {
    display: none !important;
}      

[data-baseweb="menu"] {
    max-height: none !important;
}   

/* ───────── HIDE SIDEBAR TOGGLE BUTTON ───────── */

[data-testid="stSidebarCollapseButton"] {
    display: none !important;
}
            
.kpi-wrapper div[data-testid="stHorizontalBlock"] > div {
    background: #FFFFFF;
    border: 1px solid #E6EAF2;
    border-radius: 16px;
    padding: 16px;
}

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
            
            
/* ───────── TRUE CENTER (PIXEL PERFECT) ───────── */
            
/* ───────── CENTER LABEL + VALUE INSIDE METRIC ───────── */

/* Center the whole inner block (you already have this) */
[data-testid="stMetric"] > div {
    position: absolute !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    width: 100%;
    text-align: center;
}

/* 🔥 FIX: Label container alignment */
[data-testid="stMetricLabel"] {
    width: 100% !important;
    display: flex !important;
    justify-content: center !important;   /* center horizontally */
    align-items: center !important;
    text-align: center !important;
}

/* 🔥 FIX: Actual label text */
[data-testid="stMetricLabel"] p {
    text-align: center !important;
    width: 100%;
}

/* Value already centered but enforce it */
[data-testid="stMetricValue"] {
    text-align: center !important;
    width: 100%;
}

[data-testid="stMetric"] {
    position: relative !important;
    height: 80px !important;
    padding: 0 !important;
}

/* Target inner container */
[data-testid="stMetric"] > div {
    position: absolute !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    width: 100%;
    text-align: center;
}



</style>
""", unsafe_allow_html=True)

############################################################
# COMPONENT HELPERS
############################################################

def kpi_card(label, value, subtitle, color, icon):

    colors = {
        "accent": "#3B82F6",
        "green": "#10B981",
        "amber": "#F59E0B",
        "red": "#EF4444"
    }

    c = colors.get(color, "#3B82F6")

    html = f"""
    <div style="
        height:140px;
        display:flex;
        flex-direction:column;
        justify-content:space-between;
        background:#FFFFFF;
        border:1px solid #E6EAF2;
        border-radius:16px;
        padding:16px;
    ">
        <div style="display:flex; align-items:center; gap:10px;">
            <div style="
                width:40px;
                height:40px;
                border-radius:10px;
                background:{c}20;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:18px;
            ">
                {icon}
            </div>

            <div style="
                font-size:12px;
                color:#64748B;
                font-weight:600;
                text-transform:uppercase;
            ">
                {label}
            </div>
        </div>

        <div style="
            font-size:26px;
            font-weight:700;
            color:#0F172A;
        ">
            {value}
        </div>

        <div style="
            font-size:12px;
            color:#94A3B8;
        ">
            {subtitle}
        </div>
    </div>
    """

    return html


def section_header(title, subtitle=""):
    return f"""
    <div style="margin-bottom:20px;">
      <h2 style="font-size:18px;font-weight:700;color:#1C2B4A;
                 letter-spacing:-.02em;margin:0 0 4px 0;">{title}</h2>
      {f'<p style="font-size:13px;color:#8A9ABB;margin:0;">{subtitle}</p>' if subtitle else ''}
    </div>"""


def badge(text, variant="default"):
    styles = {
        "default": ("background:#F0F3FA;color:#4A5A78;border:1px solid #E2E6F0;"),
        "success": ("background:#E4F5EE;color:#0D8F5E;border:1px solid #A5DFC5;"),
        "warning": ("background:#FEF3E2;color:#B95E00;border:1px solid #FDD8A0;"),
        "danger":  ("background:#FDEAEA;color:#C01F1F;border:1px solid #F9BABA;"),
        "info":    ("background:#EBF0FD;color:#1A56DB;border:1px solid #BFCFFA;"),
    }
    s = styles.get(variant, styles["default"])
    return f"""<span style="display:inline-block;padding:3px 9px;border-radius:99px;
                             font-size:11px;font-weight:600;{s}">{text}</span>"""


def page_title(icon, title, subtitle):
    st.markdown(f"""
    <div style="
        background:#FFFFFF; border:1px solid #E2E6F0; border-radius:14px;
        padding:28px 32px; margin-bottom:28px;
        box-shadow:0 1px 3px rgba(28,43,74,.06);
        display:flex; align-items:center; gap:20px;
    ">
      <div style="
          width:56px; height:56px; border-radius:14px;
          background:linear-gradient(135deg,#1A56DB,#4338CA);
          display:flex; align-items:center; justify-content:center;
          font-size:24px; color:#ffffff; flex-shrink:0;
      ">{icon}</div>
      <div>
        <h5 style="font-size:22px;font-weight:700;color:#1C2B4A;
                   margin:0 0 4px 0;letter-spacing:-.03em;">{title}</h5>
        <p style="font-size:13.5px;color:#8A9ABB;margin:0;">{subtitle}</p>
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
# SIDEBAR
############################################################

with st.sidebar:
    # Logo / Brand
    st.markdown("""
    <div style="padding:20px 8px 8px 8px;">
      <div style="
          display:flex; align-items:center; gap:12px; margin-bottom:6px;
      ">
        <div style="
            width:38px; height:38px; border-radius:10px;
            background:linear-gradient(135deg,#1A56DB,#4338CA);
            display:flex; align-items:center; justify-content:center;
            font-size:18px; color:#ffffff; flex-shrink:0;
        ">⬡</div>
        <div>
          <div style="font-size:22px;font-weight:700;color:#1C2B4A;
                      letter-spacing:-.02em;line-height:1.1;">
              TCS Envirozone<sup style='font-size:15px;'>AI</sup> 4.0
          </div>
          <div style="font-size:14px;color:#8A9ABB;font-weight:500;">
              Responsible Sourcing & Supplier Intelligence
          </div>
        </div>
      </div>
    </div>
    <div style="height:1px;background:#E2E6F0;margin:8px 0 16px 0;"></div>
    <div style="font-size:10px;font-weight:700;letter-spacing:.12em;
                text-transform:uppercase;color:#8A9ABB;padding:0 8px;
                margin-bottom:8px;">Main Navigation</div>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────
    # SIDEBAR NAV (STABLE RADIO VERSION)
    # ─────────────────────────────────────────────

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

    st.markdown("""
    <div style="height:1px;background:#E2E6F0;margin:20px 0 16px 0;"></div>
    <div style="font-size:10px;font-weight:700;letter-spacing:.12em;
                text-transform:uppercase;color:#8A9ABB;padding:0 8px;
                margin-bottom:12px;">System Status</div>
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
    "axes.edgecolor":     "#E2E6F0",
    "axes.labelcolor":    "#4A5A78",
    "axes.labelsize":     11,
    "axes.titlesize":     13,
    "axes.titleweight":   "600",
    "axes.titlecolor":    "#1C2B4A",
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "axes.grid":          True,
    "grid.color":         "#EAEEf6",
    "grid.linestyle":     "--",
    "grid.alpha":         0.7,
    "xtick.color":        "#8A9ABB",
    "ytick.color":        "#8A9ABB",
    "xtick.labelsize":    10,
    "ytick.labelsize":    10,
    "font.family":        "sans-serif",
    "text.color":         "#1C2B4A",
    "patch.linewidth":    0,
}

############################################################
# ── PAGE: DOCUMENT INGESTION (UPGRADED) ──────────────────
############################################################

if "📄" in page:

    page_title("📄", "Document Ingestion",
               "Upload and process supplier, ESG, and transaction PDF documents through the AI pipeline.")

    # ─────────────────────────────────────────────
    # PIPELINE VISUAL
    # ─────────────────────────────────────────────
    st.markdown("""
    <div style="
        display:flex; align-items:center; justify-content:space-between;
        background:#FFFFFF; border:1px solid #E2E6F0;
        border-radius:12px; padding:18px 24px; margin-bottom:24px;
    ">
        <div style="text-align:center;">
            <div style="font-size:20px;">📤</div>
            <div style="font-size:11px;color:#8A9ABB;">Upload</div>
        </div>
        <div style="flex:1;height:2px;background:#E2E6F0;margin:0 10px;"></div>
        <div style="text-align:center;">
            <div style="font-size:20px;">🔍</div>
            <div style="font-size:11px;color:#8A9ABB;">Extract</div>
        </div>
        <div style="flex:1;height:2px;background:#E2E6F0;margin:0 10px;"></div>
        <div style="text-align:center;">
            <div style="font-size:20px;">⚙️</div>
            <div style="font-size:11px;color:#8A9ABB;">Process</div>
        </div>
        <div style="flex:1;height:2px;background:#E2E6F0;margin:0 10px;"></div>
        <div style="text-align:center;">
            <div style="font-size:20px;">💾</div>
            <div style="font-size:11px;color:#8A9ABB;">Store</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────
    # UPDATED UPLOAD UI
    # ─────────────────────────────────────────────

    col1, col2, col3 = st.columns(3)

    def upload_card(title, icon):
        st.markdown(f"""
        <div style="
            background:#FFFFFF;
            border:1px solid #E6EAF2;
            border-radius:16px;
            padding:18px;
            margin-bottom:10px;
            box-shadow:0 2px 8px rgba(0,0,0,0.04);
        ">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
                <div style="
                    width:36px;height:36px;
                    border-radius:10px;
                    background:#EFF6FF;
                    display:flex;align-items:center;justify-content:center;
                    font-size:18px;
                ">{icon}</div>
                <div style="font-weight:600;font-size:14px;color:#0F172A;">
                    {title}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col1:
        upload_card("Supplier Document", "🏭")
        supplier_file = st.file_uploader(
            "Upload Supplier PDF",
            type=["pdf"],
            label_visibility="collapsed",
            key="sup"
        )

    with col2:
        upload_card("ESG Document", "🌿")
        esg_file = st.file_uploader(
            "Upload ESG PDF",
            type=["pdf"],
            label_visibility="collapsed",
            key="esg_up"
        )

    with col3:
        upload_card("Transaction Document", "💳")
        transaction_file = st.file_uploader(
            "Upload Transaction PDF",
            type=["pdf"],
            label_visibility="collapsed",
            key="txn"
        )

    # ─────────────────────────────────────────────
    # PROCESSING STATE
    # ─────────────────────────────────────────────
    if "logs" not in st.session_state:
        st.session_state.logs = []

    def log(msg):
        st.session_state.logs.append(msg)

    # ─────────────────────────────────────────────
    # RUN PIPELINE
    # ─────────────────────────────────────────────
    if supplier_file and esg_file and transaction_file:

        if st.button("🚀 Process Documents", use_container_width=True):

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

                # STEP 1 — SAVE FILES
                status.markdown("**📤 Uploading files...**")
                # log("Saving uploaded files locally")

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

                # STEP 2 — UPLOAD TO BLOB
                status.markdown("**☁️ Uploading to Azure Blob...**")
                #log("Uploading files to Azure Blob Storage")

                supplier_blob = upload_file_to_blob(supplier_path, supplier_file.name)
                esg_blob = upload_file_to_blob(esg_path, esg_file.name)
                transaction_blob = upload_file_to_blob(transaction_path, transaction_file.name)

                progress.progress(35)
                update_logs()

                # STEP 3 — EXTRACT
                status.markdown("**🔍 Extracting documents (Azure AI)...**")
                #log("Running Azure Document Intelligence extraction")

                supplier_text = extract_document(supplier_blob)
                #log("Supplier document extracted")

                esg_text = extract_document(esg_blob)
                #log("ESG document extracted")

                transaction_text = extract_document(transaction_blob)
                #log("Transaction document extracted")

                progress.progress(60)
                update_logs()

                # STEP 4 — PROCESS
                status.markdown("**⚙️ Processing structured data...**")
                #log("Transforming extracted data")

                doc_type1, count1 = process_extracted_document(supplier_text)
                #log(f"Processed Supplier: {count1} records")

                doc_type2, count2 = process_extracted_document(esg_text)
                #log(f"Processed ESG: {count2} records")

                doc_type3, count3 = process_extracted_document(transaction_text)
                #log(f"Processed Transactions: {count3} records")

                progress.progress(80)
                update_logs()

                # STEP 5 — LOG HISTORY
                status.markdown("**🧾 Logging ingestion history...**")
                #log("Writing to document history")

                log_document(supplier_file.name, doc_type1, count1)
                log_document(esg_file.name, doc_type2, count2)
                log_document(transaction_file.name, doc_type3, count3)

                progress.progress(100)
                update_logs()

                # SUCCESS UI
                status.markdown("### ✅ Pipeline Completed Successfully")

                st.markdown(f"""
                <div style="
                    background:#E4F5EE;border:1px solid #A5DFC5;
                    border-radius:12px;padding:18px;margin-top:10px;
                ">
                    <div style="font-weight:600;color:#0D8F5E;margin-bottom:8px;">
                        Documents Processed
                    </div>
                    <div style="display:flex;gap:30px;font-size:14px;">
                        <div>📁 Supplier: <b>{count1}</b></div>
                        <div>🌿 ESG: <b>{count2}</b></div>
                        <div>💳 Transactions: <b>{count3}</b></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                status.error(f"❌ Error: {str(e)}")

    # ─────────────────────────────────────────────
    # HISTORY TABLE
    # ─────────────────────────────────────────────
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    st.markdown(section_header("Processing History"),
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

        html = '<div style="background:#FFFFFF;border:1px solid #E6EAF2;border-radius:12px;overflow:hidden;">'
        html += '<table style="width:100%;border-collapse:collapse;font-family:Inter,sans-serif;font-size:13px;">'

        # HEADER
        html += '<thead style="background:#F8FAFC;"><tr>'
        for col in df.columns:
            html += f'<th style="text-align:left;padding:12px;border-bottom:1px solid #E6EAF2;color:#475569;font-weight:600;">{col}</th>'
        html += '</tr></thead>'

        # BODY
        html += '<tbody>'
        for _, row in df.iterrows():
            html += '<tr style="transition:background 0.2s;" onmouseover="this.style.background=\'#F8FAFC\'" onmouseout="this.style.background=\'white\'">'
            for val in row:
                html += f'<td style="padding:12px;border-bottom:1px solid #F1F5F9;color:#0F172A;">{val}</td>'
            html += '</tr>'
        html += '</tbody></table></div>'

        return html


    st.markdown(render_table(history_display), unsafe_allow_html=True)

   

# --------------------------------------------------
# DATA EXPLORER
# --------------------------------------------------
elif "🔎" in page:

    st.title("🔎 Data Explorer")

    # Dataset selector
    dataset = st.segmented_control(
    "Select Dataset",
    ["Suppliers", "ESG", "Transactions"]
)

    # Pick dataset
    if dataset == "Suppliers":
        df = suppliers
    elif dataset == "ESG":
        df = esg
    else:
        df = transactions
    # -------------------------------
    # QUICK STATS
    # -------------------------------
    col1, col2 = st.columns(2)
    col1.metric("Rows", len(df))
    col2.metric("Columns", len(df.columns))

    # -------------------------------
    # CLEAN TABLE (HTML)
    # -------------------------------
    def render_table(df):
        html = '<div style="background:#FFFFFF;border:1px solid #E6EAF2;border-radius:12px;overflow:hidden;">'
        html += '<table style="width:100%;border-collapse:collapse;font-size:13px;">'

        # Header
        html += '<thead style="background:#F8FAFC;"><tr>'
        for col in df.columns:
            html += f'<th style="padding:12px;border-bottom:1px solid #E6EAF2;text-align:left;">{col}</th>'
        html += '</tr></thead>'

        # Rows
        html += '<tbody>'
        for _, row in df.iterrows():
            html += '<tr>'
            for val in row:
                html += f'<td style="padding:12px;border-bottom:1px solid #F1F5F9;">{val}</td>'
            html += '</tr>'
        html += '</tbody></table></div>'

        return html

    st.markdown(render_table(df.head(100)), unsafe_allow_html=True)

############################################################
# ── PAGE: OVERVIEW DASHBOARD ──────────────────────────────
############################################################

# --------------------------------------------------
# OVERVIEW DASHBOARD (CLEAN VERSION)
# --------------------------------------------------
elif "📊" in page:

    st.title("📊 Overview Dashboard")
    st.markdown('<div class="kpi-wrapper">', unsafe_allow_html=True)
    # -------------------------------
    # KPI DATA
    # -------------------------------
    total_suppliers = suppliers.shape[0]
    avg_esg         = round(esg["esg_score"].mean(), 1)
    avg_delay       = round(transactions["delivery_delay_days"].mean(), 1)
    avg_defect      = round(transactions["defect_rate"].mean() * 100, 2)
    high_risk_n     = len(performance[performance["risk_score"] > 8])

    # -------------------------------
    # KPI CARDS (SAFE HTML)
    # -------------------------------
    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("🏭 Total Suppliers", total_suppliers)
    c2.metric("🌿 Avg ESG Score", avg_esg)
    c3.metric("🕐 Avg Delivery Delay", f"{avg_delay}d")
    c4.metric("⚠️ Avg Defect Rate", f"{avg_defect}%")
    c5.metric("🚨 High Risk Suppliers", high_risk_n)

    # -------------------------------
    # CHARTS
    # -------------------------------
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
            x = "No. of Suppliers",
            y = "Country",
            orientation="h",
            title= "🌍 Suppliers by Country",
        )

        fig.update_layout(
            yaxis=dict(autorange="reversed")
        )

        fig.update_traces(
            hovertemplate=
            "<b>No. of Suppliers:</b> %{x}<br>" +
            "<b>Country:</b> %{y}<extra></extra>"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        if "esg_score" in esg.columns:
            fig = px.histogram(
            x = esg["esg_score"],
            nbins=20,
            title="🌱 ESG Score Distribution",
            labels={
                "x": "ESG Score",     # 🔥 X-axis name
                "y": "Number of Suppliers"  # 🔥 Y-axis name
            }
        )
            
        fig.update_layout(
            yaxis_title="Number of Suppliers"
        )

        fig.update_traces(
            hovertemplate=
            "<b>ESG Score Range:</b> %{x}<br>" +
            "<b>Suppliers:</b> %{y}<extra></extra>"
        )

        st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# RISK MONITORING (USING PERFORMANCE TABLE)
# --------------------------------------------------
elif "⚠️" in page:

    st.title("⚠️ Risk Monitoring")

    df = performance.copy()
    df["risk_score"] = pd.to_numeric(df["risk_score"], errors="coerce")

    # -------------------------------
    # YOUR EXISTING LOGIC (KEEP THIS)
    # -------------------------------
    high_risk = df[df["risk_score"] > 8]
    medium_risk = df[(df["risk_score"] > 5) & (df["risk_score"] <= 8)]
    low_risk = df[df["risk_score"] <= 5]

    # -------------------------------
    # KPIs
    # -------------------------------
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🚨 High Risk", len(high_risk))
    c2.metric("⚠️ Medium Risk", len(medium_risk))
    c3.metric("✅ Low Risk", len(low_risk))
    c4.metric("📊 Avg Risk Score", round(df["risk_score"].mean(), 2))

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # -------------------------------
    # CHARTS
    # -------------------------------
    col1, col2 = st.columns(2)

    # 📊 Risk Distribution
    with col1:
        fig = px.histogram(
            x=df["risk_score"],
            nbins=7,
            title="📊 Risk Score Distribution"
        )

        fig.update_layout(
            xaxis_title="Risk Score",
            yaxis_title="Number of Suppliers"
        )

        fig.update_traces(
            hovertemplate=
            "<b>Risk Score Range:</b> %{x}<br>" +
            "<b>No. of Suppliers:</b> %{y}<extra></extra>"
        )

        st.plotly_chart(fig, use_container_width=True)

    # 🥧 Risk Segmentation
    with col2:
        risk_counts = pd.DataFrame({
            "Risk Level": ["High", "Medium", "Low"],
            "No. of Suppliers": [len(high_risk), len(medium_risk), len(low_risk)]
        })

        # 🔥 Color mapping
        color_map = {
            "High": "#DC2626",    # red
            "Medium": "#F59E0B",  # amber
            "Low": "#10B981"      # green
        }

        fig = px.pie(
            risk_counts,
            names="Risk Level",
            values="No. of Suppliers",
            hole=0.5,
            title="🥧 Risk Segmentation",
            color = "Risk Level",
            color_discrete_map=color_map
        )

        # 🔥 Clean tooltip
        fig.update_traces(
            hovertemplate=
            "<b>Risk Level:</b> %{label}<br>" +
            "<b>Suppliers:</b> %{value}<br>" +
            "<b>Percentage:</b> %{percent}<extra></extra>"
        )


        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # -------------------------------
    # TOP RISKY SUPPLIERS
    # -------------------------------

    top_risk = high_risk.sort_values("risk_score", ascending=False).head(10)

    fig = px.bar(
        top_risk,
        x="risk_score",
        y="supplier_name",   # ⚠️ make sure this column exists
        orientation="h",
        title="🚨 Top 10 High-Risk Suppliers"
    )

    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        xaxis_title="Risk Score",
        yaxis_title="Supplier"
    )

    fig.update_traces(
            hovertemplate=
            "<b>Risk Score:</b> %{x}<br>" +
            "<b>Supplier:</b> %{y}<extra></extra>"
        )

    st.plotly_chart(fig, use_container_width=True)


############################################################
# ── PAGE: AI INSIGHTS ─────────────────────────────────────
############################################################

# --------------------------------------------------
# 🧠 SUPPLIER COPILOT
# --------------------------------------------------
elif "👾" in page:

    page_title(
        "🤖",
        "Supplier Advisor AI",
        "AI-powered guidance across supplier risk, ESG, and performance"
    )

    # -------------------------------
    # EXAMPLE PROMPTS
    # -------------------------------
    st.markdown("""
    <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:20px;">
      <div style="background:#F0F3FA;border:1px solid #E2E6F0;border-radius:8px;
                  padding:8px 14px;font-size:12.5px;color:#4A5A78;font-weight:500;">
          💬 Which suppliers have the highest risk scores?
      </div>
      <div style="background:#F0F3FA;border:1px solid #E2E6F0;border-radius:8px;
                  padding:8px 14px;font-size:12.5px;color:#4A5A78;font-weight:500;">
          💬 Which countries have the most high-risk suppliers?
      </div>
      <div style="background:#F0F3FA;border:1px solid #E2E6F0;border-radius:8px;
                  padding:8px 14px;font-size:12.5px;color:#4A5A78;font-weight:500;">
          💬 Recommend low-risk suppliers for sourcing
      </div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------
    # CHAT STATE
    # -------------------------------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # -------------------------------
    # FORMAT AI RESPONSE
    # -------------------------------

    def format_ai_response(text):

        # Remove all markdown symbols like ### anywhere
        text = re.sub(r'#+', '', text)

        text = text.replace("**", "")
        text = text.replace("**", "")

    # Fix broken lines inside sentences
        text = re.sub(r'\n(?!-|\*)', ' ', text)

    # Fix bracket spacing
        text = re.sub(r'\(\s+', '(', text)
        text = re.sub(r'\s+\)', ')', text)

    # Remove numbering
        text = re.sub(r'\b\d+\.\s*', '', text)

    # Clean section headers
        text = text.replace("Key Insights", "\n\n🧠 Key Insights\n")
        text = text.replace("Risk Alerts", "\n\n⚠️ Risk Alerts\n")
        text = text.replace("Recommendations", "\n\n💡 Recommendations\n")

        return text.strip()

    # -------------------------------
    # CHAT UI
    # -------------------------------
    chat_container = st.container()

    with chat_container:
        if not st.session_state.messages:
            st.markdown("""
            <div style="
                text-align:center; padding:48px 24px;
                background:#F8FAFD; border:1.5px dashed #CDD3E3;
                border-radius:14px; margin-bottom:16px;
            ">
              <div style="font-size:36px; margin-bottom:12px;">🤖</div>
              <div style="font-size:15px;font-weight:600;color:#1C2B4A;margin-bottom:6px;">
                  Supplier Advisor AI Ready
              </div>
              <div style="font-size:13px;color:#8A9ABB;">
                  Ask questions about supplier risk, ESG performance, or operational insights.
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

    # -------------------------------
    # USER INPUT
    # -------------------------------
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
            <div style="font-size:12px;color:#94A3B8;margin-bottom:6px;">
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
        margin-top: 40px;
        padding: 18px 24px;
        background: #FFFFFF;
        border: 1px solid #E2E6F0;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    ">
      <div style="font-size:12.5px;color:#8A9ABB;">
          <strong style="color:#1C2B4A;">TCS Envirozone<sup>AI</sup> 4.0</strong>
          &nbsp;·&nbsp; Responsible Sourcing & Supplier Intelligence
      </div>
      <div style="display:flex;align-items:center;gap:16px;">
        <span style="font-size:11.5px;color:#8A9ABB;">Built using Azure Document Intelligence & Gemini 2.5 Flash</span>
        <div style="
            background:#E4F5EE;border:1px solid #A5DFC5;border-radius:6px;
            padding:4px 10px;font-size:11px;font-weight:600;color:#0D8F5E;
        ">● Live</div>
      </div>
    </div>
    """, unsafe_allow_html=True)