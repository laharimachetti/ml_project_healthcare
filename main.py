# main.py
import os

import requests
import streamlit as st

from prediction import predict

st.set_page_config(page_title="Health Insurance Cost Predictor", layout="wide")

# -------------------------
# Helper to load lottie
# -------------------------
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=6)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

success_anim = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_jbrw3hcz.json")

# -------------------------
# CSS (hero, card, inputs)
# -------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 50%, #fbc2eb 100%);
        min-height: 100vh;
        font-family: 'Segue UI', system-ui, sans-serif;
    }
    .container {
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
        padding-top: 24px;
        padding-bottom: 40px;
    }
    .hero-title {
        text-align: center;
        color: #000000;
        font-size: 48px;
        font-weight: 800;
        margin-bottom: 6px;
        letter-spacing: -0.5px;
    }
    .hero-sub {
        text-align: center;
        color: rgba(0,0,0,0.95);
        font-size: 18px;
        margin-bottom: 26px;
        font-weight: 500;
    }
    /* Form box */
    .form-panel {
        background: rgba(255,255,255,0.96);
        border-radius: 16px;
        padding: 28px 28px 36px 28px;
        box-shadow: 0 14px 50px rgba(16,24,40,0.12);
        width: 100%;
    }
    
    /* Make all input labels bold */
    .stTextInput label,
    .stNumberInput label,
    .stSelect box label,
    .stDateInput label {
    font-weight: 700 !important;
    color: #000000 !important;
    }

    .left-wrap {
        width: 520px;
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 12px;
    }
    .result-card {
        margin-top: 8px;
        padding: 22px;
        border-radius: 14px;
        background: #ffffff;
        box-shadow: 0 10px 30px rgba(16,24,40,0.12);
        text-align: center;
        width: 100%;
    }
    .result-title { color:#2e86de; font-size:20px; font-weight:700; margin-bottom:6px; }
    .result-amount { font-size:28px; color:#27ae60; font-weight:800; }
    .tick-icon {
        font-size: 32px;
        color: #0eca3a;
    }
    .stButton>button {
        background-color: #28a745 !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 10px 26px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        box-shadow: 0 6px 18px rgba(40,167,69,0.18) !important;
    }
    .stButton>button:hover { transform: translateY(-2px); }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Page content (hero)
# -------------------------
st.markdown('<div class="container">', unsafe_allow_html=True)
st.markdown('<div class="hero-title">💡 Health Insurance Cost Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Protecting your health with smarter predictions</div>', unsafe_allow_html=True)

# -------------------------
# Layout: left image + right form
# -------------------------
left_col, right_col = st.columns([1,1])

# LEFT SIDE
with left_col:
    doctor_path = "doctor.png"
    if not os.path.exists(doctor_path):
        alt = "/mnt/data/doctor.png"
        if os.path.exists(alt):
            doctor_path = alt
        else:
            doctor_path = os.path.join(os.path.dirname(__file__), "doctor.png")
            
    left_container = st.container()
    left_container.image(doctor_path, width=520)
    result_placeholder = left_container.empty()

# RIGHT SIDE (whole form inside one panel box)
with right_col:
    with st.container():
        st.markdown('<div class="form-panel">', unsafe_allow_html=True)

        # --- all your existing inputs unchanged ---
        r1c1, r1c2, r1c3 = st.columns(3)
        with r1c1:
            age = st.number_input("Age", 18, 100, 20, step=1, key="age")
        with r1c2:
            number_of_dependants = st.number_input("Number of Dependants", 0, 20, 0, step=1, key="dependants")
        with r1c3:
            income_lakhs = st.number_input("Income in Lakhs", 0, 1000, 2, step=1, key="income")

        r2c1, r2c2, r2c3 = st.columns(3)
        with r2c1:
            genetical_risk = st.number_input("Genetical Risk (0-5)", 0, 5, 0, step=1, key="genetic")
        with r2c2:
            insurance_plan = st.selectbox("Insurance Plan", ["Bronze", "Silver", "Gold"], index=0, key="plan")
        with r2c3:
            employment_status = st.selectbox("Employment Status", ["Salaried", "Self-Employed", "Freelancer"], index=0, key="employment")

        r3c1, r3c2, r3c3 = st.columns(3)
        with r3c1:
            gender = st.selectbox("Gender", ["Male", "Female"], index=0, key="gender")
        with r3c2:
            marital_status = st.selectbox("Marital Status", ["Unmarried", "Married"], index=0, key="marital")
        with r3c3:
            bmi_category = st.selectbox("BMI Category", ["Normal", "Obesity", "Overweight", "Underweight"], index=0, key="bmi")

        r4c1, _, r4c3 = st.columns([1, 0.1, 1])
        with r4c1:
            smoking_status = st.selectbox("Smoking Status", ["No Smoking", "Regular", "Occasional"], index=0, key="smoking")
        with r4c3:
            region = st.selectbox("Region", ["Northwest", "Southeast", "Northeast", "Southwest"], index=0, key="region")

        medical_history = st.selectbox(
            "Medical History",
            [
                'No Disease', 'Diabetes', 'High blood pressure',
                'Diabetes & High blood pressure', 'Thyroid', 'Heart disease',
                'High blood pressure & Heart disease', 'Diabetes & Thyroid',
                'Diabetes & Heart disease'
            ],
            index=0,
            key="medical"
        )

        btn_col1, btn_col2, btn_col3 = st.columns([1, 0.6, 1])
        with btn_col2:
            predict_clicked = st.button("🚀 Predict", key="predict_btn")

        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# Prediction Result
# -------------------------
if 'predict_clicked' in locals() and predict_clicked:
    input_dict = {
        'Age': age,
        'Number of Dependants': number_of_dependants,
        'Income in Lakhs': income_lakhs,
        'Genetical Risk': genetical_risk,
        'Insurance Plan': insurance_plan,
        'Employment Status': employment_status,
        'Gender': gender,
        'Marital Status': marital_status,
        'BMI Category': bmi_category,
        'Smoking Status': smoking_status,
        'Region': region,
        'Medical History': medical_history
    }

    try:
        prediction_value = predict(input_dict)
        try:
            formatted = f"₹ {float(prediction_value):,.0f}"
        except Exception:
            formatted = f"{prediction_value}"
    except Exception as e:
        formatted = None
        result_placeholder.markdown(
            f'<div class="left-wrap"><div class="result-card"><div class="result-title">⚠️ Prediction Error</div>'
            f'<div style="color:#cc3333;">{str(e)}</div></div></div>',
            unsafe_allow_html=True,
        )

    if formatted is not None:
        inner_html = f"""
            <div class="left-wrap">
                <div class="result-card">
                    <div class="result-title">🔔 Prediction Result</div>
                    <div style="font-size:16px; color:#000; margin-top:6px;">
                        Your Predicted Health Insurance Cost:
                    </div>
                    <div style="display:flex; align-items:center; justify-content:center; gap:12px; margin-top:10px;">
                        <div class="result-amount">{formatted}</div>
                        <div class="tick-icon">✅</div>
                    </div>
                </div>
            </div>
        """
        result_placeholder.markdown(inner_html, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
