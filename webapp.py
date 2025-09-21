# app.py - Complete Deployable Crop Recommendation System

import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import os
import warnings
from PIL import Image

warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="AgriSens - Smart Crop Recommendation",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fixed Custom CSS for proper visibility
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        font-weight: bold;
    }
    
    .info-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2.5rem;
        border-radius: 15px;
        border: 3px solid #2E8B57;
        margin: 2rem 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    
    .info-section h3 {
        color: #2E8B57 !important;
        font-size: 2.2rem !important;
        margin-bottom: 1.5rem !important;
        font-weight: bold !important;
        text-align: center !important;
    }
    
    .info-section p {
        color: #333333 !important;
        font-size: 1.3rem !important;
        text-align: center !important;
        margin: 0 !important;
        font-weight: 500 !important;
        line-height: 1.6 !important;
    }
    
    .feature-container {
        display: flex;
        justify-content: space-around;
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .feature-box {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #2E8B57;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        flex: 1;
        margin: 0.5rem;
    }
    
    .feature-box h4 {
        color: #2E8B57 !important;
        font-size: 1.4rem !important;
        margin-bottom: 1rem !important;
        font-weight: bold !important;
    }
    
    .feature-box p {
        color: #555 !important;
        font-size: 1rem !important;
        line-height: 1.5 !important;
        margin: 0 !important;
    }
    
    .parameters-section {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #2E8B57;
        margin: 2rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .section-header {
        color: #2E8B57 !important;
        font-size: 1.8rem !important;
        font-weight: bold !important;
        margin-bottom: 1.5rem !important;
        text-align: center !important;
        border-bottom: 2px solid #2E8B57;
        padding-bottom: 0.5rem;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        text-align: center;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
    }
    
    .prediction-box {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    
    /* Override Streamlit's default styles */
    .stMetric {
        background: white !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        border: 1px solid #e0e0e0 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    
    .stMetric > div {
        color: #333 !important;
    }
    
    .stMetric label {
        font-weight: bold !important;
        color: #2E8B57 !important;
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
    """Display crop image if available"""
    image_path = os.path.join('crop_images', f"{crop_name.lower()}.jpg")
    if os.path.exists(image_path):
        try:
            crop_image = Image.open(image_path)
            st.image(crop_image, caption=f"Recommended crop: {crop_name}", use_column_width=True)
        except Exception as e:
            st.warning(f"Could not load image for {crop_name}: {e}")
    else:
        # Create a placeholder or show text instead
        st.info(f"🌱 Recommended crop: **{crop_name}**")

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
    """Display information about the recommended crop"""
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
        st.markdown(f'<div class="metric-card"><strong>Season</strong><br>{info["season"]}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><strong>Water Need</strong><br>{info["water"]}</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><strong>Temperature</strong><br>{info["temp"]}</div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><strong>Soil Type</strong><br>{info["soil"]}</div>', unsafe_allow_html=True)

def main():
    # Load and display header image
    try:
        if os.path.exists("crop.png"):
            img = Image.open("crop.png")
            st.image(img, use_column_width=True)
    except Exception as e:
        st.info("Header image not found - continuing without it")
    
    # Title
    st.markdown('<h1 class="main-header">🌾 SMART CROP RECOMMENDATIONS</h1>', unsafe_allow_html=True)
    
    # Sidebar for inputs
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
    
    # Main content area - Fixed "How It Works" section
    st.markdown("""
    <div class="info-section">
        <h3>🎯 How It Works</h3>
        <p>Our AI-powered system analyzes soil nutrients and environmental conditions to recommend the most suitable crop for your farm. Simply enter your soil and weather parameters in the sidebar and click 'Predict Crop' to get instant recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features section with proper HTML structure
    st.markdown('<div class="feature-container">', unsafe_allow_html=True)
    
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
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Parameters section with proper visibility
    st.markdown('<div class="parameters-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">📋 Current Parameters</h2>', unsafe_allow_html=True)
    
    param_col1, param_col2 = st.columns(2)
    
    with param_col1:
        st.markdown(f'<div class="metric-container"><strong>Nitrogen</strong><br><span style="font-size: 1.5rem; color: #2E8B57;">{nitrogen} ppm</span><br><small>Essential for leaf growth and green color</small></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-container"><strong>Phosphorus</strong><br><span style="font-size: 1.5rem; color: #2E8B57;">{phosphorus} ppm</span><br><small>Important for root development and flowering</small></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-container"><strong>Potassium</strong><br><span style="font-size: 1.5rem; color: #2E8B57;">{potassium} ppm</span><br><small>Helps in disease resistance and fruit quality</small></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-container"><strong>Temperature</strong><br><span style="font-size: 1.5rem; color: #2E8B57;">{temperature} °C</span><br><small>Average growing season temperature</small></div>', unsafe_allow_html=True)
    
    with param_col2:
        st.markdown(f'<div class="metric-container"><strong>Humidity</strong><br><span style="font-size: 1.5rem; color: #2E8B57;">{humidity} %</span><br><small>Relative humidity percentage</small></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-container"><strong>pH Level</strong><br><span style="font-size: 1.5rem; color: #2E8B57;">{ph}</span><br><small>Soil acidity/alkalinity level</small></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-container"><strong>Rainfall</strong><br><span style="font-size: 1.5rem; color: #2E8B57;">{rainfall} mm</span><br><small>Annual precipitation amount</small></div>', unsafe_allow_html=True)
        
        # Soil quality indicator
        if ph < 6.5:
            soil_status = "🔴 Acidic"
            ph_advice = "Consider adding lime to increase pH"
        elif ph > 7.5:
            soil_status = "🔵 Alkaline" 
            ph_advice = "Consider adding sulfur to decrease pH"
        else:
            soil_status = "🟢 Neutral"
            ph_advice = "Optimal pH range for most crops"
        
        st.markdown(f'<div class="metric-container"><strong>Soil Status</strong><br><span style="font-size: 1.5rem;">{soil_status}</span><br><small>{ph_advice}</small></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Prediction section
    if predict_button:
        # Validate inputs
        if all([nitrogen > 0, phosphorus > 0, potassium > 0, temperature > 0, humidity > 0, ph > 0, rainfall >= 0]):
            with st.spinner("🔄 Analyzing soil conditions and predicting optimal crop..."):
                prediction = predict_crop(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall)
                
                if prediction:
                    st.markdown("---")
                    
                    # Main prediction result
                    st.markdown(f"""
                    <div class="prediction-box">
                        <h2>🎉 Recommendation Result</h2>
                        <h1>{prediction.title()}</h1>
                        <p>Based on your soil and environmental conditions, <strong>{prediction.title()}</strong> is the most suitable crop for your farm!</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display crop image
                    st.subheader("🖼️ Crop Visualization")
                    show_crop_image(prediction)
                    
                    # Display crop information
                    st.subheader("📊 Crop Information")
                    display_crop_info(prediction)
                    
                    # Additional recommendations
                    st.subheader("💡 Additional Recommendations")
                    st.info(f"""
                    **Next Steps:**
                    - Consult with local agricultural experts about {prediction} cultivation
                    - Check local market demand and pricing for {prediction}
                    - Consider crop rotation practices for sustainable farming
                    - Monitor weather forecasts before planting
                    - Test soil samples for more accurate nutrient analysis
                    """)
                    
                    st.success("✅ Prediction completed successfully!")
                else:
                    st.error("❌ Unable to make prediction. Please check your input values and try again.")
        else:
            st.error("❌ Please enter valid values for all parameters (greater than 0, except rainfall which can be 0).")
    
    # Footer information
    st.markdown("---")
    with st.expander("ℹ️ About This System"):
        st.markdown("""
        **AgriSens Crop Recommendation System**
        
        This intelligent system uses machine learning to analyze multiple factors:
        - **Soil Chemistry**: NPK levels and pH balance
        - **Climate Conditions**: Temperature, humidity, and rainfall patterns
        - **Agricultural Best Practices**: Season compatibility and water requirements
        
        **Supported Crops**: Rice, Wheat, Maize, Cotton, Sugarcane, Jute, Coffee, Coconut, Apple, Banana, 
        Grapes, Watermelon, Muskmelon, Orange, Papaya, Pomegranate, Mango, Mothbeans, Pigeonpeas, 
        Kidneybeans, Chickpea, Lentil, Blackgram, Mungbean
        
        **Model Performance**: Our Random Forest model achieves over 95% accuracy on test data.
        
        **Disclaimer**: This tool provides AI-based recommendations for educational and advisory purposes. 
        Always consult with agricultural experts and consider local conditions before making farming decisions.
        
        **Data Source**: Based on agricultural research data and farming best practices.
        """)
    
    # Performance metrics (if model exists)
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
            
            # Quick tips in sidebar
            st.sidebar.markdown("---")
            st.sidebar.markdown("### 💡 Quick Tips")
            st.sidebar.info("🌱 Higher N = Leafy crops")
            st.sidebar.info("🌸 Higher P = Root/Flower crops") 
            st.sidebar.info("🍎 Higher K = Fruit quality")
            st.sidebar.info("🌡️ Temperature affects growth rate")
            st.sidebar.info("💧 Humidity affects disease risk")

if __name__ == '__main__':
    main()
