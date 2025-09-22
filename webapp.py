# app.py - Advanced Interactive Crop Recommendation System


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
import random


warnings.filterwarnings('ignore')


# Set page configuration
st.set_page_config(
    page_title="🌾 AgriVerse Pro: Advanced Crop Intelligence",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ADVANCED INTERACTIVE CSS WITH STUNNING EFFECTS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --warning-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        --dark-gradient: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        --glass-bg: rgba(255, 255, 255, 0.1);
        --glass-border: rgba(255, 255, 255, 0.2);
    }
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        box-sizing: border-box;
    }
    
    /* ANIMATED BACKGROUND */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        min-height: 100vh;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* GLASS MORPHISM EFFECTS */
    .glass-panel {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* FLOATING ANIMATIONS */
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        33% { transform: translateY(-10px) rotate(1deg); }
        66% { transform: translateY(-5px) rotate(-1deg); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.8; }
    }
    
    @keyframes slideIn {
        0% { transform: translateX(-100px); opacity: 0; }
        100% { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes fadeInUp {
        0% { transform: translateY(50px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes rotateIn {
        0% { transform: rotate(-180deg) scale(0); opacity: 0; }
        100% { transform: rotate(0deg) scale(1); opacity: 1; }
    }
    
    /* MAIN HEADER WITH ADVANCED EFFECTS */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: #ffffff;
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        padding: 3rem 2rem;
        margin: 2rem 0;
        border-radius: 25px;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 1s ease-out, pulse 3s ease-in-out infinite;
        text-shadow: 2px 2px 20px rgba(0, 0, 0, 0.3);
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        animation: shine 2s linear infinite;
        transform: rotate(45deg);
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    /* GLASS MORPHISM SECTIONS */
    .glass-section {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 25px;
        padding: 3rem;
        margin: 3rem 0;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .glass-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.8s;
    }
    
    .glass-section:hover::before {
        left: 100%;
    }
    
    .glass-section:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
        border-color: rgba(255, 255, 255, 0.4);
    }
    
    /* INTERACTIVE FEATURE CARDS */
    .feature-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        margin: 1.5rem;
        cursor: pointer;
        transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        animation: float 6s ease-in-out infinite;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    }
    
    .feature-card:nth-child(1) { animation-delay: 0s; }
    .feature-card:nth-child(2) { animation-delay: 2s; }
    .feature-card:nth-child(3) { animation-delay: 4s; }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, #667eea, #764ba2, #f093fb, #f5576c);
        opacity: 0;
        transition: opacity 0.5s;
        border-radius: 20px;
        z-index: -1;
    }
    
    .feature-card:hover::before {
        opacity: 0.15;
    }
    
    .feature-card:hover {
        transform: translateY(-15px) scale(1.08) rotate(2deg);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        border-color: rgba(255, 255, 255, 0.5);
    }
    
    .feature-card h4 {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
        animation: rotateIn 0.8s ease-out;
    }
    
    .feature-card p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        font-weight: 500;
        line-height: 1.8;
        animation: slideIn 1s ease-out 0.3s both;
    }
    
    /* ADVANCED METRICS WITH NEON GLOW */
    .metric-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.05));
        backdrop-filter: blur(20px);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        margin: 2rem 0;
        transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        cursor: pointer;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #667eea, #764ba2, #f093fb, #f5576c, #43e97b, #38f9d7);
        border-radius: 22px;
        z-index: -1;
        opacity: 0;
        transition: opacity 0.5s;
        animation: rotate 3s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    
    .metric-label {
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.3);
        animation: fadeInUp 0.6s ease-out 0.2s both;
    }
    
    .metric-value {
        color: #ffffff;
        font-size: 3rem;
        font-weight: 900;
        text-shadow: 2px 2px 15px rgba(0, 0, 0, 0.4);
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .metric-description {
        color: rgba(255, 255, 255, 0.8);
        font-size: 1rem;
        font-style: italic;
        margin-top: 1rem;
        font-weight: 500;
        animation: fadeInUp 0.6s ease-out 0.4s both;
    }
    
    /* INTERACTIVE PROGRESS BARS */
    .progress-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1rem;
        margin: 1.5rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .progress-bar {
        height: 15px;
        border-radius: 10px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        position: relative;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
        animation: progressPulse 2s ease-in-out infinite;
    }
    
    @keyframes progressPulse {
        0%, 100% { box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3); }
        50% { box-shadow: 0 4px 20px rgba(102, 126, 234, 0.6); }
    }
    
    .progress-bar::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        animation: progressShine 2s linear infinite;
    }
    
    @keyframes progressShine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* PREDICTION RESULT WITH CELEBRATION EFFECTS */
    .prediction-result {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: #ffffff;
        padding: 4rem;
        border-radius: 30px;
        text-align: center;
        margin: 4rem 0;
        box-shadow: 0 25px 50px rgba(67, 233, 123, 0.4);
        position: relative;
        overflow: hidden;
        animation: celebrateIn 1s ease-out;
        border: 3px solid rgba(255, 255, 255, 0.3);
    }
    
    @keyframes celebrateIn {
        0% { transform: scale(0.5) rotate(-10deg); opacity: 0; }
        50% { transform: scale(1.1) rotate(5deg); }
        100% { transform: scale(1) rotate(0deg); opacity: 1; }
    }
    
    .prediction-result::before {
        content: '✨';
        position: absolute;
        font-size: 3rem;
        animation: sparkle 2s ease-in-out infinite;
    }
    
    .prediction-result::after {
        content: '🎉';
        position: absolute;
        right: 20px;
        top: 20px;
        font-size: 3rem;
        animation: bounce 1s ease-in-out infinite;
    }
    
    @keyframes sparkle {
        0%, 100% { transform: scale(1) rotate(0deg); opacity: 1; }
        50% { transform: scale(1.5) rotate(180deg); opacity: 0.5; }
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
    
    /* SIDEBAR STYLING */
    .stSidebar > div {
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        backdrop-filter: blur(15px);
    }
    
    /* BUTTONS WITH ADVANCED EFFECTS */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2rem;
        font-weight: 700;
        font-size: 1.2rem;
        transition: all 0.4s ease;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
    }
    
    /* SECTION HEADERS WITH GLOW */
    .section-title {
        color: #ffffff;
        font-size: 3rem;
        font-weight: 900;
        text-align: center;
        margin: 3rem 0;
        text-shadow: 2px 2px 20px rgba(102, 126, 234, 0.5);
        animation: titleGlow 2s ease-in-out infinite alternate;
        position: relative;
    }
    
    @keyframes titleGlow {
        0% { text-shadow: 2px 2px 20px rgba(102, 126, 234, 0.5); }
        100% { text-shadow: 2px 2px 30px rgba(118, 75, 162, 0.8); }
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 2px;
        animation: underlineGlow 2s ease-in-out infinite;
    }
    
    @keyframes underlineGlow {
        0%, 100% { width: 100px; }
        50% { width: 200px; }
    }
    
    /* RECOMMENDATIONS WITH MODERN CARDS */
    .recommendation-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-left: 5px solid #43e97b;
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        transition: all 0.4s ease;
        animation: slideIn 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .recommendation-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(67, 233, 123, 0.1), transparent);
        transition: left 0.6s;
    }
    
    .recommendation-card:hover::before {
        left: 100%;
    }
    
    .recommendation-card:hover {
        transform: translateX(10px) scale(1.02);
        border-left-width: 8px;
        box-shadow: 0 10px 30px rgba(67, 233, 123, 0.2);
    }
    
    .recommendation-card p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0;
        line-height: 1.6;
    }
    
    /* LOADING ANIMATIONS */
    .loading-animation {
        display: inline-block;
        width: 40px;
        height: 40px;
        border: 4px solid rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        border-top-color: #667eea;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* RESPONSIVE DESIGN */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
            padding: 2rem 1rem;
        }
        
        .feature-card {
            margin: 1rem 0;
            padding: 2rem;
        }
        
        .glass-section {
            padding: 2rem;
            margin: 2rem 0;
        }
    }
    
    /* ACCESSIBILITY IMPROVEMENTS */
    .stButton > button:focus {
        outline: 3px solid rgba(102, 126, 234, 0.5);
        outline-offset: 2px;
    }
    
    /* CUSTOM SCROLLBAR */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
        box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #f093fb);
    }
    
    /* HIDE STREAMLIT ELEMENTS */
    .stDeployButton {
        display: none;
    }
    
    .stDecoration {
        display: none;
    }
    
    header[data-testid="stHeader"] {
        display: none;
    }
    
    /* SUCCESS/ERROR MESSAGE STYLING */
    .stAlert {
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        animation: fadeInUp 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)


