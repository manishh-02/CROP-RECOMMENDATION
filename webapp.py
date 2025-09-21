import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import os
import warnings
from PIL import Image
import time

warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(
    page_title="AgriVerse Pro: Smart Crop Recommendation",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS for interactive gradients, transitions, and glowing effects
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

/* Base typography */
body, .css-1d391kg, .stMarkdown, .stTextInput>div>input {
    font-family: 'Poppins', sans-serif !important;
    color: #1B2A41 !important;
}

/* Main header with gradient text glow */
.main-header {
    font-size: 3.8rem !important;
    font-weight: 700 !important;
    text-align: center !important;
    margin: 3rem 0 2rem 0 !important;
    background: linear-gradient(45deg, #28a745, #20c997);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: textGlow 3s ease-in-out infinite alternate;
}

@keyframes textGlow {
    0% { filter: drop-shadow(0 0 10px #20c997); }
    100% { filter: drop-shadow(0 0 20px #28a745); }
}

/* Info section with subtle background gradient and shine */
.info-section {
    background: linear-gradient(135deg, #f5f9f8, #d7ede8);
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(40, 167, 69, 0.3);
    padding: 3rem;
    margin: 3rem 0;
    position: relative;
    overflow: hidden;
    transition: transform 0.3s ease;
}
.info-section:hover {
    transform: translateY(-10px);
}

.info-section::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(40, 167, 69, 0.08), transparent);
    animation: shine 3s infinite;
    z-index: 0;
}

@keyframes shine {
    0% { transform: translate(-100%, -100%) rotate(45deg); }
    100% { transform: translate(100%, 100%) rotate(45deg); }
}

.info-section h3 {
    position: relative;
    z-index: 1;
    color: #14532d;
    font-size: 2.8rem;
    font-weight: 700;
    margin-bottom: 1rem;
    text-shadow: 1px 1px 6px rgba(0,0,0,0.2);
}

.info-section p {
    position: relative;
    z-index: 1;
    font-size: 1.3rem;
    line-height: 1.7;
    font-weight: 500;
    color: #234d26dd;
    text-shadow: 1px 1px 3px rgba(255,255,255,0.6);
}

/* Feature Boxes */
.feature-box {
    background: #fff;
    border-radius: 20px;
    border: 3px solid #28a745;
    box-shadow: 0 8px 25px rgba(40, 167, 69, 0.2);
    padding: 2.5rem;
    margin: 1.5rem 1rem !important;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.17, 0.67, 0.83, 0.67);
    position: relative;
    overflow: hidden;
}

.feature-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    height: 100%;
    width: 100%;
    background: linear-gradient(90deg, transparent, #20c99766, transparent);
    transition: left 0.5s ease-in-out;
    z-index: 0;
}

.feature-box:hover::before {
    left: 100%;
}

.feature-box:hover {
    box-shadow: 0 15px 45px rgba(40, 167, 69, 0.4);
    border-color: #20c997;
    transform: translateY(-8px) scale(1.05);
}

.feature-box h4 {
    position: relative;
    z-index: 1;
    font-size: 1.8rem;
    color: #166534;
    font-weight: 700;
    margin-bottom: 1rem;
    text-shadow: 1px 1px 4px rgba(0,0,0,0.15);
}

.feature-box p {
    position: relative;
    z-index: 1;
    font-weight: 600;
    font-size: 1.2rem;
    color: #276749dd;
}

/* Parameter gauges */
.parameters-section {
    background: #f9fff9;
    border-radius: 25px;
    border: 4px solid #16a34a;
    padding: 3rem;
    margin: 3rem 0;
    box-shadow: 0 15px 40px rgba(40, 167, 69, 0.1);
}

.section-header {
    position: relative;
    font-size: 2.8rem;
    font-weight: 700;
    text-align: center;
    color: #14532d;
    border-bottom: 5px solid #20c997;
    padding-bottom: 1rem;
    margin-bottom: 3rem;
}

.section-header::after {
    content: '';
    position: absolute;
    bottom: -7px;
    left: 50%;
    transform: translateX(-50%);
    width: 120px;
    height: 5px;
    background: linear-gradient(90deg, #20c997, #28a745);
    animation: pulse 3s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* Metric gauges */
.metric-container {
    background: white;
    border-radius: 15px;
    border: 3px solid #52b788;
    padding: 1.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 4px 12px rgba(40, 167, 69, 0.15);
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

.metric-container:hover {
    box-shadow: 0 10px 30px rgba(40, 167, 69, 0.4);
    border-color: #38a169;
    transform: translateY(-5px);
}

.metric-label {
    font-weight: 600;
    font-size: 1.2rem;
    color: #166534;
    margin-bottom: 0.5rem;
}

.metric-value {
    font-weight: 700;
    font-size: 2.2rem;
    color: #16a34a;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.metric-description {
    font-style: italic;
    color: #4ade80;
    margin-top: 0.5rem;
}

/* Prediction box */
.prediction-box {
    background: linear-gradient(135deg, #059669, #047857);
    border-radius: 25px;
    color: white;
    padding: 3rem;
    margin: 3rem 0;
    font-size: 1.6rem;
    text-align: center;
    box-shadow: 0 12px 35px rgba(5, 150, 105, 0.7);
    animation: bounceIn 0.8s ease-out;
    position: relative;
    border: 4px solid #22c55e;
}

@keyframes bounceIn {
    0% { transform: scale(0.5); opacity: 0; }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); opacity: 1; }
}

.prediction-box h1 {
    font-size: 3.5rem;
    margin: 1rem 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
}

.prediction-box h2 {
    font-weight: 700;
    margin-bottom: 0.5rem;
}

/* Crop info */
.crop-info-section {
    background: linear-gradient(135deg, #6b46c1, #7c3aed);
    border-radius: 20px;
    color: white;
    padding: 3rem;
    margin: 3rem 0;
    box-shadow: 0 8px 30px rgba(124, 58, 237, 0.7);
}

.crop-info-header {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 2rem;
    border-bottom: 4px solid rgba(255, 255, 255, 0.5);
    padding-bottom: 1rem;
}

.crop-metric-card {
    background: rgba(110, 64, 170, 0.85);
    border-radius: 15px;
    padding: 2rem;
    margin: 1rem;
    text-align: center;
    box-shadow: 0 6px 15px rgba(110, 64, 170, 0.7);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 2px solid white;
}

.crop-metric-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 12px 25px rgba(156, 71, 243, 0.85);
    border-color: #e0c3fc;
}

.crop-metric-label {
    font-weight: 600;
    font-size: 1.3rem;
    opacity: 0.85;
    margin-bottom: 0.5rem;
}

.crop-metric-value {
    font-size: 2rem;
    font-weight: 700;
    text-shadow: 2px 2px 5px rgba(0,0,0,0.3);
}

/* Additional recommendations */
.recommendations-section {
    background: linear-gradient(135deg, #facc15, #eab308);
    border-radius: 20px;
    padding: 3rem;
    margin: 3rem 0;
    box-shadow: 0 12px 30px rgba(250, 204, 21, 0.7);
    color: #333;
}

.recommendations-header {
    text-align: center;
    font-weight: 700;
    font-size: 2rem;
    margin-bottom: 2rem;
    color: #1a202c;
    text-shadow: 1px 1px 2px rgba(255,255,255,0.5);
}

.recommendations-content {
    background: rgba(255, 255, 255, 0.85);
    border-radius: 15px;
    padding: 2rem;
    border: 2px solid #d97706;
    box-shadow: 0 6px 18px rgba(217, 119, 6, 0.3);
}

.recommendations-list li {
    margin: 1rem 0;
    padding: 1rem 1.5rem;
    border-left: 5px solid #d97706;
    background: #f59e0b1a;
    font-weight: 600;
    font-size: 1.2rem;
    transition: all 0.3s ease;
    border-radius: 8px;
}

.recommendations-list li:hover {
    background: #fbbf24;
    color: white;
    border-left-width: 8px;
    box-shadow: 0 4px 8px rgba(255, 191, 36, 0.7);
}

/* Scrollbar for cleaner experience */
::-webkit-scrollbar {
    width: 12px;
}
::-webkit-scrollbar-track {
    background: #e2e8f0;
    border-radius: 10px;
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #047857, #22c55e);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #065f46, #16a34a);
}

/* Expander spacing fix to eliminate overlap */
.stExpander {
    margin-top: 6rem !important;
    margin-bottom: 6rem !important;
    padding: 2rem !important;
}

.stExpander > div {
    background: white !important;
    border-radius: 20px !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1) !important;
    border: 3px solid #94a3b8 !important;
    padding: 2rem !important;
}

/* Utility fade-in animation */
.fade-in {
    animation: fadeIn 1s ease forwards;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# The rest of your backend and app logic remains unchanged as before.
# Use your existing load_data(), train_and_save_model(), create_interactive_gauge(), predict_crop(), show_crop_image(), display_crop_info(), main() functions here.

# Just replace your current CSS code block with the above CSS and keep backend functions the same.

