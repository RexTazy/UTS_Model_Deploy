model = load_model()

# ===== Judul Aplikasi =====
st.title("Fikri Aziz Biruni Project - 2702356362")
st.title("Hotel Booking Cancellation Prediction")
st.markdown("Masukkan data pemesanan hotel untuk memprediksi apakah pemesanan akan dibatalkan atau tidak.")

# ===== Inisialisasi nilai default untuk session_state =====
input_keys = {
    'no_of_adults': 0,
    'no_of_children': 0,
    'no_of_weekend_nights': 0,
    'no_of_week_nights': 0,
    'type_of_meal_plan': 'Meal Plan 1',
    'required_car_parking_space': 0,
    'room_type_reserved': 'Room Type 1',
    'lead_time': 100,
    'arrival_year': 2017,
    'arrival_month': 3,
    'arrival_date': 28,
    'market_segment_type': 'Online',
    'repeated_guest': 0,
    'no_of_previous_cancellations': 0,
    'no_of_previous_bookings_not_canceled': 0,
    'avg_price_per_room': 80.0,
    'no_of_special_requests': 0
}

for key, default_value in input_keys.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

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
        st.experimental_rerun()
with col2:
    if st.button("Test Case 2"):
        fill_test_case(2)
        st.experimental_rerun()

# ===== Input Form dari User =====
no_of_adults = st.number_input('Number of Adults', min_value=0, max_value=4, key='no_of_adults')
no_of_children = st.number_input('Number of Children', min_value=0,  max_value=10, key='no_of_children')