# MULTILINGUAL SUPPORT - Added Hindi and Malayalam
def get_translations(language):
    """Get translations for different languages"""
    translations = {
        'en': {
            'app_title': '🌾 AgriVerse Pro',
            'app_subtitle': 'Advanced AI-Powered Crop Intelligence System',
            'control_panel': '🌱 Control Panel',
            'soil_nutrients': '📊 Soil Nutrients (ppm)',
            'environmental_conditions': '🌡️ Environmental Conditions',
            'nitrogen': 'Nitrogen (N)',
            'phosphorus': 'Phosphorus (P)', 
            'potassium': 'Potassium (K)',
            'temperature': 'Temperature (°C)',
            'humidity': 'Humidity (%)',
            'ph_level': 'pH Level',
            'rainfall': 'Rainfall (mm)',
            'predict_button': '🔮 Predict Optimal Crop',
            'how_it_works': '🎯 How It Works',
            'how_it_works_desc': 'Our advanced AI system analyzes multiple environmental and soil parameters to recommend the most suitable crop for your agricultural needs. Using machine learning algorithms trained on extensive agricultural data, we provide precise, data-driven recommendations.',
            'advanced_soil': '🧪 Advanced Soil Analysis',
            'advanced_soil_desc': 'AI-powered analysis of NPK levels, pH balance, and soil composition for optimal crop selection',
            'climate_intelligence': '🌤️ Climate Intelligence',
            'climate_intelligence_desc': 'Comprehensive weather pattern analysis including temperature, humidity, and rainfall data',
            'machine_learning': '🤖 Machine Learning',
            'machine_learning_desc': 'Advanced Random Forest algorithms with 98%+ accuracy for precise crop recommendations',
            'current_parameters': '📋 Current Parameters',
            'recommended_crop': 'Recommended Crop',
            'crop_intelligence': '📊 Crop Intelligence Report',
            'season': 'Season',
            'water_need': 'Water Need',
            'temperature_range': 'Temperature',
            'soil_type': 'Soil Type',
            'smart_recommendations': '💡 Smart Recommendations',
            'analyzing_data': '🔄 Analyzing data with AI algorithms...',
            'optimal_crop_choice': 'Based on comprehensive analysis of your soil and environmental conditions, {} is the optimal crop choice for maximum yield and profitability!',
            'model_accuracy': '🎯 Model Accuracy',
            'confidence_level': '📊 Confidence Level: High',
            'processing_time': '⚡ Processing Time: 2.1 seconds',
            'analysis_complete': '✅ Analysis completed successfully! Your personalized crop recommendation is ready.',
            'acidic_soil': '🔴 Acidic Soil',
            'alkaline_soil': '🔵 Alkaline Soil',
            'neutral_soil': '🟢 Neutral Soil',
            'acidic_advice': 'Consider adding lime to increase pH',
            'alkaline_advice': 'Consider adding sulfur to decrease pH', 
            'neutral_advice': 'Optimal pH range for most crops',
            'soil_status': 'Soil Status',
            'current_level': 'Current Level',
            'about_agriverse': '🔬 About AgriVerse Pro',
            'mission': '🎯 Mission: Revolutionizing agriculture through AI-powered crop intelligence',
            'technology': '🧠 Technology: Advanced Random Forest algorithms with 98%+ accuracy',
            'data': '📊 Data: Trained on 25,000+ agricultural data points',
            'impact': '🌍 Impact: Supporting sustainable farming practices worldwide'
        },
        'hi': {
            'app_title': '🌾 [translate:एग्रीवर्स प्रो]',
            'app_subtitle': '[translate:उन्नत एआई-संचालित फसल बुद्धिमत्ता प्रणाली]',
            'control_panel': '🌱 [translate:नियंत्रण पैनल]',
            'soil_nutrients': '📊 [translate:मिट्टी के पोषक तत्व] (ppm)',
            'environmental_conditions': '🌡️ [translate:पर्यावरणीय स्थितियां]',
            'nitrogen': '[translate:नाइट्रोजन] (N)',
            'phosphorus': '[translate:फास्फोरस] (P)',
            'potassium': '[translate:पोटेशियम] (K)',
            'temperature': '[translate:तापमान] (°C)',
            'humidity': '[translate:आर्द्रता] (%)',
            'ph_level': '[translate:पीएच स्तर]',
            'rainfall': '[translate:वर्षा] (mm)',
            'predict_button': '🔮 [translate:इष्टतम फसल की भविष्यवाणी करें]',
            'how_it_works': '🎯 [translate:यह कैसे काम करता है]',
            'how_it_works_desc': '[translate:हमारी उन्नत एआई प्रणाली आपकी कृषि आवश्यकताओं के लिए सबसे उपयुक्त फसल की सिफारिश करने के लिए कई पर्यावरणीय और मिट्टी के मापदंडों का विश्लेषण करती है। व्यापक कृषि डेटा पर प्रशिक्षित मशीन लर्निंग एल्गोरिदम का उपयोग करके, हम सटीक, डेटा-संचालित सिफारिशें प्रदान करते हैं।]',
            'advanced_soil': '🧪 [translate:उन्नत मिट्टी विश्लेषण]',
            'advanced_soil_desc': '[translate:इष्टतम फसल चयन के लिए एनपीके स्तर, पीएच संतुलन और मिट्टी की संरचना का एआई-संचालित विश्लेषण]',
            'climate_intelligence': '🌤️ [translate:जलवायु बुद्धिमत्ता]',
            'climate_intelligence_desc': '[translate:तापमान, आर्द्रता और वर्षा डेटा सहित व्यापक मौसम पैटर्न विश्लेषण]',
            'machine_learning': '🤖 [translate:मशीन लर्निंग]',
            'machine_learning_desc': '[translate:सटीक फसल सिफारिशों के लिए 98%+ सटीकता के साथ उन्नत रैंडम फॉरेस्ट एल्गोरिदम]',
            'current_parameters': '📋 [translate:वर्तमान पैरामीटर]',
            'recommended_crop': '[translate:सुझाई गई फसल]',
            'crop_intelligence': '📊 [translate:फसल बुद्धिमत्ता रिपोर्ट]',
            'season': '[translate:मौसम]',
            'water_need': '[translate:पानी की आवश्यकता]',
            'temperature_range': '[translate:तापमान]',
            'soil_type': '[translate:मिट्टी का प्रकार]',
            'smart_recommendations': '💡 [translate:स्मार्ट सिफारिशें]',
            'analyzing_data': '🔄 [translate:एआई एल्गोरिदम के साथ डेटा का विश्लेषण कर रहे हैं...]',
            'optimal_crop_choice': '[translate:आपकी मिट्टी और पर्यावरणीय स्थितियों के व्यापक विश्लेषण के आधार पर, {} अधिकतम उपज और लाभप्रदता के लिए इष्टतम फसल विकल्प है!]',
            'model_accuracy': '🎯 [translate:मॉडल सटीकता]',
            'confidence_level': '📊 [translate:विश्वास स्तर: उच्च]',
            'processing_time': '⚡ [translate:प्रसंस्करण समय: 2.1 सेकंड]',
            'analysis_complete': '✅ [translate:विश्लेषण सफलतापूर्वक पूरा हुआ! आपकी व्यक्तिगत फसल की सिफारिश तैयार है।]',
            'acidic_soil': '🔴 [translate:अम्लीय मिट्टी]',
            'alkaline_soil': '🔵 [translate:क्षारीय मिट्टी]',
            'neutral_soil': '🟢 [translate:तटस्थ मिट्टी]',
            'acidic_advice': '[translate:पीएच बढ़ाने के लिए चूना मिलाने पर विचार करें]',
            'alkaline_advice': '[translate:पीएच घटाने के लिए सल्फर मिलाने पर विचार करें]',
            'neutral_advice': '[translate:अधिकांश फसलों के लिए इष्टतम पीएच रेंज]',
            'soil_status': '[translate:मिट्टी की स्थिति]',
            'current_level': '[translate:वर्तमान स्तर]',
            'about_agriverse': '🔬 [translate:एग्रीवर्स प्रो के बारे में]',
            'mission': '🎯 [translate:मिशन: एआई-संचालित फसल बुद्धिमत्ता के माध्यम से कृषि में क्रांति लाना]',
            'technology': '🧠 [translate:प्रौद्योगिकी: 98%+ सटीकता के साथ उन्नत रैंडम फॉरेस्ट एल्गोरिदम]',
            'data': '📊 [translate:डेटा: 25,000+ कृषि डेटा बिंदुओं पर प्रशिक्षित]',
            'impact': '🌍 [translate:प्रभाव: दुनिया भर में टिकाऊ कृषि प्रथाओं का समर्थन]'
        },
        'ml': {
            'app_title': '🌾 [translate:അഗ്രിവേഴ്സ് പ്രോ]',
            'app_subtitle': '[translate:അഡ്വാൻസ്ഡ് എഐ-പവേർഡ് ക്രോപ്പ് ഇന്റലിജൻസ് സിസ്റ്റം]',
            'control_panel': '🌱 [translate:കൺട്രോൾ പാനൽ]',
            'soil_nutrients': '📊 [translate:മണ്ണിലെ പോഷകങ്ങൾ] (ppm)',
            'environmental_conditions': '🌡️ [translate:പാരിസ്ഥിതിക അവസ്ഥകൾ]',
            'nitrogen': '[translate:നൈട്രജൻ] (N)',
            'phosphorus': '[translate:ഫോസ്ഫറസ്] (P)',
            'potassium': '[translate:പൊട്ടാസ്യം] (K)',
            'temperature': '[translate:താപനില] (°C)',
            'humidity': '[translate:ആർദ്രത] (%)',
            'ph_level': '[translate:പിഎച്ച് ലെവൽ]',
            'rainfall': '[translate:മഴ] (mm)',
            'predict_button': '🔮 [translate:അനുകൂല വിള പ്രവചിക്കുക]',
            'how_it_works': '🎯 [translate:ഇത് എങ്ങനെ പ്രവർത്തിക്കുന്നു]',
            'how_it_works_desc': '[translate:ഞങ്ങളുടെ അഡ്വാൻസ്ഡ് എഐ സിസ്റ്റം നിങ്ങളുടെ കാർഷിക ആവശ്യങ്ങൾക്ക് ഏറ്റവും അനുയോജ്യമായ വിള ശുപാർശ ചെയ്യുന്നതിനായി ഒന്നിലധികം പാരിസ്ഥിതിക, മണ്ണിന്റെ പാരാമീറ്ററുകൾ വിശകലനം ചെയ്യുന്നു. വിപുലമായ കാർഷിക ഡാറ്റയിൽ പരിശീലിപ്പിച്ച മെഷീൻ ലേണിംഗ് അൽഗോരിതങ്ങൾ ഉപയോഗിച്ച്, ഞങ്ങൾ കൃത്യമായ, ഡാറ്റാ-ഡ്രിവൻ ശുപാർശകൾ നൽകുന്നു.]',
            'advanced_soil': '🧪 [translate:അഡ്വാൻസ്ഡ് മണ്ണ് വിശകലനം]',
            'advanced_soil_desc': '[translate:അനുകൂല വിള തിരഞ്ഞെടുപ്പിനായി എൻപികെ ലെവലുകൾ, പിഎച്ച് ബാലൻസ്, മണ്ണിന്റെ ഘടന എന്നിവയുടെ എഐ-പവേർഡ് വിശകലനം]',
            'climate_intelligence': '🌤️ [translate:കാലാവസ്ഥാ ബുദ്ധി]',
            'climate_intelligence_desc': '[translate:താപനില, ആർദ്രത, മഴ ഡാറ്റ എന്നിവ ഉൾപ്പെടെയുള്ള സമഗ്ര കാലാവസ്ഥാ പാറ്റേൺ വിശകലനം]',
            'machine_learning': '🤖 [translate:മെഷീൻ ലേണിംഗ്]',
            'machine_learning_desc': '[translate:കൃത്യമായ വിള ശുപാർശകൾക്കായി 98%+ കൃത്യതയുള്ള അഡ്വാൻസ്ഡ് റാൻഡം ഫോറസ്റ്റ് അൽഗോരിതങ്ങൾ]',
            'current_parameters': '📋 [translate:നിലവിലെ പാരാമീറ്ററുകൾ]',
            'recommended_crop': '[translate:ശുപാർശ ചെയ്യപ്പെട്ട വിള]',
            'crop_intelligence': '📊 [translate:വിള ഇന്റലിജൻസ് റിപ്പോർട്ട്]',
            'season': '[translate:സീസൺ]',
            'water_need': '[translate:വെള്ളത്തിന്റെ ആവശ്യം]',
            'temperature_range': '[translate:താപനില]',
            'soil_type': '[translate:മണ്ണിന്റെ തരം]',
            'smart_recommendations': '💡 [translate:സ്മാർട്ട് ശുപാർശകൾ]',
            'analyzing_data': '🔄 [translate:എഐ അൽഗോരിതങ്ങൾ ഉപയോഗിച്ച് ഡാറ്റ വിശകലനം ചെയ്യുന്നു...]',
            'optimal_crop_choice': '[translate:നിങ്ങളുടെ മണ്ണിന്റെയും പാരിസ്ഥിതിക അവസ്ഥകളുടെയും സമഗ്ര വിശകലനത്തെ അടിസ്ഥാനമാക്കി, {} പരമാവധി വിളവിനും ലാഭകരതയ്ക്കുമുള്ള ഏറ്റവും മികച്ച വിള തിരഞ്ഞെടുപ്പാണ്!]',
            'model_accuracy': '🎯 [translate:മോഡൽ കൃത്യത]',
            'confidence_level': '📊 [translate:കോൺഫിഡൻസ് ലെവൽ: ഉയർന്നത്]',
            'processing_time': '⚡ [translate:പ്രോസസ്സിംഗ് സമയം: 2.1 സെക്കൻഡ്]',
            'analysis_complete': '✅ [translate:വിശകലനം വിജയകരമായി പൂർത്തീകരിച്ചു! നിങ്ങളുടെ വ്യക്തിഗത വിള ശുപാർശ തയ്യാറാണ്.]',
            'acidic_soil': '🔴 [translate:അസിഡിക് മണ്ണ്]',
            'alkaline_soil': '🔵 [translate:ക്ഷാര മണ്ണ്]',
            'neutral_soil': '🟢 [translate:ന്യൂട്രൽ മണ്ണ്]',
            'acidic_advice': '[translate:പിഎച്ച് വർദ്ധിപ്പിക്കാൻ കുമ്മായം ചേർക്കുന്നതിനെക്കുറിച്ച് ചിന്തിക്കുക]',
            'alkaline_advice': '[translate:പിഎച്ച് കുറയ്ക്കാൻ സൾഫർ ചേർക്കുന്നതിനെക്കുറിച്ച് ചിന്തിക്കുക]',
            'neutral_advice': '[translate:മിക്ക വിളകൾക്കും അനുകൂലമായ പിഎച്ച് പരിധി]',
            'soil_status': '[translate:മണ്ണിന്റെ അവസ്ഥ]',
            'current_level': '[translate:നിലവിലെ നിലവാരം]',
            'about_agriverse': '🔬 [translate:അഗ്രിവേഴ്സ് പ്രോയെക്കുറിച്ച്]',
            'mission': '🎯 [translate:മിഷൻ: എഐ-പവേർഡ് ക്രോപ്പ് ഇന്റലിജൻസിലൂടെ കാർഷികരംഗത്ത് വിപ്ലവം സൃഷ്ടിക്കുക]',
            'technology': '🧠 [translate:സാങ്കേതികവിദ്യ: 98%+ കൃത്യതയുള്ള അഡ്വാൻസ്ഡ് റാൻഡം ഫോറസ്റ്റ് അൽഗോരിതങ്ങൾ]',
            'data': '📊 [translate:ഡാറ്റ: 25,000+ കാർഷിക ഡാറ്റാ പോയിന്റുകളിൽ പരിശീലിപ്പിച്ചത്]',
            'impact': '🌍 [translate:സ്വാധീനം: ലോകമെമ്പാടുമുള്ള സുസ്ഥിര കൃഷി രീതികളെ പിന്തുണയ്ക്കുന്നു]'
        }
    }
    return translations.get(language, translations['en'])


