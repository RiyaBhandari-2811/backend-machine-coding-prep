"""
Chapter 6: Streamlit Frontend for ML Model Prediction
Insurance Premium Predictor - User Interface

This Streamlit app:
- Provides UI for insurance premium prediction
- Sends user input to FastAPI backend
- Displays prediction results
- Shows confidence factors and explanations

How to run:
    streamlit run frontend.py --server.port 8501

Requirements:
    streamlit
    requests
    pandas

API Expected at: http://localhost:8000/predict
"""

import streamlit as st
import requests
import pandas as pd
from typing import Dict, Any

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

st.sidebar.header("⚙️ Settings")

api_url = st.sidebar.text_input(
    "API Endpoint",
    value="http://localhost:8000",
    help="Base URL of FastAPI server"
)

api_endpoint = f"{api_url}/predict"

debug_mode = st.sidebar.checkbox("Debug Mode", value=False)

st.sidebar.divider()
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    ### About
    This app predicts insurance premium categories
    based on personal and health attributes.
    
    **Powered by:**
    - FastAPI (Backend)
    - Scikit-learn (ML Model)
    - Streamlit (Frontend)
    
    **Premium Categories:**
    - 🟢 **Low** - Lower insurance premium
    - 🟡 **Medium** - Average premium
    - 🔴 **High** - Higher insurance premium
    """
)

# ============================================================================
# MAIN CONTENT
# ============================================================================

st.title("🛡️ Insurance Premium Predictor")
st.markdown(
    """
    Enter your details below to get your insurance premium prediction.
    The AI model considers your health, lifestyle, and financial factors.
    """
)

st.divider()

# ============================================================================
# FORM LAYOUT
# ============================================================================

st.subheader("📋 Your Information")

# Create two columns for better layout
col1, col2 = st.columns(2)

with col1:
    age = st.number_input(
        "Age (years)",
        min_value=0,
        max_value=100,
        value=35,
        help="Your age in years"
    )
    
    weight = st.number_input(
        "Weight (kg)",
        min_value=30.0,
        max_value=200.0,
        value=70.0,
        step=0.5,
        help="Your body weight in kilograms"
    )
    
    height = st.number_input(
        "Height (m)",
        min_value=1.2,
        max_value=2.5,
        value=1.70,
        step=0.01,
        help="Your height in meters (e.g., 1.72)"
    )
    
    income_lpa = st.number_input(
        "Annual Income (LPA)",
        min_value=0.0,
        max_value=500.0,
        value=15.0,
        step=0.5,
        help="Annual salary in Lakh Per Annum (1 LPA = 100,000 INR)"
    )

with col2:
    smoker = st.selectbox(
        "Are you a smoker?",
        options=["No", "Yes"],
        index=0,
        help="Do you smoke cigarettes or other tobacco products?"
    )
    smoker_bool = smoker == "Yes"
    
    city = st.text_input(
        "City",
        value="Bangalore",
        placeholder="e.g., Mumbai, Delhi, Bangalore",
        help="City of residence (used for tier classification)"
    )
    
    occupation = st.selectbox(
        "Occupation",
        options=[
            "Software Engineer",
            "Doctor",
            "Teacher",
            "Business Owner",
            "Government Job",
            "Unemployed",
            "Retired",
            "Others"
        ],
        index=0,
        help="Your professional category"
    )

st.divider()

# ============================================================================
# PREDICTION BUTTON & LOGIC
# ============================================================================

# Center the button
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    predict_button = st.button(
        "🔮 Predict Premium Category",
        use_container_width=True,
        type="primary"
    )

# ============================================================================
# HANDLE PREDICTION
# ============================================================================

if predict_button:
    # Prepare request payload
    payload = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker_bool,
        "city": city,
        "occupation": occupation
    }
    
    if debug_mode:
        st.info(f"📤 Sending to {api_endpoint}")
        st.json(payload)
    
    # Make API request
    with st.spinner("🔄 Processing your request..."):
        try:
            response = requests.post(
                api_endpoint,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Display prediction result
                st.success("✅ Prediction Complete!")
                st.divider()
                
                # ============================================================
                # RESULT DISPLAY
                # ============================================================
                
                # Large category display with color coding
                category = result.get("predicted_category", "Unknown")
                
                # Color mapping
                color_map = {
                    "Low": ("🟢", "green"),
                    "Medium": ("🟡", "orange"),
                    "High": ("🔴", "red")
                }
                
                emoji, color = color_map.get(category, ("❓", "gray"))
                
                # Display category prominently
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown(
                        f"""
                        <div style="text-align: center; padding: 30px; 
                                    background-color: {color}; 
                                    border-radius: 10px; color: white;">
                            <h2>{emoji} {category}</h2>
                            <p style="font-size: 16px;">Premium Category</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                st.divider()
                
                # Display explanation
                st.subheader("📖 Explanation")
                explanation = result.get("explanation", "No explanation available")
                st.info(explanation)
                
                st.divider()
                
                # Display confidence factors (features used in prediction)
                st.subheader("🔬 Analysis Factors")
                
                factors = result.get("confidence_factors", {})
                
                # Create tabs for different views
                tab1, tab2 = st.tabs(["Table View", "Detailed View"])
                
                with tab1:
                    # Convert factors to dataframe for nice display
                    factors_df = pd.DataFrame([factors]).T
                    factors_df.columns = ["Value"]
                    st.dataframe(factors_df, use_container_width=True)
                
                with tab2:
                    # Detailed explanation of each factor
                    factor_descriptions = {
                        "age_group": "Age category (Young/Adult/Middle-aged/Senior)",
                        "lifestyle_risk": "Health risk assessment (Low/Medium/High)",
                        "bmi": "Body Mass Index (weight/height²)",
                        "city_tier": "City classification (1=Metro, 2=Second-tier, 3=Other)",
                        "income_lpa": "Annual income in Lakh Per Annum",
                        "occupation": "Professional category"
                    }
                    
                    for factor, value in factors.items():
                        description = factor_descriptions.get(
                            factor,
                            "Factor description not available"
                        )
                        st.write(f"**{factor.replace('_', ' ').title()}**")
                        st.write(f"Value: `{value}`")
                        st.write(f"*{description}*")
                        st.divider()
                
                st.divider()
                
                # Display recommendation
                st.subheader("💡 Recommendations")
                
                if category == "High":
                    st.warning(
                        "⚠️ **High Premium Category Detected**\n\n"
                        "Consider these improvements to lower your premium:\n"
                        "- 🚭 **Quit smoking** - Most impactful change\n"
                        "- 💪 **Lose weight** - Achieve healthy BMI (< 25)\n"
                        "- 🏃 **Exercise regularly** - Improves overall health\n"
                        "- 🥗 **Eat healthy** - Balanced diet\n"
                        "- 📍 **Relocate if possible** - Tier-1 cities may have different rates"
                    )
                
                elif category == "Medium":
                    st.info(
                        "ℹ️ **Medium Premium Category**\n\n"
                        "You can potentially improve your category:\n"
                        "- 💪 **Exercise more** - Reduce BMI\n"
                        "- 🚭 **Avoid smoking** - Critical factor\n"
                        "- 👨‍⚕️ **Regular check-ups** - Maintain good health"
                    )
                
                else:  # Low
                    st.success(
                        "✨ **Low Premium Category - Great!**\n\n"
                        "You qualify for lower insurance rates!\n"
                        "- ✅ Maintain your healthy lifestyle\n"
                        "- 🏃 Continue regular exercise\n"
                        "- 👨‍⚕️ Keep up regular health check-ups"
                    )
                
                # Debug info (if enabled)
                if debug_mode:
                    st.divider()
                    st.subheader("🐛 Debug Information")
                    st.json(result)
            
            else:
                # API error
                st.error(f"❌ API Error: {response.status_code}")
                st.error(response.text)
        
        except requests.exceptions.ConnectionError:
            st.error(
                "❌ **Cannot connect to API server!**\n\n"
                "Make sure FastAPI server is running:\n"
                "```bash\n"
                "uvicorn main:app --reload --port 8000\n"
                "```"
            )
        
        except requests.exceptions.Timeout:
            st.error("⏱️ **Request timeout!** Server taking too long to respond.")
        
        except requests.exceptions.RequestException as e:
            st.error(f"❌ **Request error:** {str(e)}")
        
        except Exception as e:
            st.error(f"❌ **Unexpected error:** {str(e)}")

st.divider()

# ============================================================================
# FOOTER / INFO
# ============================================================================

st.markdown(
    """
    ---
    
    ### 📚 How It Works
    
    1. **You enter** your personal and health information
    2. **AI model** analyzes factors like age, BMI, lifestyle, and income
    3. **Prediction** is made: Low / Medium / High premium
    4. **Recommendations** are provided to improve your category
    
    ### 🔐 Privacy
    Your data is processed locally and not stored permanently.
    
    ### ❓ Questions?
    - Check the sidebar for feature explanations
    - Visit `/docs` on the API server for API documentation
    - Review the code comments for technical details
    
    ---
    **Chapter 6: Machine Learning Model Serving with FastAPI**
    """
)
