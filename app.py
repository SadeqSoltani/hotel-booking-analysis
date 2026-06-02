import streamlit as st
import pandas as pd
import numpy as np
import joblib
import datetime
from sklearn.preprocessing import LabelEncoder

st.set_page_config(
    page_title="Hotel Cancellation Predictor",
    page_icon="🏨",
    layout="wide"
)

st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }

    /* Hide default streamlit header */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Hero header */
    .hero {
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
        border-radius: 20px;
        padding: 40px;
        margin-bottom: 30px;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        text-align: center;
    }
    .hero h1 {
        font-size: 2.8em;
        font-weight: 800;
        background: linear-gradient(90deg, #e94560, #0f3460, #533483);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .hero p {
        color: rgba(255,255,255,0.7);
        font-size: 1.1em;
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin: 10px 0;
    }
    .metric-card h2 {
        font-size: 2.5em;
        font-weight: 800;
        margin: 0;
    }
    .metric-card p {
        color: rgba(255,255,255,0.6);
        margin: 5px 0 0 0;
        font-size: 0.9em;
    }

    /* Risk badge */
    .risk-high {
        background: linear-gradient(135deg, #e94560, #c0392b);
        border-radius: 50px;
        padding: 15px 30px;
        font-size: 1.5em;
        font-weight: 800;
        color: white;
        text-align: center;
        box-shadow: 0 4px 20px rgba(233,69,96,0.5);
        animation: pulse 2s infinite;
    }
    .risk-medium {
        background: linear-gradient(135deg, #f39c12, #e67e22);
        border-radius: 50px;
        padding: 15px 30px;
        font-size: 1.5em;
        font-weight: 800;
        color: white;
        text-align: center;
        box-shadow: 0 4px 20px rgba(243,156,18,0.5);
    }
    .risk-low {
        background: linear-gradient(135deg, #27ae60, #2ecc71);
        border-radius: 50px;
        padding: 15px 30px;
        font-size: 1.5em;
        font-weight: 800;
        color: white;
        text-align: center;
        box-shadow: 0 4px 20px rgba(39,174,96,0.5);
    }

    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, #e94560, #533483);
        border-radius: 10px;
        padding: 12px 20px;
        margin: 20px 0 15px 0;
        font-weight: 700;
        font-size: 1.1em;
        color: white;
    }

    /* Input card */
    .input-card {
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 15px;
    }

    /* Stats bar */
    .stats-bar {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 15px 25px;
        display: flex;
        justify-content: space-around;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 25px;
    }

    /* Progress bar custom */
    .prob-bar-container {
        background: rgba(255,255,255,0.1);
        border-radius: 50px;
        height: 20px;
        margin: 10px 0;
        overflow: hidden;
    }

    /* Factor cards */
    .factor-warning {
        background: rgba(243,156,18,0.15);
        border-left: 4px solid #f39c12;
        border-radius: 8px;
        padding: 12px 15px;
        margin: 8px 0;
        color: #f39c12;
    }
    .factor-success {
        background: rgba(39,174,96,0.15);
        border-left: 4px solid #27ae60;
        border-radius: 8px;
        padding: 12px 15px;
        margin: 8px 0;
        color: #2ecc71;
    }
    .factor-info {
        background: rgba(52,152,219,0.15);
        border-left: 4px solid #3498db;
        border-radius: 8px;
        padding: 12px 15px;
        margin: 8px 0;
        color: #3498db;
    }

    /* Action box */
    .action-high {
        background: rgba(233,69,96,0.15);
        border: 2px solid #e94560;
        border-radius: 15px;
        padding: 20px;
        color: white;
    }
    .action-medium {
        background: rgba(243,156,18,0.15);
        border: 2px solid #f39c12;
        border-radius: 15px;
        padding: 20px;
        color: white;
    }
    .action-low {
        background: rgba(39,174,96,0.15);
        border: 2px solid #27ae60;
        border-radius: 15px;
        padding: 20px;
        color: white;
    }

    /* Streamlit elements override */
    .stSelectbox label, .stSlider label, .stRadio label {
        color: rgba(255,255,255,0.8) !important;
        font-weight: 500;
    }
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        color: white !important;
        border-radius: 10px !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #e94560, #533483) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 15px 40px !important;
        font-size: 1.1em !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 20px rgba(233,69,96,0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(233,69,96,0.6) !important;
    }
    div[data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2em !important;
        font-weight: 800 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: rgba(255,255,255,0.6) !important;
    }
    .stDivider {
        border-color: rgba(255,255,255,0.1) !important;
    }
    p, label {
        color: rgba(255,255,255,0.85) !important;
    }

    @keyframes pulse {
        0% { box-shadow: 0 4px 20px rgba(233,69,96,0.5); }
        50% { box-shadow: 0 4px 35px rgba(233,69,96,0.9); }
        100% { box-shadow: 0 4px 20px rgba(233,69,96,0.5); }
    }
</style>
""", unsafe_allow_html=True)

meal_map = {
    'Bed and Breakfast': 'BB',
    'Half Board': 'HB',
    'Full Board': 'FB',
    'Self Catering': 'SC',
    'No Meal': 'Undefined'
}
distribution_map = {
    'Travel Agent / Tour Operator': 'TA/TO',
    'Direct': 'Direct',
    'Corporate': 'Corporate',
    'Global Distribution System': 'GDS',
    'Undefined': 'Undefined'
}
room_type_map = {
    'Standard': 'A',
    'Superior': 'B',
    'Deluxe': 'C',
    'Executive': 'D',
    'Suite': 'E',
    'Junior Suite': 'F',
    'Family Room': 'G',
    'Presidential Suite': 'H',
    'Other': 'L'
}
country_map = {
    'Portugal': 'PRT',
    'United Kingdom': 'GBR',
    'France': 'FRA',
    'Spain': 'ESP',
    'Germany': 'DEU',
    'Italy': 'ITA',
    'Ireland': 'IRL',
    'Belgium': 'BEL',
    'Brazil': 'BRA',
    'Netherlands': 'NLD',
    'USA': 'USA',
    'Switzerland': 'CHE',
    'Other': 'Other'
}
segment_map = {
    'Online Travel Agency': 'Online TA',
    'Offline Travel Agency': 'Offline TA/TO',
    'Direct': 'Direct',
    'Groups': 'Groups',
    'Corporate': 'Corporate',
    'Aviation': 'Aviation',
    'Complementary': 'Complementary'
}
deposit_map = {
    'No Deposit': 'No Deposit',
    'Non Refundable': 'Non Refund',
    'Refundable': 'Refundable'
}


@st.cache_resource
def load_model():
    model = joblib.load('models/xgb_model.pkl')
    feature_columns = joblib.load('models/feature_columns.pkl')
    return model, feature_columns

model, feature_columns = load_model()


st.markdown("""
<div class="hero">
    <h1>🏨 Hotel Cancellation Risk Predictor</h1>
    <p>AI-powered cancellation prediction to optimize revenue and reduce no-shows</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="stats-bar">
    <div style="text-align:center">
        <div style="font-size:1.8em;font-weight:800;
                    color:#e94560">119,390</div>
        <div style="color:rgba(255,255,255,0.5);
                    font-size:0.85em">Bookings Trained</div>
    </div>
    <div style="text-align:center">
        <div style="font-size:1.8em;font-weight:800;
                    color:#e94560">95.29%</div>
        <div style="color:rgba(255,255,255,0.5);
                    font-size:0.85em">ROC-AUC Score</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-header">📋 Enter Booking Details</div>',
            unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown("**🏢 Booking Information**")
    hotel = st.selectbox("Hotel Type",
                         ["City Hotel", "Resort Hotel"])
    lead_time = st.slider("Lead Time (days)",
                          min_value=0, max_value=700,
                          value=60, step=1)
    deposit_type = st.selectbox("Deposit Type",
                                ["No Deposit",
                                 "Non Refundable",
                                 "Refundable"])
    market_segment = st.selectbox("Market Segment",
                                  ["Online Travel Agency",
                                   "Offline Travel Agency",
                                   "Direct", "Groups",
                                   "Corporate", "Aviation",
                                   "Complementary"])
    distribution_friendly = st.selectbox(
        "Booking Channel",
        list(distribution_map.keys()))
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown("**👥 Guest Information**")
    country = st.selectbox("Guest Country",
                           ["Portugal", "United Kingdom",
                            "France", "Spain", "Germany",
                            "Italy", "Ireland", "Belgium",
                            "Brazil", "Netherlands",
                            "USA", "Switzerland", "Other"])
    adults = st.slider("Number of Adults",
                       min_value=1, max_value=10, value=2)
    children = st.slider("Number of Children",
                         min_value=0, max_value=5, value=0)
    babies = st.slider("Number of Babies",
                       min_value=0, max_value=3, value=0)
    is_repeated_guest = st.radio("Repeat Guest?",
                                 ["No", "Yes"],
                                 horizontal=True)
    previous_cancellations = st.slider(
        "Previous Cancellations",
        min_value=0, max_value=10, value=0)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown("**🛏️ Stay Information**")
    stays_in_weekend_nights = st.slider(
        "Weekend Nights",
        min_value=0, max_value=10, value=1)
    stays_in_week_nights = st.slider(
        "Week Nights",
        min_value=0, max_value=14, value=2)
    meal_friendly = st.selectbox("Meal Plan",
                                 list(meal_map.keys()))
    reserved_room_friendly = st.selectbox(
        "Reserved Room Type",
        list(room_type_map.keys()))
    assigned_room_friendly = st.selectbox(
        "Assigned Room Type",
        list(room_type_map.keys()))
    total_of_special_requests = st.slider(
        "Number of Special Requests",
        min_value=0, max_value=5, value=0)
    required_car_parking_spaces = st.radio(
        "Parking Required?",
        ["No", "Yes"], horizontal=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


if st.button("🔍 Predict Cancellation Risk",
             type="primary",
             use_container_width=True):

   
    country_code = country_map[country]
    segment_code = segment_map[market_segment]
    deposit_code = deposit_map[deposit_type]
    meal_code = meal_map[meal_friendly]
    distribution_code = distribution_map[distribution_friendly]
    reserved_room_code = room_type_map[reserved_room_friendly]
    assigned_room_code = room_type_map[assigned_room_friendly]


    total_nights = (stays_in_weekend_nights +
                    stays_in_week_nights)
    total_guests = adults + children + babies
    total_revenue = 100 * total_nights
    room_match = (1 if reserved_room_code ==
                  assigned_room_code else 0)
    is_family = 1 if (children > 0 or babies > 0) else 0
    is_weekend_arrival = 0
    revenue_per_night = total_revenue / max(total_nights, 1)
    is_repeated = 1 if is_repeated_guest == "Yes" else 0
    parking = (1 if required_car_parking_spaces
               == "Yes" else 0)

  
    if lead_time == 0:
        lead_time_bucket = "1. Same day"
    elif lead_time <= 7:
        lead_time_bucket = "2. 1-7 days"
    elif lead_time <= 30:
        lead_time_bucket = "3. 8-30 days"
    elif lead_time <= 90:
        lead_time_bucket = "4. 31-90 days"
    elif lead_time <= 180:
        lead_time_bucket = "5. 91-180 days"
    else:
        lead_time_bucket = "6. 180+ days"

   
    now = datetime.datetime.now()
    month = now.month
    if month in [12, 1, 2]:
        season = "Winter"
    elif month in [3, 4, 5]:
        season = "Spring"
    elif month in [6, 7, 8]:
        season = "Summer"
    else:
        season = "Autumn"

  
    input_data = {
        'hotel': hotel,
        'lead_time': lead_time,
        'arrival_date_year': now.year,
        'arrival_date_month': now.strftime('%B'),
        'arrival_date_week_number': now.isocalendar()[1],
        'arrival_date_day_of_month': now.day,
        'stays_in_weekend_nights': stays_in_weekend_nights,
        'stays_in_week_nights': stays_in_week_nights,
        'adults': adults,
        'children': children,
        'babies': babies,
        'meal': meal_code,
        'country': country_code,
        'market_segment': segment_code,
        'distribution_channel': distribution_code,
        'is_repeated_guest': is_repeated,
        'previous_cancellations': previous_cancellations,
        'previous_bookings_not_canceled': 0,
        'reserved_room_type': reserved_room_code,
        'assigned_room_type': assigned_room_code,
        'booking_changes': 0,
        'deposit_type': deposit_code,
        'agent': 0,
        'company': 0,
        'days_in_waiting_list': 0,
        'customer_type': 'Transient',
        'adr': 100.0,
        'required_car_parking_spaces': parking,
        'total_of_special_requests': total_of_special_requests,
        'total_nights': total_nights,
        'total_revenue': total_revenue,
        'is_weekend_arrival': is_weekend_arrival,
        'season': season,
        'lead_time_bucket': lead_time_bucket,
        'room_match': room_match,
        'is_family': is_family,
        'total_guests': total_guests,
        'revenue_per_night': revenue_per_night,
    }

    input_df = pd.DataFrame([input_data])


    cat_cols_model = input_df.select_dtypes(
        include=['object']).columns.tolist()
    le = LabelEncoder()
    for col in cat_cols_model:
        input_df[col] = le.fit_transform(
            input_df[col].astype(str))
    input_df = input_df.reindex(
        columns=feature_columns, fill_value=0)


    prob = model.predict_proba(input_df)[0][1]
    avg_booking_value = 339.26
    expected_loss = prob * avg_booking_value


    if prob < 0.35:
        risk_level = "LOW RISK"
        risk_class = "risk-low"
        action_class = "action-low"
        action_icon = "✅"
        action_text = ("Standard booking — no intervention required. "
                       "Monitor as normal.")
    elif prob < 0.65:
        risk_level = "MEDIUM RISK"
        risk_class = "risk-medium"
        action_class = "action-medium"
        action_icon = "⚠️"
        action_text = ("Medium risk — consider sending a booking "
                       "confirmation reminder 30 days before arrival "
                       "or offering a complimentary room upgrade.")
    else:
        risk_level = "HIGH RISK"
        risk_class = "risk-high"
        action_class = "action-high"
        action_icon = "🚨"
        action_text = ("High risk — recommend requiring a deposit or "
                       "non-refundable rate. Consider proactive "
                       "outreach with upgrade or flexible date "
                       "change option.")


    st.markdown(
        '<div class="section-header">📊 Prediction Results</div>',
        unsafe_allow_html=True)

    res_col1, res_col2, res_col3 = st.columns(3)

    with res_col1:
        st.markdown(f"""
        <div class="metric-card">
            <p>Cancellation Probability</p>
            <h2 style="color:#e94560">{prob*100:.1f}%</h2>
            <div class="prob-bar-container">
                <div style="background:linear-gradient(90deg,
                    #27ae60,#f39c12,#e94560);
                    width:{prob*100}%;height:100%;
                    border-radius:50px;
                    transition:width 0.5s ease">
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with res_col2:
        st.markdown(f"""
        <div class="metric-card">
            <p>Risk Level</p>
            <div class="{risk_class}"
                 style="margin-top:10px">
                {risk_level}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with res_col3:
        st.markdown(f"""
        <div class="metric-card">
            <p>Expected Revenue at Risk</p>
            <h2 style="color:#f39c12">${expected_loss:.0f}</h2>
            <p style="font-size:0.8em">
                Based on avg booking value of $339
            </p>
        </div>
        """, unsafe_allow_html=True)

    
    st.markdown(
        '<div class="section-header">🔍 Key Risk Factors</div>',
        unsafe_allow_html=True)

    risk_factors = []
    if deposit_type == "Non Refundable":
        risk_factors.append((
            "💳 Non-refundable deposit — revenue secured "
            "regardless of cancellation status",
            "info"))
    if lead_time > 90:
        risk_factors.append((
            f"📅 Long lead time ({lead_time} days) — bookings "
            f"90+ days out cancel at 44-57%",
            "warning"))
    if market_segment == "Groups":
        risk_factors.append((
            "👥 Groups segment — highest cancellation "
            "rate at 61.1%",
            "warning"))
    if total_of_special_requests == 0:
        risk_factors.append((
            "📝 No special requests — guests with zero "
            "requests cancel at 47.7%",
            "warning"))
    if parking == 0:
        risk_factors.append((
            "🚗 No parking required — parking guests "
            "cancel at much lower rates",
            "warning"))
    if room_match == 0:
        risk_factors.append((
            "⬆️ Room upgraded — upgraded guests cancel "
            "at only 5.4% (positive signal)",
            "success"))
    if is_repeated == 1:
        risk_factors.append((
            "🔄 Repeat guest — cancels at only 14.5% "
            "(positive signal)",
            "success"))
    if previous_cancellations > 0:
        risk_factors.append((
            f"⚠️ Previous cancellations: "
            f"{previous_cancellations} — past behaviour "
            f"predicts future risk",
            "warning"))
    if country == "Portugal":
        risk_factors.append((
            "🇵🇹 Portuguese domestic guest — cancels at "
            "56.6% vs 37% overall average",
            "warning"))

    if risk_factors:
        for message, level in risk_factors:
            css_class = f"factor-{level}"
            st.markdown(
                f'<div class="{css_class}">{message}</div>',
                unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="factor-info">'
            'ℹ️ No major risk factors detected for '
            'this booking.</div>',
            unsafe_allow_html=True)


    st.markdown(
        '<div class="section-header">'
        '💡 Recommended Action</div>',
        unsafe_allow_html=True)
    st.markdown(f"""
    <div class="{action_class}">
        <strong>{action_icon} {risk_level}:</strong>
        {action_text}
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;
            color:rgba(255,255,255,0.4);
            font-size:0.85em;
            padding:20px;
            border-top:1px solid rgba(255,255,255,0.1)">
    🏨 Hotel Booking Demand Analysis &nbsp;|&nbsp;
    Built by Sadeq Soltani &nbsp;|&nbsp;
    XGBoost Model &nbsp;|&nbsp;
    ROC-AUC: 95.29% &nbsp;|&nbsp;
    <a href="https://github.com/SadeqSoltani"
       style="color:#e94560;text-decoration:none">
       GitHub
    </a>
</div>
""", unsafe_allow_html=True)