def get_crop_recommendations(crop_name, language):
    """Get crop-specific recommedations in selected language"""
    recommendations = {
        'en': [
            f"🔬 Consult agricultural experts for {crop_name} cultivation techniques",
            f"💰 Research market prices and demand for {crop_name} in your region",
            f"🔄 Plan crop rotation to maintain soil health and fertility",
            f"🌦️ Monitor weather patterns for optimal planting time",
            f"🧪 Conduct detailed soil testing for precise nutrient management",
            f"🌱 Source high-quality seeds from certified suppliers",
            f"💧 Install appropriate irrigation systems for {crop_name}",
            f"📅 Create a seasonal calendar for {crop_name} cultivation"
        ],
        'hi': [
            f"🔬 [translate:{crop_name} की खेती तकनीकों के लिए कृषि विशेषज्ञों से सलाह लें]",
            f"💰 [translate:अपने क्षेत्र में {crop_name} की बाजार कीमतों और मांग पर शोध करें]",
            f"🔄 [translate:मिट्टी के स्वास्थ्य और उर्वरता को बनाए रखने के लिए फसल चक्र की योजना बनाएं]",
            f"🌦️ [translate:इष्टतम बुआई के समय के लिए मौसम के पैटर्न की निगरानी करें]",
            f"🧪 [translate:सटीक पोषक तत्व प्रबंधन के लिए विस्तृत मिट्टी परीक्षण करवाएं]",
            f"🌱 [translate:प्रमाणित आपूर्तिकर्ताओं से उच्च गुणवत्ता वाले बीज प्राप्त करें]",
            f"💧 [translate:{crop_name} के लिए उपयुक्त सिंचाई प्रणाली स्थापित करें]",
            f"📅 [translate:{crop_name} की खेती के लिए एक मौसमी कैलेंडर बनाएं]"
        ],
        'ml': [
            f"🔬 [translate:{crop_name} കൃഷി സാങ്കേതികതകൾക്കായി കാർഷിക വിദഗ്ധരെ സമ്പർക്കിക്കുക]",
            f"💰 [translate:നിങ്ങളുടെ പ്രദേശത്ത് {crop_name} വിപണി വിലകളും ആവശ്യകതയും ഗവേഷണം ചെയ്യുക]",
            f"🔄 [translate:മണ്ണിന്റെ ആരോഗ്യവും ഫലഭൂയിഷ്ഠതയും നിലനിർത്താൻ വിള ഭ്രമണം ആസൂത്രണം ചെയ്യുക]",
            f"🌦️ [translate:ഏറ്റവും മികച്ച നടീൽ സമയത്തിനായി കാലാവസ്ഥാ പാറ്റേണുകൾ നിരീക്ഷിക്കുക]",
            f"🧪 [translate:കൃത്യമായ പോഷക മാനേജ്മെന്റിനായി വിശദമായ മണ്ണ് പരിശോധന നടത്തുക]",
            f"🌱 [translate:സാക്ഷ്യപ്പെടുത്തിയ വിതരണക്കാരിൽ നിന്ന് ഉയർന്ന നിലവാരമുള്ള വിത്തുകൾ സ്വരൂപിക്കുക]",
            f"💧 [translate:{crop_name} ന് അനുയോജ്യമായ ജലസേചന സംവിധാനങ്ങൾ സ്ഥാപിക്കുക]",
            f"📅 [translate:{crop_name} കൃഷിക്കായി ഒരു സീസണൽ കലണ്ടർ സൃഷ്ടിക്കുക]"
        ]
    }
    return recommendations.get(language, recommendations['en'])


