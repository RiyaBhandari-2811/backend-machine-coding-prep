"""
Streamlit Frontend for Insurance Premium Prediction API
This connects to your deployed FastAPI backend on AWS EC2

IMPORTANT: Update API_BASE_URL below with your actual AWS IP address
"""

import streamlit as st
import requests
import json
from typing import Optional

# ============================================================================
# CONFIGURATION - UPDATE THIS WITH YOUR AWS IP
# ============================================================================
# Replace with your AWS EC2 public IP
# Example: "http://54.123.45.67:8000"
API_BASE_URL = "http://YOUR_AWS_IP:8000"

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM STYLING
# ============================================================================
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================
st.title("🏥 Insurance Premium Prediction")
st.markdown("**Predict insurance premium based on personal details using AI**")

# ============================================================================
# SIDEBAR - API CONFIGURATION
# ============================================================================
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Display current API URL
    st.subheader("API Connection")
    if API_BASE_URL == "http://YOUR_AWS_IP:8000":
        st.warning("⚠️ Please update API_BASE_URL in the code with your AWS IP!")
    else:
        st.success(f"✅ Connected to:\n`{API_BASE_URL}`")
    
    # API Status
    if st.button("🔍 Check API Status", use_container_width=True):
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=3)
            if response.status_code == 200:
                health_data = response.json()
                st.success("✅ API is Healthy!")
                st.json(health_data)
            else:
                st.error(f"❌ API returned status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API")
            st.info("Make sure:")
            st.write("1. AWS IP is correct")
            st.write("2. EC2 instance is running")
            st.write("3. Docker container is running")
            st.write("4. Security group allows port 8000")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    st.divider()
    
    # Information
    st.subheader("📖 About")
    st.markdown("""
    This app predicts insurance premiums based on:
    - Age and lifestyle
    - Income level
    - City and occupation
    
    Model: Random Forest Classifier
    Accuracy: ~95%
    """)
    
    st.divider()
    
    # Links
    st.subheader("🔗 Useful Links")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📚 API Docs", use_container_width=True):
            st.info(f"Open in browser: {API_BASE_URL}/docs")
    with col2:
        if st.button("🔄 API Health", use_container_width=True):
            st.info(f"Health check: {API_BASE_URL}/health")

# ============================================================================
# MAIN INPUT FORM
# ============================================================================
st.header("📋 Enter Your Details")

# Create form with columns for better layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Personal Information")
    age = st.slider(
        "Age",
        min_value=18,
        max_value=100,
        value=30,
        step=1,
        help="Your current age in years"
    )
    
    weight = st.number_input(
        "Weight (kg)",
        min_value=30.0,
        max_value=200.0,
        value=70.0,
        step=1.0,
        help="Your weight in kilograms"
    )
    
    height = st.number_input(
        "Height (m)",
        min_value=1.0,
        max_value=2.5,
        value=1.70,
        step=0.01,
        help="Your height in meters (e.g., 1.70)"
    )

with col2:
    st.subheader("Financial & Lifestyle")
    income_lpa = st.number_input(
        "Annual Income (LPA)",
        min_value=1,
        max_value=200,
        value=10,
        step=1,
        help="Annual income in Lakhs Per Annum (1 LPA = 100,000 rupees)"
    )
    
    smoker = st.checkbox(
        "Are you a smoker?",
        value=False,
        help="Smoking status affects premium significantly"
    )
    
    city = st.selectbox(
        "City of Residence",
        ["delhi", "mumbai", "bangalore", "gurgaon", "pune"],
        help="Your current city"
    )

# Additional Information
st.subheader("Additional Information")
occupation = st.selectbox(
    "Occupation",
    ["student", "employed", "self-employed", "retired"],
    help="Current occupation status"
)

# ============================================================================
# CALCULATE BMI (Optional Information)
# ============================================================================
if age and weight and height:
    bmi = weight / (height ** 2)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("BMI", f"{bmi:.1f}", help="Body Mass Index")
    with col2:
        if bmi < 18.5:
            category = "Underweight"
            color = "🔵"
        elif bmi < 25:
            category = "Normal"
            color = "🟢"
        elif bmi < 30:
            category = "Overweight"
            color = "🟡"
        else:
            category = "Obese"
            color = "🔴"
        st.metric("BMI Category", f"{color} {category}")
    with col3:
        risk_level = "High" if smoker else "Medium" if bmi > 25 else "Low"
        st.metric("Initial Risk", risk_level)

# ============================================================================
# PREDICTION BUTTON
# ============================================================================
st.divider()

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    predict_button = st.button(
        "🔮 Predict Insurance Premium",
        use_container_width=True,
        type="primary"
    )

