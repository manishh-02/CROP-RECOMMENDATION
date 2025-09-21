<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AgriVision Pro | AI-Powered Crop Recommendation</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Roboto+Slab:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary: #1e3c72;
            --secondary: #2a5298;
            --accent: #ff6b35;
            --light: #f8f9fa;
            --dark: #343a40;
            --success: #28a745;
            --warning: #ffc107;
            --danger: #dc3545;
            --gradient-primary: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            --gradient-accent: linear-gradient(135deg, #ff6b35 0%, #e55a2b 100%);
            --gradient-success: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            --gradient-warning: linear-gradient(135deg, #ffc107 0%, #ff9900 100%);
            --shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
            --shadow-hover: 0 15px 40px rgba(0, 0, 0, 0.25);
            --transition: all 0.3s ease;
            --transition-slow: all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        body {
            font-family: 'Poppins', sans-serif;
            color: var(--dark);
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e7ec 100%);
            min-height: 100vh;
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Header Styles */
        header {
            background: var(--gradient-primary);
            color: white;
            padding: 20px 0;
            border-bottom-left-radius: 20px;
            border-bottom-right-radius: 20px;
            box-shadow: var(--shadow);
            position: relative;
            overflow: hidden;
        }

        header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            animation: shine 4s infinite;
            z-index: 1;
        }

        @keyframes shine {
            0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
        }

        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: relative;
            z-index: 2;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .logo i {
            font-size: 2.5rem;
            color: #ffd700;
            filter: drop-shadow(0 0 5px rgba(255, 215, 0, 0.5));
        }

        .logo-text {
            font-family: 'Roboto Slab', serif;
            font-weight: 700;
            font-size: 2rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .nav-links {
            display: flex;
            gap: 30px;
        }

        .nav-links a {
            color: white;
            text-decoration: none;
            font-weight: 500;
            transition: var(--transition);
            padding: 8px 15px;
            border-radius: 50px;
        }

        .nav-links a:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-3px);
        }

        /* Hero Section */
        .hero {
            padding: 80px 0;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .hero-content {
            max-width: 800px;
            margin: 0 auto;
            position: relative;
            z-index: 2;
        }

        .hero h1 {
            font-family: 'Roboto Slab', serif;
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 20px;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }

        .hero p {
            font-size: 1.2rem;
            margin-bottom: 30px;
            color: var(--dark);
        }

        .hero-buttons {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-top: 30px;
        }

        .btn {
            padding: 15px 30px;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1rem;
            border: none;
            cursor: pointer;
            transition: var(--transition);
            display: inline-flex;
            align-items: center;
            gap: 10px;
            box-shadow: var(--shadow);
        }

        .btn-primary {
            background: var(--gradient-primary);
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-hover);
        }

        .btn-outline {
            background: transparent;
            color: var(--primary);
            border: 2px solid var(--primary);
        }

        .btn-outline:hover {
            background: var(--primary);
            color: white;
            transform: translateY(-5px);
            box-shadow: var(--shadow-hover);
        }

        /* Features Section */
        .features {
            padding: 80px 0;
            background: white;
            border-radius: 20px;
            box-shadow: var(--shadow);
            margin: 40px 0;
        }

        .section-title {
            text-align: center;
            margin-bottom: 60px;
            font-family: 'Roboto Slab', serif;
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--primary);
            position: relative;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: -15px;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 4px;
            background: var(--gradient-accent);
            border-radius: 2px;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }

        .feature-card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: var(--shadow);
            transition: var(--transition);
            text-align: center;
            border: 1px solid rgba(0, 0, 0, 0.05);
        }

        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: var(--shadow-hover);
        }

        .feature-icon {
            width: 80px;
            height: 80px;
            background: var(--gradient-primary);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            font-size: 2rem;
            color: white;
        }

        .feature-card h3 {
            font-size: 1.5rem;
            margin-bottom: 15px;
            color: var(--primary);
        }

        /* Input Form Section */
        .input-section {
            padding: 80px 0;
            background: var(--gradient-primary);
            border-radius: 20px;
            box-shadow: var(--shadow);
            margin: 40px 0;
            color: white;
        }

        .form-container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        }

        .form-title {
            text-align: center;
            margin-bottom: 40px;
            font-family: 'Roboto Slab', serif;
            font-size: 2.2rem;
        }

        .input-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
        }

        .input-group {
            margin-bottom: 20px;
        }

        .input-group label {
            display: block;
            margin-bottom: 10px;
            font-weight: 500;
        }

        .input-group input {
            width: 100%;
            padding: 15px;
            border-radius: 10px;
            border: none;
            background: rgba(255, 255, 255, 0.9);
            font-size: 1rem;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            transition: var(--transition);
        }

        .input-group input:focus {
            outline: none;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
            transform: translateY(-3px);
        }

        .slider-container {
            margin-top: 10px;
        }

        .slider {
            -webkit-appearance: none;
            width: 100%;
            height: 10px;
            border-radius: 5px;
            background: rgba(255, 255, 255, 0.3);
            outline: none;
        }

        .slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 25px;
            height: 25px;
            border-radius: 50%;
            background: var(--accent);
            cursor: pointer;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
            transition: var(--transition);
        }

        .slider::-webkit-slider-thumb:hover {
            transform: scale(1.2);
            box-shadow: 0 0 15px rgba(255, 107, 53, 0.5);
        }

        .value-display {
            text-align: center;
            font-weight: 600;
            margin-top: 10px;
            font-size: 1.1rem;
            color: white;
            background: rgba(255, 255, 255, 0.1);
            padding: 5px 10px;
            border-radius: 5px;
            display: inline-block;
        }

        .submit-btn {
            display: block;
            width: 100%;
            padding: 18px;
            background: var(--gradient-accent);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.2rem;
            font-weight: 600;
            margin-top: 30px;
            cursor: pointer;
            transition: var(--transition);
            box-shadow: 0 5px 20px rgba(229, 90, 43, 0.4);
        }

        .submit-btn:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(229, 90, 43, 0.6);
        }

        /* Results Section */
        .results-section {
            padding: 80px 0;
            background: white;
            border-radius: 20px;
            box-shadow: var(--shadow);
            margin: 40px 0;
            text-align: center;
        }

        .result-card {
            background: var(--gradient-success);
            color: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: var(--shadow);
            margin: 0 auto;
            max-width: 600px;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1); box-shadow: 0 10px 30px rgba(40, 167, 69, 0.5); }
            50% { transform: scale(1.02); box-shadow: 0 15px 40px rgba(40, 167, 69, 0.7); }
            100% { transform: scale(1); box-shadow: 0 10px 30px rgba(40, 167, 69, 0.5); }
        }

        .result-card h2 {
            font-size: 2.5rem;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .result-card p {
            font-size: 1.2rem;
            margin-bottom: 30px;
        }

        .crop-image {
            width: 200px;
            height: 200px;
            border-radius: 50%;
            object-fit: cover;
            border: 5px solid white;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            margin: 0 auto 30px;
        }

        /* Footer */
        footer {
            background: var(--gradient-primary);
            color: white;
            padding: 40px 0;
            border-top-left-radius: 20px;
            border-top-right-radius: 20px;
            margin-top: 80px;
        }

        .footer-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .footer-logo {
            font-family: 'Roboto Slab', serif;
            font-size: 1.8rem;
            font-weight: 700;
        }

        .footer-links {
            display: flex;
            gap: 20px;
        }

        .footer-links a {
            color: white;
            text-decoration: none;
            transition: var(--transition);
        }

        .footer-links a:hover {
            color: #ffd700;
            transform: translateY(-3px);
        }

        .social-icons {
            display: flex;
            gap: 15px;
        }

        .social-icons a {
            color: white;
            font-size: 1.5rem;
            transition: var(--transition);
        }

        .social-icons a:hover {
            color: #ffd700;
            transform: translateY(-5px);
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                gap: 20px;
            }

            .nav-links {
                flex-wrap: wrap;
                justify-content: center;
            }

            .hero h1 {
                font-size: 2.5rem;
            }

            .hero-buttons {
                flex-direction: column;
                align-items: center;
            }

            .footer-content {
                flex-direction: column;
                gap: 30px;
                text-align: center;
            }

            .input-grid {
                grid-template-columns: 1fr;
            }
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .fade-in {
            animation: fadeIn 1s ease-out;
        }

        .delay-1 { animation-delay: 0.2s; }
        .delay-2 { animation-delay: 0.4s; }
        .delay-3 { animation-delay: 0.6s; }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="header-content">
                <div class="logo">
                    <i class="fas fa-seedling"></i>
                    <div class="logo-text">AgriVision Pro</div>
                </div>
                <div class="nav-links">
                    <a href="#"><i class="fas fa-home"></i> Home</a>
                    <a href="#"><i class="fas fa-info-circle"></i> About</a>
                    <a href="#"><i class="fas fa-cogs"></i> Features</a>
                    <a href="#"><i class="fas fa-phone"></i> Contact</a>
                </div>
            </div>
        </div>
    </header>

    <div class="container">
        <section class="hero">
            <div class="hero-content fade-in">
                <h1>AI-Powered Crop Recommendation System</h1>
                <p>Maximize your agricultural yield with our advanced AI system that analyzes soil conditions, climate data, and environmental factors to recommend the perfect crops for your farm.</p>
                <div class="hero-buttons">
                    <button class="btn btn-primary"><i class="fas fa-play"></i> Get Started</button>
                    <button class="btn btn-outline"><i class="fas fa-book"></i> Learn More</button>
                </div>
            </div>
        </section>

        <section class="features">
            <h2 class="section-title">How It Works</h2>
            <div class="features-grid">
                <div class="feature-card fade-in delay-1">
                    <div class="feature-icon">
                        <i class="fas fa-vial"></i>
                    </div>
                    <h3>Soil Analysis</h3>
                    <p>Our system analyzes NPK levels and pH balance of your soil to determine the optimal conditions for different crops.</p>
                </div>
                <div class="feature-card fade-in delay-2">
                    <div class="feature-icon">
                        <i class="fas fa-cloud-sun"></i>
                    </div>
                    <h3>Climate Check</h3>
                    <p>We evaluate temperature, humidity, and rainfall patterns to match crops with your local climate conditions.</p>
                </div>
                <div class="feature-card fade-in delay-3">
                    <div class="feature-icon">
                        <i class="fas fa-robot"></i>
                    </div>
                    <h3>AI Prediction</h3>
                    <p>Our advanced machine learning algorithm processes all data to provide accurate crop recommendations with over 95% accuracy.</p>
                </div>
            </div>
        </section>

        <section class="input-section">
            <h2 class="section-title" style="color: white;">Enter Your Farm Details</h2>
            <div class="form-container">
                <div class="input-grid">
                    <div class="input-group">
                        <label for="nitrogen">Nitrogen Level (N)</label>
                        <input type="range" min="0" max="140" value="50" class="slider" id="nitrogen">
                        <div class="value-display">Value: <span id="nitrogen-value">50</span> ppm</div>
                    </div>
                    <div class="input-group">
                        <label for="phosphorus">Phosphorus Level (P)</label>
                        <input type="range" min="0" max="145" value="50" class="slider" id="phosphorus">
                        <div class="value-display">Value: <span id="phosphorus-value">50</span> ppm</div>
                    </div>
                    <div class="input-group">
                        <label for="potassium">Potassium Level (K)</label>
                        <input type="range" min="0" max="205" value="50" class="slider" id="potassium">
                        <div class="value-display">Value: <span id="potassium-value">50</span> ppm</div>
                    </div>
                    <div class="input-group">
                        <label for="temperature">Temperature</label>
                        <input type="range" min="0" max="50" value="25" class="slider" id="temperature">
                        <div class="value-display">Value: <span id="temperature-value">25</span> °C</div>
                    </div>
                    <div class="input-group">
                        <label for="humidity">Humidity</label>
                        <input type="range" min="0" max="100" value="60" class="slider" id="humidity">
                        <div class="value-display">Value: <span id="humidity-value">60</span> %</div>
                    </div>
                    <div class="input-group">
                        <label for="ph">pH Level</label>
                        <input type="range" min="0" max="14" value="7" step="0.1" class="slider" id="ph">
                        <div class="value-display">Value: <span id="ph-value">7</span></div>
                    </div>
                    <div class="input-group">
                        <label for="rainfall">Rainfall</label>
                        <input type="range" min="0" max="500" value="100" class="slider" id="rainfall">
                        <div class="value-display">Value: <span id="rainfall-value">100</span> mm</div>
                    </div>
                </div>
                <button class="submit-btn" id="predict-btn">
                    <i class="fas fa-calculator"></i> Predict Optimal Crop
                </button>
            </div>
        </section>

        <section class="results-section" id="results" style="display: none;">
            <h2 class="section-title">Recommended Crop</h2>
            <div class="result-card">
                <img src="https://images.unsplash.com/photo-1612393266591-c3292f8a3a1f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&q=80" alt="Wheat" class="crop-image">
                <h2>Wheat</h2>
                <p>Based on your soil and climate conditions, wheat is the most suitable crop for your farm with a 92% compatibility score.</p>
                <button class="btn btn-outline"><i class="fas fa-download"></i> Download Full Report</button>
            </div>
        </section>
    </div>

    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-logo">AgriVision Pro</div>
                <div class="footer-links">
                    <a href="#">Privacy Policy</a>
                    <a href="#">Terms of Service</a>
                    <a href="#">Contact Us</a>
                </div>
                <div class="social-icons">
                    <a href="#"><i class="fab fa-facebook"></i></a>
                    <a href="#"><i class="fab fa-twitter"></i></a>
                    <a href="#"><i class="fab fa-instagram"></i></a>
                    <a href="#"><i class="fab fa-linkedin"></i></a>
                </div>
            </div>
        </div>
    </footer>

    <script>
        // Update slider values in real-time
        const sliders = document.querySelectorAll('.slider');
        sliders.forEach(slider => {
            const valueDisplay = slider.nextElementSibling.querySelector('span');
            valueDisplay.textContent = slider.value;
            
            slider.addEventListener('input', () => {
                valueDisplay.textContent = slider.value;
            });
        });

        // Show results on button click
        const predictBtn = document.getElementById('predict-btn');
        const resultsSection = document.getElementById('results');
        
        predictBtn.addEventListener('click', () => {
            resultsSection.style.display = 'block';
            resultsSection.scrollIntoView({ behavior: 'smooth' });
            
            // Add confetti effect (simulated)
            predictBtn.innerHTML = '<i class="fas fa-check"></i> Prediction Complete!';
            predictBtn.style.background = 'var(--gradient-success)';
            
            // Reset button after 3 seconds
            setTimeout(() => {
                predictBtn.innerHTML = '<i class="fas fa-calculator"></i> Predict Optimal Crop';
                predictBtn.style.background = 'var(--gradient-accent)';
            }, 3000);
        });

        // Add animations on scroll
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        }, observerOptions);

        document.querySelectorAll('.feature-card, .section-title').forEach(el => {
            observer.observe(el);
        });
    </script>
</body>
</html>