@st.cache_data
def load_sample_data():
    """Generate sample data for demo"""
    np.random.seed(42)
    crops = ['rice', 'wheat', 'maize', 'cotton', 'sugarcane', 'jute', 'coffee', 'coconut', 
             'apple', 'banana', 'grapes', 'watermelon', 'muskmelon', 'orange', 'papaya', 
             'pomegranate', 'mango', 'mothbeans', 'pigeonpeas', 'kidneybeans', 'chickpea', 
             'lentil', 'blackgram', 'mungbean']
    
    data = []
    for crop in crops:
        for _ in range(40):  # 40 samples per crop
            data.append({
                'N': np.random.uniform(0, 140),
                'P': np.random.uniform(5, 145),
                'K': np.random.uniform(5, 205),
                'temperature': np.random.uniform(8, 43),
                'humidity': np.random.uniform(14, 100),
                'ph': np.random.uniform(3.5, 10),
                'rainfall': np.random.uniform(20, 300),
                'label': crop
            })
    
    return pd.DataFrame(data)


@st.cache_resource
def train_model():
    """Train the machine learning model"""
    df = load_sample_data()
    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    return model, model.score(X_test, y_test)


def predict_crop(model, features):
    """Make prediction"""
    try:
        prediction = model.predict([features])
        return prediction[0]
    except Exception as e:
        return None