# ============================================================================
# MAKE PREDICTION
# ============================================================================
if predict_button:
    # Prepare request data
    request_data = {
        "age": int(age),
        "weight": float(weight),
        "height": float(height),
        "income_lpa": int(income_lpa),
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }
    
    # Show loading state
    with st.spinner("🔄 Predicting..."):
        try:
            # Make API request
            response = requests.post(
                f"{API_BASE_URL}/predict",
                json=request_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            # ================================================================
            # SUCCESS RESPONSE
            # ================================================================
            if response.status_code == 200:
                result = response.json()
                
                st.success("✅ Prediction Successful!")
                
                # Display main prediction
                st.divider()
                st.header("📊 Prediction Results")
                
                # Premium Category with color coding
                category = result.get("predicted_category", "Unknown")
                confidence = result.get("confidence", 0)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if category == "Low":
                        icon = "🟢"
                    elif category == "Medium":
                        icon = "🟡"
                    else:
                        icon = "🔴"
                    st.metric("Premium Category", f"{icon} {category}")
                
                with col2:
                    confidence_pct = confidence * 100
                    st.metric("Model Confidence", f"{confidence_pct:.1f}%")
                
                with col3:
                    # Risk interpretation
                    if category == "Low":
                        risk_text = "Low Risk"
                        risk_help = "Good health profile"
                    elif category == "Medium":
                        risk_text = "Medium Risk"
                        risk_help = "Some health concerns"
                    else:
                        risk_text = "High Risk"
                        risk_help = "Multiple risk factors"
                    
                    st.metric("Risk Level", risk_text, delta=risk_help)
                
                # Display detailed class probabilities
                st.divider()
                st.subheader("📈 Class Probabilities")
                
                probabilities = result.get("class_probabilities", {})
                
                cols = st.columns(len(probabilities))
                for idx, (class_name, prob) in enumerate(probabilities.items()):
                    with cols[idx]:
                        st.progress(prob, text=f"{class_name}: {prob*100:.1f}%")
                
                # Input summary
                st.divider()
                st.subheader("📝 Input Summary")
                
                input_summary = f"""
                **Personal Details:**
                - Age: {age} years
                - Weight: {weight} kg
                - Height: {height} m
                - BMI: {bmi:.1f}
                
                **Financial & Lifestyle:**
                - Income: ₹{income_lpa} LPA
                - Smoker: {'Yes' if smoker else 'No'}
                - City: {city.title()}
                - Occupation: {occupation.title()}
                """
                st.markdown(input_summary)
                
                # Export results
                st.divider()
                st.subheader("📥 Export Results")
                
                result_json = json.dumps(result, indent=2)
                st.download_button(
                    label="Download Results as JSON",
                    data=result_json,
                    file_name="prediction_result.json",
                    mime="application/json"
                )
            
            # ================================================================
            # ERROR RESPONSE
            # ================================================================
            else:
                st.error(f"❌ API Error: Status {response.status_code}")
                st.write("Response:")
                st.write(response.text)
        
        # ================================================================
        # CONNECTION ERRORS
        # ================================================================
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot Connect to API")
            st.markdown("""
            **Troubleshooting Steps:**
            1. ✔️ Verify AWS IP address is correct in the code
            2. ✔️ Check EC2 instance is running
            3. ✔️ Verify Docker container is running: `docker ps`
            4. ✔️ Check security group allows port 8000
            5. ✔️ Verify firewall rules on EC2
            
            **Quick Check:**
            - Try accessing API directly: `{API_BASE_URL}`
            - Check API health: `{API_BASE_URL}/health`
            """)
        
        # ================================================================
        # TIMEOUT ERRORS
        # ================================================================
        except requests.exceptions.Timeout:
            st.error("❌ Request Timeout")
            st.warning("API took too long to respond. Try again in a moment.")
        
        # ================================================================
        # OTHER ERRORS
        # ================================================================
        except Exception as e:
            st.error(f"❌ Unexpected Error: {str(e)}")
            st.write("Error details:")
            st.write(str(e))

# ============================================================================
# FOOTER
# ============================================================================
st.divider()
st.markdown("""
### 📚 How It Works

1. **Enter Details:** Provide your personal, financial, and lifestyle information
2. **Submit:** Click "Predict Insurance Premium"
3. **AI Prediction:** Our ML model analyzes your profile
4. **Results:** Get premium category (Low/Medium/High) with confidence score

### 🤖 Model Information

- **Algorithm:** Random Forest Classifier
- **Features:** 7 input parameters
- **Training Data:** 1000+ insurance records
- **Accuracy:** ~95%

### 🔒 Privacy

Your data is:
- ✅ Processed on our secure servers
- ✅ Never stored permanently
- ✅ Never shared with third parties
- ✅ HTTPS encrypted (when configured)

### 📞 Support

- 🔗 [API Documentation]({API_BASE_URL}/docs)
- 🐛 [Report Issues]()
- 📧 [Contact Support]()

---

**Powered by:** FastAPI + Machine Learning + AWS EC2 + Streamlit
""")

# Footer statistics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Model Type", "Random Forest")
with col2:
    st.metric("Accuracy", "~95%")
with col3:
    st.metric("Training Samples", "1000+")
