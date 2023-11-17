import streamlit as st
import pandas as pd
import joblib
st.set_page_config(
    page_title="Crop Recommendation System",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown("<h1 style='text-align: center;'>Crop Recommendation System</h1>", unsafe_allow_html=True)
df_desc = pd.read_csv('D:/agrids/Crop_Desc.csv', sep=';', encoding='utf-8')
df = pd.read_csv('D:/agrids/Crop_recommendation.csv')
rdf_clf = joblib.load('rdf_clf.pkl')
st.markdown("<h3 style='text-align: center;'>Please input the feature values to predict the best crop to plant.</h3><br>", unsafe_allow_html=True)
n_input = st.number_input('Insert N (kg/ha) value:', min_value=0, max_value=140)
p_input = st.number_input('Insert P (kg/ha) value:', min_value=5, max_value=145)
k_input = st.number_input('Insert K (kg/ha) value:', min_value=5, max_value=205)
temp_input = st.number_input('Insert Avg Temperature (ºC) value:', min_value=9., max_value=43., step=1., format="%.2f")
hum_input = st.number_input('Insert Avg Humidity (%) value:', min_value=15., max_value=99., step=1., format="%.2f")
ph_input = st.number_input('Insert pH value:', min_value=3.6, max_value=9.9, step=0.1, format="%.2f")
rain_input = st.number_input('Insert Avg Rainfall (mm) value:', min_value=21.0, max_value=298.0, step=0.1, format="%.2f")
st.markdown("<br>", unsafe_allow_html=True)
predict_btn = st.button('Recommend Crop')
st.markdown("<br>", unsafe_allow_html=True)
cola, colb = st.columns([6, 6])
if predict_btn:
    predict_inputs = [[n_input, p_input, k_input, temp_input, hum_input, ph_input, rain_input]]
    rdf_predicted_value = rdf_clf.predict(predict_inputs)

    with cola:
        st.markdown(f"<h5>Best Crop to Plant: <b>{rdf_predicted_value[0]}</b></h5>", unsafe_allow_html=True)

    with colb:
        df_desc = df_desc.astype({'label': str, 'image': str})
        df_desc['label'] = df_desc['label'].str.strip()
        df_desc['image'] = df_desc['image'].str.strip()

        df_pred_image = df_desc[df_desc['label'].isin(rdf_predicted_value)]
        df_image = df_pred_image['image'].item()

        st.markdown(f"""<h5 style = 'text-align: left; height: 300px; object-fit: contain;'> {df_image} </h5>""",
                    unsafe_allow_html=True)