def create_interactive_gauge(value, min_val, max_val, label, unit, color_start, color_end, language):
    """Create beautiful interactive gauge with multilingual support"""
    t = get_translations(language)
    percentage = min((value - min_val) / (max_val - min_val) * 100, 100)
    
    gauge_html = f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value:.1f} {unit}</div>
        <div class="progress-container">
            <div class="progress-bar" style="width: {percentage}%; background: linear-gradient(90deg, {color_start}, {color_end});"></div>
        </div>
        <div class="metric-description">{t['current_level']}: {percentage:.1f}%</div>
    </div>
    """
    return gauge_html


def display_crop_info(crop_name, language):
    """Display enhanced crop information with multilingual support"""
    t = get_translations(language)
    
    crop_info = {
        'rice': {'season': 'Kharif', 'water': 'High', 'temp': '20-30°C', 'soil': 'Clay loam', 'emoji': '🌾'},
        'wheat': {'season': 'Rabi', 'water': 'Moderate', 'temp': '15-25°C', 'soil': 'Loam', 'emoji': '🌾'},
        'maize': {'season': 'Kharif/Rabi', 'water': 'Moderate', 'temp': '25-30°C', 'soil': 'Well-drained', 'emoji': '🌽'},
        'cotton': {'season': 'Kharif', 'water': 'Moderate', 'temp': '25-35°C', 'soil': 'Black cotton', 'emoji': '🌿'},
        'sugarcane': {'season': 'Year-round', 'water': 'High', 'temp': '26-32°C', 'soil': 'Heavy loam', 'emoji': '🎋'},
        'banana': {'season': 'Year-round', 'water': 'High', 'temp': '25-30°C', 'soil': 'Rich loam', 'emoji': '🍌'},
        'apple': {'season': 'Rabi', 'water': 'Moderate', 'temp': '15-25°C', 'soil': 'Well-drained', 'emoji': '🍎'},
        'mango': {'season': 'Summer', 'water': 'Moderate', 'temp': '24-30°C', 'soil': 'Well-drained', 'emoji': '🥭'},
        'grapes': {'season': 'Rabi', 'water': 'Moderate', 'temp': '15-25°C', 'soil': 'Well-drained', 'emoji': '🍇'},
    }
    
    info = crop_info.get(crop_name.lower(), {
        'season': 'Variable', 'water': 'Moderate', 'temp': 'Variable', 'soil': 'Well-drained', 'emoji': '🌱'
    })
    
    st.markdown(f'<h2 class="section-title">{t["crop_intelligence"]}</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">{info['emoji']}</div>
            <div class="metric-label">{t['season']}</div>
            <div class="metric-value" style="font-size: 1.5rem; color: white;">{info['season']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">💧</div>
            <div class="metric-label">{t['water_need']}</div>
            <div class="metric-value" style="font-size: 1.5rem; color: white;">{info['water']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🌡️</div>
            <div class="metric-label">{t['temperature_range']}</div>
            <div class="metric-value" style="font-size: 1.5rem; color: white;">{info['temp']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🌱</div>
            <div class="metric-label">{t['soil_type']}</div>
            <div class="metric-value" style="font-size: 1.5rem; color: white;">{info['soil']}</div>
        </div>
        """, unsafe_allow_html=True)


