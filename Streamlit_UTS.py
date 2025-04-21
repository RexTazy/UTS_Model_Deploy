import streamlit as st
import pandas as pd
import joblib

# ===== Load Model =====
@st.cache_resource
def load_model():
    return joblib.load("RF_model.pkl")

model = load_model()

# ===== Judul Aplikasi =====
st.title("Fikri Aziz Biruni Project - 2702356362")
st.title("Hotel Booking Cancellation Prediction")
st.markdown("Masukkan data pemesanan hotel untuk memprediksi apakah pemesanan akan dibatalkan atau tidak.")

def fill_test_case(case_id):
    if case_id == 1:
        st.session_state.no_of_adults = 2
        st.session_state.no_of_children = 1
        st.session_state.no_of_weekend_nights = 1
        st.session_state.no_of_week_nights = 3
        st.session_state.type_of_meal_plan = 'Meal Plan 1'
        st.session_state.required_car_parking_space = 1
        st.session_state.room_type_reserved = 'Room Type 1'
        st.session_state.lead_time = 100
        st.session_state.arrival_year = 2017
        st.session_state.arrival_month = 7
        st.session_state.arrival_date = 15
        st.session_state.market_segment_type = 'Online'
        st.session_state.repeated_guest = 0
        st.session_state.no_of_previous_cancellations = 0
        st.session_state.no_of_previous_bookings_not_canceled = 2
        st.session_state.avg_price_per_room = 80.5
        st.session_state.no_of_special_requests = 1

    elif case_id == 2:
        st.session_state.no_of_adults = 1
        st.session_state.no_of_children = 0
        st.session_state.no_of_weekend_nights = 0
        st.session_state.no_of_week_nights = 1
        st.session_state.type_of_meal_plan = 'Not Selected'
        st.session_state.required_car_parking_space = 0
        st.session_state.room_type_reserved = 'Room Type 3'
        st.session_state.lead_time = 10
        st.session_state.arrival_year = 2018
        st.session_state.arrival_month = 12
        st.session_state.arrival_date = 5
        st.session_state.market_segment_type = 'Corporate'
        st.session_state.repeated_guest = 1
        st.session_state.no_of_previous_cancellations = 2
        st.session_state.no_of_previous_bookings_not_canceled = 1
        st.session_state.avg_price_per_room = 150.0
        st.session_state.no_of_special_requests = 0

# Tombol test case
col1, col2 = st.columns(2)
with col1:
    if st.button("Test Case 1"):
        fill_test_case(1)
with col2:
    if st.button("Test Case 2"):
        fill_test_case(2)

# ===== Input Form dari User =====
no_of_adults = st.number_input('Number of Adults', min_value=0, max_value=4, key='no_of_adults')
no_of_children = st.number_input('Number of Children', min_value=0,  max_value=10, key='no_of_children')
no_of_weekend_nights = st.number_input('Number of Weekend Nights', min_value=0, max_value=7, key='no_of_weekend_nights')
no_of_week_nights = st.number_input('Number of Week Nights', min_value=0, max_value=17, key='no_of_week_nights')
type_of_meal_plan = st.selectbox('Meal Plan', ['Meal Plan 1', 'Meal Plan 2', 'Meal Plan 3', 'Not Selected'], key='type_of_meal_plan')
required_car_parking_space = st.selectbox('Required Car Parking Space', [0, 1], key='required_car_parking_space')
room_type_reserved = st.selectbox('Room Type Reserved', ['Room Type 1', 'Room Type 2', 'Room Type 3', 'Room Type 4', 'Room Type 5', 'Room Type 6', 'Room Type 7'], key='room_type_reserved')
lead_time = st.number_input('Lead Time', min_value=0, max_value=443, value=100, key='lead_time')
arrival_year = st.number_input('Arrival Year', min_value=2017, max_value=2018, value=2017, key='arrival_year')
arrival_month = st.number_input('Arrival Month', min_value=1, max_value=12, value=3, key='arrival_month')
arrival_date = st.number_input('Arrival Date', min_value=1, max_value=31, value=28, key='arrival_date')
market_segment_type = st.selectbox('Market Segment Type', ['Aviation', 'Complementary', 'Corporate', 'Offline', 'Online'], key='market_segment_type')
repeated_guest = st.number_input('Repeated Guest', min_value=0, max_value=1, value=0, key='repeated_guest')
no_of_previous_cancellations = st.number_input('Number of Previous Cancellations', min_value=0, max_value=13, value=0, key='no_of_previous_cancellations')
no_of_previous_bookings_not_canceled = st.number_input('Number of Previous Bookings Not Canceled', min_value=0, max_value=58, value=0, key='no_of_previous_bookings_not_canceled')
avg_price_per_room = st.number_input('Average Price per Room', min_value=0.0, max_value=540.00, key='avg_price_per_room')
no_of_special_requests = st.number_input('Number of Special Requests', min_value=0, max_value=5, key='no_of_special_requests')

# ===== Submit Button =====
if st.button("Predict"):
    # Buat dataframe dari input user
    user_input = pd.DataFrame([{
        'no_of_adults': no_of_adults,
        'no_of_children': no_of_children,
        'no_of_weekend_nights': no_of_weekend_nights,
        'no_of_week_nights': no_of_week_nights,
        'type_of_meal_plan': type_of_meal_plan,
        'required_car_parking_space': required_car_parking_space,
        'room_type_reserved': room_type_reserved,
        'lead_time': lead_time,
        'arrival_year': arrival_year,
        'arrival_month': arrival_month,
        'arrival_date': arrival_date,
        'market_segment_type': market_segment_type,
        'repeated_guest': repeated_guest,
        'no_of_previous_cancellations': no_of_previous_cancellations,
        'no_of_previous_bookings_not_canceled': no_of_previous_bookings_not_canceled,
        'avg_price_per_room': avg_price_per_room,
        'no_of_special_requests': no_of_special_requests
    }])

    # One-hot encode kolom kategorikal
    categorical_cols = ['type_of_meal_plan', 'room_type_reserved', 'market_segment_type']
    user_input = pd.get_dummies(user_input, columns=categorical_cols)

    # Reindex agar kolom input cocok dengan model
    model_features = model.feature_names_in_
    user_input = user_input.reindex(columns=model_features, fill_value=0)

    # Prediksi
    prediction = model.predict(user_input)[0]
    result_text = "Not Canceled ✅" if prediction == 1 else "Canceled ❌"

    # Tampilkan hasil
    st.subheader("Prediksi:")

    if prediction == 1:
        st.success(result_text)
    else:
        st.error(result_text)
