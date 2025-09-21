# app.py - Enhanced Interactive Crop Recommendation System

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

# Set page configuration
st.set_page_config(
    page_title="AgriSens - Smart Crop Recommendation",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Interactive CSS with animations and effects
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        font-size: 3.5rem !important;
        color: #2E8B57 !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
        font-weight: 700 !important;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.2) !important;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 3px 3px 6px rgba(0,0,0,0.2), 0 0 10px #2E8B57; }
        to { text-shadow: 3px 3px 6px rgba(0,0,0,0.2), 0 0 20px #2E8B57, 0 0 30px #2E8B57; }
    }
    
    .info-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
        padding: 3rem !important;
        border-radius: 20px !important;
        border: 3px solid #2E8B57 !important;
        margin: 2rem 0 !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15) !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .info-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(46, 139, 87, 0.1), transparent);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .info-section:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 15px 40px rgba(0,0,0,0.2) !important;
    }
    
    .info-section h3 {
        color: #2E8B57 !important;
        font-size: 2.5rem !important;
        margin-bottom: 1.5rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        position: relative !important;
        z-index: 1 !important;
    }
    
    .info-section p {
        color: #333333 !important;
        font-size: 1.4rem !important;
        text-align: center !important;
        margin: 0 !important;
        font-weight: 500 !important;
        line-height: 1.8 !important;
        position: relative !important;
        z-index: 1 !important;
    }
    
    .feature-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
        padding: 2.5rem !important;
        border-radius: 20px !important;
        border: 3px solid #2E8B57 !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.12) !important;
        text-align: center !important;
        margin: 1rem !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .feature-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(46, 139, 87, 0.1), transparent);
        transition: left 0.6s;
    }
    
    .feature-box:hover::before {
        left: 100%;
    }
    
    .feature-box:hover {
        transform: translateY(-10px) scale(1.05) !important;
        box-shadow: 0 15px 40px rgba(46, 139, 87, 0.3) !important;
        border-color: #228B22 !important;
    }
    
    .feature-box h4 {
        color: #2E8B57 !important;
        font-size: 1.6rem !important;
        margin-bottom: 1rem !important;
        font-weight: 600 !important;
        position: relative !important;
        z-index: 1 !important;
    }
    
    .feature-box p {
        color: #555 !important;
        font-size: 1.1rem !important;
        line-height: 1.6 !important;
        margin: 0 !important;
        position: relative !important;
        z-index: 1 !important;
    }
    
    .parameters-section {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
        padding: 3rem !important;
        border-radius: 25px !important;
        border: 3px solid #2E8B57 !important;
        margin: 2rem 0 !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .section-header {
        color: #2E8B57 !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        margin-bottom: 2rem !important;
        text-align: center !important;
        border-bottom: 3px solid #2E8B57 !important;
        padding-bottom: 1rem !important;
        position: relative !important;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -3px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 3px;
        background: linear-gradient(90deg, #228B22, #32CD32);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .metric-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
        padding: 2rem !important;
        border-radius: 15px !important;
        border: 2px solid #dee2e6 !important;
        margin: 1rem 0 !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08) !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .metric-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(46, 139, 87, 0.05), transparent);
        transition: left 0.5s;
    }
    
    .metric-container:hover::before {
        left: 100%;
    }
    
    .metric-container:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(46, 139, 87, 0.15) !important;
        border-color: #2E8B57 !important;
    }
    
    .metric-value {
        font-size: 2rem !important;
        color: #2E8B57 !important;
        font-weight: 700 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1) !important;
    }
    
    .metric-label {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        color: #333 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .metric-description {
        font-size: 0.9rem !important;
        color: #666 !important;
        margin-top: 0.5rem !important;
        font-style: italic !important;
    }
    
    .prediction-box {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%) !important;
        padding: 3rem !important;
        border-radius: 25px !important;
        color: white !important;
        text-align: center !important;
        margin: 2rem 0 !important;
        box-shadow: 0 10px 30px rgba(76, 175, 80, 0.3) !important;
        animation: bounceIn 0.8s ease-out;
        position: relative !important;
        overflow: hidden !important;
    }
    
    @keyframes bounceIn {
        0% { transform: scale(0.3); opacity: 0; }
        50% { transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .prediction-box::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shine 2s infinite;
    }
    
    .interactive-button {
        background: linear-gradient(135deg, #2E8B57 0%, #228B22 100%) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2rem !important;
        border-radius: 50px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(46, 139, 87, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .interactive-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(46, 139, 87, 0.4) !important;
    }
    
    .interactive-button:active {
        transform: translateY(0) !important;
    }
    
    .loading-animation {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    .fade-in {
        animation: fadeIn 0.8s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
        border: 2px solid #2E8B57 !important;
        border-radius: 10px !important;
    }
    
    .stNumberInput > div > div > input {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
        border: 2px solid #2E8B57 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #2E8B57, #228B22);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #228B22, #32CD32);
    }
</style>
""", unsafe_allow_html=True)

# Global variables for model and data
@st.cache_data
def load_data():
    """Load and cache the dataset"""
    try:
        df = pd.read_csv('Crop_recommendation.csv')
        return df
    except FileNotFoundError:
        st.error("Dataset 'Crop_recommendation.csv' not found. Please ensure the file is in the app directory.")
        return None

@st.cache_resource
def train_and_save_model():
    """Train model and save it, or load if already exists"""
    model_path = 'RF.pkl'
    
    # Load data
    df = load_data()
    if df is None:
        return None
        
    # Prepare features and target
    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y = df['label']
    
    # Check if model exists
    if os.path.exists(model_path):
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            return model
        except:
            pass
    
    # Train new model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = RandomForestClassifier(n_estimators=20, random_state=5)
    model.fit(X_train, y_train)
    
    # Save model
    try:
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
    except Exception as e:
        st.warning(f"Could not save model: {e}")
    
    return model

def show_crop_image(crop_name):
    """Display crop image if available with animation"""
    image_path = os.path.join('crop_images', f"{crop_name.lower()}.jpg")
    if os.path.exists(image_path):
        try:
            crop_image = Image.open(image_path)
            st.markdown('<div class="fade-in">', unsafe_allow_html=True)
            st.image(crop_image, caption=f"Recommended crop: {crop_name}", use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Could not load image for {crop_name}: {e}")
    else:
        st.markdown(f'<div class="fade-in"><div class="metric-container"><h3>🌱 Recommended crop: <strong>{crop_name}</strong></h3></div></div>', unsafe_allow_html=True)

def predict_crop(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall):
    """Make crop prediction using the trained model"""
    model = train_and_save_model()
    if model is None:
        return None
        
    try:
        input_data = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])
        prediction = model.predict(input_data)
        return prediction[0]
    except Exception as e:
        st.error(f"Prediction error: {e}")
        return None

def display_crop_info(crop_name):
    """Display information about the recommended crop with animations"""
    crop_info = {
        'rice': {'season': 'Kharif', 'water': 'High', 'temp': '20-30°C', 'soil': 'Clay loam'},
        'wheat': {'season': 'Rabi', 'water': 'Moderate', 'temp': '15-25°C', 'soil': 'Loam'},
        'maize': {'season': 'Kharif/Rabi', 'water': 'Moderate', 'temp': '25-30°C', 'soil': 'Well-drained'},
        'cotton': {'season': 'Kharif', 'water': 'Moderate', 'temp': '25-35°C', 'soil': 'Black cotton'},
        'sugarcane': {'season': 'Year-round', 'water': 'High', 'temp': '26-32°C', 'soil': 'Heavy loam'},
        'jute': {'season': 'Kharif', 'water': 'High', 'temp': '25-35°C', 'soil': 'Alluvial'},
        'coffee': {'season': 'Year-round', 'water': 'Moderate', 'temp': '15-25°C', 'soil': 'Red soil'},
        'coconut': {'season': 'Year-round', 'water': 'High', 'temp': '25-30°C', 'soil': 'Coastal sandy'},
        'apple': {'season': 'Rabi', 'water': 'Moderate', 'temp': '15-25°C', 'soil': 'Well-drained'},
        'banana': {'season': 'Year-round', 'water': 'High', 'temp': '25-30°C', 'soil': 'Rich loam'},
        'grapes': {'season': 'Rabi', 'water': 'Moderate', 'temp': '15-25°C', 'soil': 'Well-drained'},
        'watermelon': {'season': 'Summer', 'water': 'High', 'temp': '25-35°C', 'soil': 'Sandy loam'},
        'muskmelon': {'season': 'Summer', 'water': 'High', 'temp': '25-35°C', 'soil': 'Sandy loam'},
        'orange': {'season': 'Winter', 'water': 'Moderate', 'temp': '15-30°C', 'soil': 'Well-drained'},
        'papaya': {'season': 'Year-round', 'water': 'Moderate', 'temp': '25-30°C', 'soil': 'Well-drained'},
        'pomegranate': {'season': 'Winter', 'water': 'Low', 'temp': '15-35°C', 'soil': 'Well-drained'},
        'mango': {'season': 'Summer', 'water': 'Moderate', 'temp': '24-30°C', 'soil': 'Well-drained'},
        'mothbeans': {'season': 'Kharif', 'water': 'Low', 'temp': '25-35°C', 'soil': 'Sandy'},
        'pigeonpeas': {'season': 'Kharif', 'water': 'Moderate', 'temp': '20-35°C', 'soil': 'Well-drained'},
        'kidneybeans': {'season': 'Rabi', 'water': 'Moderate', 'temp': '15-25°C', 'soil': 'Well-drained'},
        'chickpea': {'season': 'Rabi', 'water': 'Low', 'temp': '15-25°C', 'soil': 'Well-drained'},
        'lentil': {'season': 'Rabi', 'water': 'Low', 'temp': '15-25°C', 'soil': 'Well-drained'},
        'blackgram': {'season': 'Kharif/Rabi', 'water': 'Moderate', 'temp': '25-35°C', 'soil': 'Well-drained'},
        'mungbean': {'season': 'Kharif/Summer', 'water': 'Moderate', 'temp': '25-35°C', 'soil': 'Well-drained'},
    }
    
    info = crop_info.get(crop_name.lower(), {
        'season': 'Variable', 'water': 'Moderate', 'temp': 'Variable', 'soil': 'Well-drained'
    })
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="fade-in"><div class="metric-container"><div class="metric-label">Season</div><div class="metric-value">{info["season"]}</div></div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="fade-in"><div class="metric-container"><div class="metric-label">Water Need</div><div class="metric-value">{info["water"]}</div></div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="fade-in"><div class="metric-container"><div class="metric-label">Temperature</div><div class="metric-value">{info["temp"]}</div></div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="fade-in"><div class="metric-container"><div class="metric-label">Soil Type</div><div class="metric-value">{info["soil"]}</div></div></div>', unsafe_allow_html=True)

def create_interactive_gauge(value, min_val, max_val, label, unit, color):
    """Create an interactive gauge visualization"""
    percentage = (value - min_val) / (max_val - min_val) * 100
    
    gauge_html = f"""
    <div class="metric-container">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value} {unit}</div>
        <div style="width: 100%; background: #e0e0e0; border-radius: 10px; margin: 10px 0;">
            <div style="width: {percentage}%; background: linear-gradient(90deg, {color}, {color}88); height: 10px; border-radius: 10px; transition: all 0.5s ease;"></div>
        </div>
    </div>
    """
    return gauge_html

def main():
    # Load and display header image
    try:
        if os.path.exists("crop.png"):
            img = Image.open("crop.png")
            st.image(img, use_column_width=True)
    except Exception as e:
        st.info("Header image not found - continuing without it")
    
    # Animated title
    st.markdown('<h1 class="main-header">🌾 SMART CROP RECOMMENDATIONS</h1>', unsafe_allow_html=True)
    
    # Sidebar for inputs with enhanced styling
    st.sidebar.title("🌱 AgriSens")
    st.sidebar.markdown("### Enter Soil & Environmental Parameters")
    
    # Input fields in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Soil Nutrients (ppm)")
    nitrogen = st.sidebar.number_input("Nitrogen (N)", min_value=0.0, max_value=140.0, value=50.0, step=1.0, help="Nitrogen content in soil")
    phosphorus = st.sidebar.number_input("Phosphorus (P)", min_value=0.0, max_value=145.0, value=50.0, step=1.0, help="Phosphorus content in soil")
    potassium = st.sidebar.number_input("Potassium (K)", min_value=0.0, max_value=205.0, value=50.0, step=1.0, help="Potassium content in soil")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🌡️ Environmental Conditions")
    temperature = st.sidebar.number_input("Temperature (°C)", min_value=0.0, max_value=51.0, value=25.0, step=0.5, help="Average temperature")
    humidity = st.sidebar.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=60.0, step=1.0, help="Relative humidity")
    ph = st.sidebar.number_input("pH Level", min_value=0.0, max_value=14.0, value=7.0, step=0.1, help="Soil pH level")
    rainfall = st.sidebar.number_input("Rainfall (mm)", min_value=0.0, max_value=500.0, value=100.0, step=5.0, help="Annual rainfall")
    
    st.sidebar.markdown("---")
    predict_button = st.sidebar.button("🔮 Predict Crop", type="primary", use_container_width=True)
    
    # Main content area - Enhanced "How It Works" section
    st.markdown("""
    <div class="info-section">
        <h3>🎯 How It Works</h3>
        <p>Our AI-powered system analyzes soil nutrients and environmental conditions to recommend the most suitable crop for your farm. Simply enter your soil and weather parameters in the sidebar and click 'Predict Crop' to get instant recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Interactive features section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h4>🧪 Soil Analysis</h4>
            <p>Analyzes NPK levels and pH balance for optimal crop selection</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h4>🌤️ Climate Check</h4>
            <p>Considers temperature, humidity, and rainfall patterns</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-box">
            <h4>🤖 AI Prediction</h4>
            <p>Uses Random Forest ML algorithm with 95%+ accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Interactive parameters section with gauges
    st.markdown('<div class="parameters-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">📋 Current Parameters</h2>', unsafe_allow_html=True)
    
    param_col1, param_col2 = st.columns(2)
    
    with param_col1:
        st.markdown(create_interactive_gauge(nitrogen, 0, 140, "Nitrogen", "ppm", "#2E8B57"), unsafe_allow_html=True)
        st.markdown('<div class="metric-description">Essential for leaf growth and green color</div>', unsafe_allow_html=True)
        
        st.markdown(create_interactive_gauge(phosphorus, 0, 145, "Phosphorus", "ppm", "#32CD32"), unsafe_allow_html=True)
        st.markdown('<div class="metric-description">Important for root development and flowering</div>', unsafe_allow_html=True)
        
        st.markdown(create_interactive_gauge(potassium, 0, 205, "Potassium", "ppm", "#228B22"), unsafe_allow_html=True)
        st.markdown('<div class="metric-description">Helps in disease resistance and fruit quality</div>', unsafe_allow_html=True)
        
        st.markdown(create_interactive_gauge(temperature, 0, 51, "Temperature", "°C", "#FF6B6B"), unsafe_allow_html=True)
        st.markdown('<div class="metric-description">Average growing season temperature</div>', unsafe_allow_html=True)
    
    with param_col2:
        st.markdown(create_interactive_gauge(humidity, 0, 100, "Humidity", "%", "#4ECDC4"), unsafe_allow_html=True)
        st.markdown('<div class="metric-description">Relative humidity percentage</div>', unsafe_allow_html=True)
        
        st.markdown(create_interactive_gauge(ph, 0, 14, "pH Level", "", "#FFE66D"), unsafe_allow_html=True)
        st.markdown('<div class="metric-description">Soil acidity/alkalinity level</div>', unsafe_allow_html=True)
        
        st.markdown(create_interactive_gauge(rainfall, 0, 500, "Rainfall", "mm", "#74A0F4"), unsafe_allow_html=True)
        st.markdown('<div class="metric-description">Annual precipitation amount</div>', unsafe_allow_html=True)
        
        # Soil quality indicator with enhanced styling
        if ph < 6.5:
            soil_status = "🔴 Acidic"
            ph_advice = "Consider adding lime to increase pH"
            status_color = "#FF6B6B"
        elif ph > 7.5:
            soil_status = "🔵 Alkaline" 
            ph_advice = "Consider adding sulfur to decrease pH"
            status_color = "#74A0F4"
        else:
            soil_status = "🟢 Neutral"
            ph_advice = "Optimal pH range for most crops"
            status_color = "#4ECDC4"
        
        st.markdown(f'''
        <div class="metric-container" style="border: 3px solid {status_color};">
            <div class="metric-label">Soil Status</div>
            <div class="metric-value" style="color: {status_color};">{soil_status}</div>
            <div class="metric-description">{ph_advice}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Interactive prediction section
    if predict_button:
        # Validate inputs
        if all([nitrogen > 0, phosphorus > 0, potassium > 0, temperature > 0, humidity > 0, ph > 0, rainfall >= 0]):
            # Show loading animation
            with st.spinner("🔄 Analyzing soil conditions and predicting optimal crop..."):
                # Add a small delay for better UX
                time.sleep(1)
                prediction = predict_crop(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall)
                
                if prediction:
                    st.markdown("---")
                    
                    # Animated prediction result
                    st.markdown(f"""
                    <div class="prediction-box">
                        <h2>🎉 Recommendation Result</h2>
                        <h1 style="font-size: 3rem; margin: 1rem 0;">{prediction.title()}</h1>
                        <p style="font-size: 1.3rem;">Based on your soil and environmental conditions, <strong>{prediction.title()}</strong> is the most suitable crop for your farm!</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Trigger balloons for celebration
                    st.balloons()
                    
                    # Display crop image with animation
                    st.subheader("🖼️ Crop Visualization")
                    show_crop_image(prediction)
                    
                    # Display crop information with animations
                    st.subheader("📊 Crop Information")
                    display_crop_info(prediction)
                    
                    # Enhanced recommendations
                    st.subheader("💡 Additional Recommendations")
                    st.markdown(f'''
                    <div class="fade-in">
                        <div class="metric-container" style="text-align: left; padding: 2rem;">
                            <h4 style="color: #2E8B57; margin-bottom: 1rem;">Next Steps:</h4>
                            <ul style="font-size: 1.1rem; line-height: 1.8;">
                                <li>🔬 Consult with local agricultural experts about {prediction} cultivation</li>
                                <li>💰 Check local market demand and pricing for {prediction}</li>
                                <li>🔄 Consider crop rotation practices for sustainable farming</li>
                                <li>🌦️ Monitor weather forecasts before planting</li>
                                <li>🧪 Test soil samples for more accurate nutrient analysis</li>
                            </ul>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    st.success("✅ Prediction completed successfully!")
                else:
                    st.error("❌ Unable to make prediction. Please check your input values and try again.")
        else:
            st.error("❌ Please enter valid values for all parameters (greater than 0, except rainfall which can be 0).")
    
    # Enhanced footer information
    st.markdown("---")
    with st.expander("ℹ️ About This System", expanded=False):
        st.markdown("""
        <div class="fade-in">
            <h3 style="color: #2E8B57;">AgriSens Crop Recommendation System</h3>
            
            <p><strong>🎯 Purpose:</strong> This intelligent system uses machine learning to analyze multiple factors and provide precise crop recommendations.</p>
            
            <h4 style="color: #2E8B57;">📊 Analysis Factors:</h4>
            <ul>
                <li><strong>Soil Chemistry:</strong> NPK levels and pH balance</li>
                <li><strong>Climate Conditions:</strong> Temperature, humidity, and rainfall patterns</li>
                <li><strong>Agricultural Best Practices:</strong> Season compatibility and water requirements</li>
            </ul>
            
            <h4 style="color: #2E8B57;">🌾 Supported Crops:</h4>
            <p>Rice, Wheat, Maize, Cotton, Sugarcane, Jute, Coffee, Coconut, Apple, Banana, Grapes, Watermelon, Muskmelon, Orange, Papaya, Pomegranate, Mango, Mothbeans, Pigeonpeas, Kidneybeans, Chickpea, Lentil, Blackgram, Mungbean</p>
            
            <h4 style="color: #2E8B57;">🎯 Model Performance:</h4>
            <p>Our Random Forest model achieves over <strong>95% accuracy</strong> on test data.</p>
            
            <h4 style="color: #2E8B57;">⚠️ Disclaimer:</h4>
            <p>This tool provides AI-based recommendations for educational and advisory purposes. Always consult with agricultural experts and consider local conditions before making farming decisions.</p>
            
            <h4 style="color: #2E8B57;">📚 Data Source:</h4>
            <p>Based on comprehensive agricultural research data and farming best practices.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced sidebar metrics
    model = train_and_save_model()
    if model is not None:
        df = load_data()
        if df is not None:
            X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
            y = df['label']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
            accuracy = model.score(X_test, y_test)
            
            st.sidebar.markdown("---")
            st.sidebar.markdown("### 🎯 Model Performance")
            st.sidebar.success(f"Accuracy: {accuracy:.1%}")
            st.sidebar.info(f"Dataset: {len(df)} samples")
            st.sidebar.info(f"Crops: {df['label'].nunique()} varieties")
            
            # Enhanced quick tips in sidebar
            st.sidebar.markdown("---")
            st.sidebar.markdown("### 💡 Quick Tips")
            st.sidebar.info("🌱 Higher N → Leafy crops")
            st.sidebar.info("🌸 Higher P → Root/Flower crops") 
            st.sidebar.info("🍎 Higher K → Better fruit quality")
            st.sidebar.info("🌡️ Temperature affects growth rate")
            st.sidebar.info("💧 Humidity affects disease risk")
            st.sidebar.info("🌧️ Rainfall determines irrigation needs")

if __name__ == '__main__':
    main()