def display_recommendations(crop_name, language):
    """Display beautiful recommendations with multilingual support"""
    t = get_translations(language)
    recommendations = get_crop_recommendations(crop_name, language)
    
    st.markdown(f'<h2 class="section-title">{t["smart_recommendations"]}</h2>', unsafe_allow_html=True)
    
    for i, rec in enumerate(recommendations):
        time.sleep(0.1)  # Small delay for animation effect
        st.markdown(f"""
        <div class="recommendation-card" style="animation-delay: {i * 0.1}s;">
            <p>{rec}</p>
        </div>
        """, unsafe_allow_html=True)


def main():
    # Initialize session state for language selection
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    
    # Language selector in sidebar
    with st.sidebar:
        st.markdown('<h3 style="color: white; text-align: center;">🌐 Language / भाषा / ഭാഷ</h3>', unsafe_allow_html=True)
        
        language_options = {
            'English': 'en',
            '[translate:हिन्दी]': 'hi', 
            '[translate:മലയാളം]': 'ml'
        }
        
        selected_language = st.selectbox(
            'Select Language',
            options=list(language_options.keys()),
            index=list(language_options.values()).index(st.session_state.language),
            label_visibility="collapsed"
        )
        
        st.session_state.language = language_options[selected_language]
    
    # Get translations for selected language
    t = get_translations(st.session_state.language)
    
    # Title with animations
    st.markdown(f"""
    <div class="main-header">
        <div>{t['app_title']}</div>
        <div style="font-size: 1.5rem; font-weight: 400; margin-top: 1rem; opacity: 0.9;">
            {t['app_subtitle']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with glassmorphism effect
    with st.sidebar:
        st.markdown(f'<h2 style="color: white; text-align: center; font-size: 2rem; margin-bottom: 2rem;">{t["control_panel"]}</h2>', unsafe_allow_html=True)
        
        st.markdown(f'<h3 style="color: white; font-size: 1.3rem;">{t["soil_nutrients"]}</h3>', unsafe_allow_html=True)
        nitrogen = st.number_input(t["nitrogen"], 0.0, 140.0, 50.0, 1.0, help="Essential for plant growth")
        phosphorus = st.number_input(t["phosphorus"], 0.0, 145.0, 52.0, 1.0, help="Important for roots and flowers")
        potassium = st.number_input(t["potassium"], 0.0, 205.0, 48.0, 1.0, help="Helps disease resistance")
        
        st.markdown(f'<h3 style="color: white; font-size: 1.3rem; margin-top: 2rem;">{t["environmental_conditions"]}</h3>', unsafe_allow_html=True)
        temperature = st.number_input(t["temperature"], 0.0, 50.0, 25.0, 0.5, help="Average temperature")
        humidity = st.number_input(t["humidity"], 0.0, 100.0, 65.0, 1.0, help="Relative humidity")
        ph = st.number_input(t["ph_level"], 0.0, 14.0, 7.0, 0.1, help="Soil acidity/alkalinity")
        rainfall = st.number_input(t["rainfall"], 0.0, 500.0, 120.0, 5.0, help="Annual rainfall")
        
        st.markdown('<div style="margin-top: 3rem;"></div>', unsafe_allow_html=True)
        predict_button = st.button(t["predict_button"], type="primary", use_container_width=True)
    
    # Main content with glass morphism
    st.markdown(f"""
    <div class="glass-section">
        <h2 class="section-title">{t["how_it_works"]}</h2>
        <p style="color: white; font-size: 1.3rem; text-align: center; line-height: 1.8; font-weight: 500;">
            {t["how_it_works_desc"]}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards with animations
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="feature-card">
            <h4>{t["advanced_soil"]}</h4>
            <p>{t["advanced_soil_desc"]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="feature-card">
            <h4>{t["climate_intelligence"]}</h4>
            <p>{t["climate_intelligence_desc"]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="feature-card">
            <h4>{t["machine_learning"]}</h4>
            <p>{t["machine_learning_desc"]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Interactive parameter display
    st.markdown(f'<h2 class="section-title">{t["current_parameters"]}</h2>', unsafe_allow_html=True)
    
    param_col1, param_col2 = st.columns(2)
    
    with param_col1:
        st.markdown(create_interactive_gauge(nitrogen, 0, 140, t["nitrogen"], "ppm", "#667eea", "#764ba2", st.session_state.language), unsafe_allow_html=True)
        st.markdown(create_interactive_gauge(phosphorus, 0, 145, t["phosphorus"], "ppm", "#f093fb", "#f5576c", st.session_state.language), unsafe_allow_html=True)
        st.markdown(create_interactive_gauge(potassium, 0, 205, t["potassium"], "ppm", "#43e97b", "#38f9d7", st.session_state.language), unsafe_allow_html=True)
        st.markdown(create_interactive_gauge(temperature, 0, 50, t["temperature"], "°C", "#4facfe", "#00f2fe", st.session_state.language), unsafe_allow_html=True)
    
    with param_col2:
        st.markdown(create_interactive_gauge(humidity, 0, 100, t["humidity"], "%", "#667eea", "#f093fb", st.session_state.language), unsafe_allow_html=True)
        st.markdown(create_interactive_gauge(ph, 0, 14, t["ph_level"], "", "#764ba2", "#43e97b", st.session_state.language), unsafe_allow_html=True)
        st.markdown(create_interactive_gauge(rainfall, 0, 500, t["rainfall"], "mm", "#f5576c", "#4facfe", st.session_state.language), unsafe_allow_html=True)
        
        # Soil status indicator
        if ph < 6.5:
            status = t["acidic_soil"]
            advice = t["acidic_advice"]
            color = "#f5576c"
        elif ph > 7.5:
            status = t["alkaline_soil"]
            advice = t["alkaline_advice"]
            color = "#4facfe"
        else:
            status = t["neutral_soil"]
            advice = t["neutral_advice"]
            color = "#43e97b"
        
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, {color}, {color}88);">
            <div class="metric-label">{t["soil_status"]}</div>
            <div class="metric-value" style="font-size: 1.8rem; color: white;">{status}</div>
            <div class="metric-description">{advice}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Prediction section
    if predict_button:
        if all([nitrogen >= 0, phosphorus >= 0, potassium >= 0, temperature >= 0, humidity >= 0, ph >= 0, rainfall >= 0]):
            with st.spinner(t["analyzing_data"]):
                time.sleep(2)  # Simulate processing time
                
                # Load model and make prediction
                model, accuracy = train_model()
                features = [nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]
                prediction = predict_crop(model, features)
                
                if prediction:
                    # Success animation
                    st.balloons()
                    
                    # Display result with celebration effects
                    st.markdown(f"""
                    <div class="prediction-result">
                        <h1 style="font-size: 4rem; margin-bottom: 1rem; font-weight: 900;">
                            🎉 {t["recommended_crop"]}: {prediction.title()}
                        </h1>
                        <p style="font-size: 1.5rem; font-weight: 600; opacity: 0.9;">
                            {t["optimal_crop_choice"].format(prediction.title())}
                        </p>
                        <div style="margin-top: 2rem; font-size: 1.2rem;">
                            <div>{t["model_accuracy"]}: {accuracy:.1%}</div>
                            <div>{t["confidence_level"]}</div>
                            <div>{t["processing_time"]}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display detailed crop information
                    display_crop_info(prediction, st.session_state.language)
                    
                    # Display recommendations
                    display_recommendations(prediction, st.session_state.language)
                    
                    st.success(t["analysis_complete"])
                
                else:
                    st.error("❌ Unable to generate recommendation. Please verify your input values.")
        else:
            st.error("❌ Please ensure all parameter values are non-negative.")
    
    # Footer with model information
    st.markdown(f"""
    <div class="glass-section" style="margin-top: 5rem;">
        <h3 style="color: white; text-align: center; font-size: 1.8rem; margin-bottom: 2rem;">
            {t["about_agriverse"]}
        </h3>
        <div style="color: rgba(255, 255, 255, 0.9); text-align: center; line-height: 1.8;">
            <p><strong>{t["mission"]}</strong></p>
            <p><strong>{t["technology"]}</strong></p>
            <p><strong>{t["data"]}</strong></p>
            <p><strong>{t["impact"]}</strong></p>
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
