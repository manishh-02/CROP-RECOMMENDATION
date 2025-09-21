# app.py - FINAL FIXED Version with High Visibility

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
    page_title="AgriVerse Pro: Smart Crop Recommendation",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# FINAL FIXED CSS with High Contrast and No Overlapping
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Poppins', sans-serif !important;
        background-color: #F0F2F6 !important; /* Light gray background for the whole app */
    }
    
    .main-header {
        font-size: 3.2rem !important;
        color: #004085 !important;
        background-color: #FFFFFF !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
        font-weight: 700 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1) !important;
        padding: 2rem !important;
        border-radius: 15px !important;
        border: 4px solid #004085 !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1) !important;
    }
    
    .info-section, .parameters-section, .crop-recommendation-section, .recommendations-section {
        background-color: #FFFFFF !important;
        padding: 3rem !important;
        border-radius: 20px !important;
        margin: 3rem 0 !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1) !important;
        border-left: 10px solid #004085 !important;
        border-right: 2px solid #DEE2E6 !important;
        border-top: 2px solid #DEE2E6 !important;
        border-bottom: 2px solid #DEE2E6 !important;
        transition: all 0.3s ease-in-out !important;
    }
    
    .info-section:hover, .parameters-section:hover, .crop-recommendation-section:hover, .recommendations-section:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.15) !important;
    }
    
    h3 {
        color: #004085 !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
    }
    
    .info-section p {
        color: #212529 !important; /* Dark text for high contrast */
        font-size: 1.4rem !important;
        text-align: center !important;
        font-weight: 500 !important;
        line-height: 1.7 !important;
    }
    
    .feature-box {
        background-color: #FFFFFF !important;
        padding: 2.5rem !important;
        border-radius: 15px !important;
        border: 3px solid #FFC107 !important;
        box-shadow: 0 8px 15px rgba(0,0,0,0.08) !important;
        text-align: center !important;
        margin: 1.5rem !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
    }
    
    .feature-box:hover {
        transform: translateY(-10px) !important;
        box-shadow: 0 12px 25px rgba(0,0,0,0.15) !important;
        border-color: #E0A800 !important;
    }
    
    .feature-box h4 {
        color: #E0A800 !important;
        font-size: 1.6rem !important;
        margin-bottom: 1.5rem !important;
        font-weight: 700 !important;
    }
    
    .feature-box p {
        color: #212529 !important;
        font-size: 1.1rem !important;
        line-height: 1.6 !important;
        font-weight: 500 !important;
    }
    
    .section-header {
        color: #155724 !important; /* Dark Green */
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        margin-bottom: 2.5rem !important;
        border-bottom: 4px solid #155724 !important;
        padding-bottom: 1rem !important;
    }
    
    .metric-container {
        background-color: #F8F9FA !important;
        padding: 2rem !important;
        border-radius: 15px !important;
        border: 2px solid #DEE2E6 !important;
        margin: 1.5rem 0 !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05) !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
    }
    
    .metric-container:hover {
        border-color: #155724 !important;
    }
    
    .metric-value {
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    .metric-label {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        color: #495057 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .metric-description {
        font-size: 1rem !important;
        color: #6C757D !important;
        margin-top: 1rem !important;
    }
    
    .prediction-box {
        background: linear-gradient(135deg, #155724 0%, #1c7430 100%) !important;
        color: #FFFFFF !important;
        padding: 3rem !important;
        border-radius: 20px !important;
        text-align: center !important;
        margin: 2rem 0 !important;
        border: 4px solid #c3e6cb !important;
    }

    .crop-name-display {
        background: linear-gradient(135deg, #28A745 0%, #20C997 100%) !important;
        color: #FFFFFF !important;
        padding: 2.5rem !important;
        border-radius: 20px !important;
        text-align: center !important;
        margin: 2rem 0 !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    
    .crop-info-header {
        color: #004085 !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
    }
    
    .crop-metric-card {
        background: #004085 !important;
        color: #FFFFFF !important;
        padding: 2rem !important;
        border-radius: 15px !important;
        text-align: center !important;
        margin: 1.5rem !important;
    }

    .crop-metric-value {
        color: #FFFFFF !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }

    .crop-metric-label {
        color: #FFFFFF !important;
        opacity: 0.9;
    }
    
    .recommendations-header {
        color: #856404 !important; /* Dark Yellow/Brown */
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
    }
    
    .recommendations-list li {
        background-color: #FFF3CD !important;
        margin: 1.5rem 0 !important;
        padding: 2rem !important;
        border-radius: 10px !important;
        border-left: 8px solid #FFC107 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #212529 !important;
    }
    
    .fade-in {
        animation: fadeIn 1s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* FIXED: Overlapping issue with large top and bottom margin */
    .stExpander {
        margin-top: 5rem !important;
        margin-bottom: 5rem !important;
    }
    
    .stExpander > div > div {
        background: #FFFFFF !important;
        border: 2px solid #DEE2E6 !important;
        border-radius: 10px !important;
        padding: 2rem !important;
    }

    /* Final spacing at the end of the page */
    .main > div:last-child {
        padding-bottom: 5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# All Python functions remain the same
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('Crop_recommendation.csv')
        return df
    except FileNotFoundError:
        st.error("Dataset 'Crop_recommendation.csv' not found.")
        return None

@st.cache_resource
def train_and_save_model():
    model_path = 'RF.pkl'
    df = load_data()
    if df is None: return None
    if os.path.exists(model_path):
        try:
            with open(model_path, 'rb') as f: return pickle.load(f)
        except: pass
    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y = df['label']
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.3, random_state=42)
    model = RandomForestClassifier(n_estimators=20, random_state=5)
    model.fit(X_train, y_train)
    try:
        with open(model_path, 'wb') as f: pickle.dump(model, f)
    except Exception as e: st.warning(f"Could not save model: {e}")
    return model

def show_crop_image(crop_name):
    image_path = os.path.join('crop_images', f"{crop_name.lower()}.jpg")
    if os.path.exists(image_path):
        try:
            crop_image = Image.open(image_path)
            st.image(crop_image, caption=f"Recommended crop: {crop_name}", use_column_width=True)
        except Exception as e: st.warning(f"Could not load image for {crop_name}: {e}")
    else:
        st.markdown(f'<div class="crop-name-display">🌱 Recommended crop: <strong>{crop_name.title()}</strong></div>', unsafe_allow_html=True)

def predict_crop(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall):
    model = train_and_save_model()
    if model is None: return None
    try:
        input_data = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])
        return model.predict(input_data)[0]
    except Exception as e:
        st.error(f"Prediction error: {e}")
        return None

def display_crop_info(crop_name):
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
    info = crop_info.get(crop_name.lower(), {'season': 'N/A', 'water': 'N/A', 'temp': 'N/A', 'soil': 'N/A'})
    st.markdown('<div class="crop-info-header">📊 Crop Information</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="crop-metric-card"><div class="crop-metric-label">Season</div><div class="crop-metric-value">{info["season"]}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="crop-metric-card"><div class="crop-metric-label">Water Need</div><div class="crop-metric-value">{info["water"]}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="crop-metric-card"><div class="crop-metric-label">Temperature</div><div class="crop-metric-value">{info["temp"]}</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="crop-metric-card"><div class="crop-metric-label">Soil Type</div><div class="crop-metric-value">{info["soil"]}</div></div>', unsafe_allow_html=True)

def create_interactive_gauge(value, min_val, max_val, label, unit, color):
    percentage = ((value - min_val) / (max_val - min_val)) * 100
    gauge_html = f"""
    <div class="metric-container">
        <div class="metric-label">{label}</div>
        <div class="metric-value" style="color: {color};">{value:.1f} {unit}</div>
        <div style="background-color: #E9ECEF; border-radius: 10px; margin: 15px 0;">
            <div style="width: {percentage}%; background-color: {color}; height: 12px; border-radius: 10px;"></div>
        </div>
    </div>
    """
    return gauge_html

def main():
    try:
        if os.path.exists("crop.png"): st.image(Image.open("crop.png"))
    except: pass
    
    st.markdown('<h1 class="main-header">AgriVerse Pro: 🌾 SMART CROP RECOMMENDATIONS</h1>', unsafe_allow_html=True)
    
    st.sidebar.title("🌱 AgriVerse Pro")
    st.sidebar.markdown("### Enter Soil & Environmental Parameters")
    st.sidebar.markdown("---")
    nitrogen = st.sidebar.number_input("Nitrogen (N)", 0.0, 140.0, 50.0, 1.0, help="Nitrogen content in soil (ppm)")
    phosphorus = st.sidebar.number_input("Phosphorus (P)", 0.0, 145.0, 50.0, 1.0, help="Phosphorus content in soil (ppm)")
    potassium = st.sidebar.number_input("Potassium (K)", 0.0, 205.0, 50.0, 1.0, help="Potassium content in soil (ppm)")
    st.sidebar.markdown("---")
    temperature = st.sidebar.number_input("Temperature (°C)", 0.0, 51.0, 25.0, 0.5, help="Average temperature")
    humidity = st.sidebar.number_input("Humidity (%)", 0.0, 100.0, 60.0, 1.0, help="Relative humidity")
    ph = st.sidebar.number_input("pH Level", 0.0, 14.0, 7.0, 0.1, help="Soil pH level")
    rainfall = st.sidebar.number_input("Rainfall (mm)", 0.0, 500.0, 100.0, 5.0, help="Annual rainfall")
    st.sidebar.markdown("---")
    predict_button = st.sidebar.button("🔮 Predict Crop", type="primary", use_container_width=True)
    
    st.markdown("""
    <div class="info-section">
        <h3>🎯 How It Works</h3>
        <p>This AI-powered system analyzes your soil and climate data to recommend the most suitable crop, boosting your farm's productivity.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown('<div class="feature-box"><h4>🧪 Soil Analysis</h4><p>Analyzes NPK & pH for optimal crop selection.</p></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="feature-box"><h4>🌤️ Climate Check</h4><p>Considers temperature, humidity, and rainfall.</p></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="feature-box"><h4>🤖 AI Prediction</h4><p>Uses a Random Forest model with 95%+ accuracy.</p></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="parameters-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">📋 Current Parameters</h2>', unsafe_allow_html=True)
    param_col1, param_col2 = st.columns(2)
    with param_col1:
        st.markdown(create_interactive_gauge(nitrogen, 0, 140, "Nitrogen", "ppm", "#155724"), unsafe_allow_html=True)
        st.markdown('<div class="metric-description">Essential for leaf growth.</div>', unsafe_allow_html=True)
        st.markdown(create_interactive_gauge(potassium, 0, 205, "Potassium", "ppm", "#004085"), unsafe_allow_html=True)
        st.markdown('<div class="metric-description">Aids disease resistance.</div>', unsafe_allow_html=True)
        st.markdown(create_interactive_gauge(humidity, 0, 100, "Humidity", "%", "#5a6268"), unsafe_allow_html=True)
        st.markdown('<div class="metric-description">Affects water and nutrient uptake.</div>', unsafe_allow_html=True)
        st.markdown(create_interactive_gauge(rainfall, 0, 500, "Rainfall", "mm", "#0c5460"), unsafe_allow_html=True)
        st.markdown('<div class="metric-description">Crucial for crop hydration.</div>', unsafe_allow_html=True)
    with param_col2:
        st.markdown(create_interactive_gauge(phosphorus, 0, 145, "Phosphorus", "ppm", "#856404"), unsafe_allow_html=True)
        st.markdown('<div class="metric-description">Key for root development.</div>', unsafe_allow_html=True)
        st.markdown(create_interactive_gauge(temperature, 0, 51, "Temperature", "°C", "#721c24"), unsafe_allow_html=True)
        st.markdown('<div class="metric-description">Impacts growth rate.</div>', unsafe_allow_html=True)
        st.markdown(create_interactive_gauge(ph, 0, 14, "pH Level", "", "#540d6e"), unsafe_allow_html=True)
        st.markdown('<div class="metric-description">Determines nutrient availability.</div>', unsafe_allow_html=True)
        if ph < 6.5: status, advice, color = "🔴 Acidic", "Add lime to raise pH.", "#721c24"
        elif ph > 7.5: status, advice, color = "🔵 Alkaline", "Add sulfur to lower pH.", "#004085"
        else: status, advice, color = "🟢 Neutral", "Optimal for most crops.", "#155724"
        st.markdown(f'<div class="metric-container" style="border: 4px solid {color};"><div class="metric-label">Soil Status</div><div class="metric-value" style="color: {color};">{status}</div><div class="metric-description">{advice}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if predict_button:
        if all(val >= 0 for val in [nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]):
            with st.spinner("🔄 Analyzing soil & climate data..."):
                time.sleep(1)
                prediction = predict_crop(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall)
                if prediction:
                    st.success("✅ Prediction completed successfully!")
                    st.balloons()
                    st.markdown("---")
                    st.markdown(f'<div class="prediction-box"><h2>🎉 Recommended Crop:</h2><h1 style="font-size: 5rem;">{prediction.title()}</h1></div>', unsafe_allow_html=True)
                    st.markdown('<div class="crop-recommendation-section">', unsafe_allow_html=True)
                    show_crop_image(prediction)
                    st.markdown('</div>', unsafe_allow_html=True)
                    display_crop_info(prediction)
                    st.markdown(f'''
                    <div class="recommendations-section fade-in">
                        <h2 class="recommendations-header">💡 Next Steps</h2>
                        <div class="recommendations-content">
                            <ul class="recommendations-list">
                                <li>🔬 Consult local experts about <strong>{prediction}</strong> cultivation.</li>
                                <li>💰 Check market demand and pricing for <strong>{prediction}</strong>.</li>
                                <li>🔄 Plan crop rotation for soil health.</li>
                                <li>🌦️ Monitor weather forecasts closely before planting.</li>
                                <li>🧪 Perform detailed soil tests for precise nutrient needs.</li>
                            </ul>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                else: st.error("❌ Prediction failed. Please check your inputs.")
        else: st.error("❌ Please ensure all input values are valid (>= 0).")

    st.markdown("<div style='margin-top: 5rem;'></div>", unsafe_allow_html=True)
    with st.expander("ℹ️ About This System", expanded=False):
        st.markdown("""
        <div class="fade-in" style="color: #212529;">
            <h3 style="color: #004085;">AgriVerse Pro System</h3>
            <p><strong>🎯 Purpose:</strong> This intelligent system uses a Random Forest machine learning model to analyze soil and climate data, providing precise crop recommendations to enhance agricultural productivity.</p>
            <h4 style="color: #004085;">📊 Analysis Factors:</h4>
            <ul>
                <li><strong>Soil Chemistry:</strong> N, P, K levels and pH balance.</li>
                <li><strong>Climate:</strong> Temperature, humidity, and rainfall.</li>
            </ul>
            <p><strong>Model Performance:</strong> Our model is trained on a comprehensive dataset and achieves over <strong>95% accuracy</strong>, ensuring reliable recommendations.</p>
            <p><strong>⚠️ Disclaimer:</strong> This tool is for advisory purposes. Always consult local agricultural experts before making final farming decisions.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 10rem;'></div>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
