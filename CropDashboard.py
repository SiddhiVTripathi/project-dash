import streamlit as st
import time
import pickle
import numpy as np 

with st.sidebar:
    service = st.selectbox(label='Dashboard',options=['Crop','Fertilizer','Health'],help='Select the service you want to use')
    with st.spinner(f"Loading models for {service} service.."):
        time.sleep(2)
    st.success("Done!!")

if service=='Crop':

    with st.form('Soil_details_form'):
        st.title("Find out the best crop for your farm")
        # Input soil details in widget
        nitrogen = st.text_input(label='Nitrogen',key='NitrogenVal',placeholder="0-140")
        phosphorus = st.text_input(label='Phosphorus',key='Phosphorus',placeholder="5-145")
        potassium = st.text_input(label='Potassium',key='Potassium',placeholder="5-205")
        temperature = st.text_input(label='Temprature',key='Temprature',placeholder="value (in C)")
        humidity = st.text_input(label='Humidity',key='Humidity',placeholder="14.0-100")
        ph = st.text_input(label="pH",key="pH",placeholder="0-14")
        rainfall = st.text_input(label="Rainfall",key="rainfall",placeholder="0-300")

        # submit the details
        submitted = st.form_submit_button("Recommend")
        # Run the model if details submitted
        if submitted:
            st.success("Submitted")
            model = pickle.load(open('model.pkl', 'rb'))
            final_features = np.array([[int(nitrogen), int(phosphorus), int(potassium), float(temperature), float(humidity), int(ph), int(rainfall)]])
            prediction = model.predict(final_features)
            output = prediction[0]
            st.write(output)
            st.stop()
            
elif service=='Fertilizer':
    with st.form('Fertliser_for_crop_form'):
        st.title("Find out the best Fertiliser for your Crop")
        # Input crop and soil details in widget
        crop = st.text_input(label='Crop',key='crop',placeholder="select from list of crops")
        nitrogen = st.text_input(label='Nitrogen',key='NitrogenVal',placeholder="0-140")
        phophorus = st.text_input(label='Phosphorus',key='Phosphorus',placeholder="5-145")
        potassium = st.text_input(label='Potassium',key='Potassium',placeholder="5-205")
        moisture = st.text_input(label='Soil Moisture',key='SoilMoisture',placeholder="Moisture Content Value")

        # submit the details
        submitted = st.form_submit_button("Suggest")
        # Run the model if details submitted
        if submitted:
            st.success("Submitted")
            st.stop()

elif service=='Health':
    with st.form('crops_health'):
        st.title("Find out about your crop's Health")
        # Input crop and soil details in widget
        insect_count = st.text_input(label='Insect Count',key='count',placeholder="Insect Count Value")
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            crop_type = st.radio(label='Crop Type',key='Croptype',options=(0,1))
        with col2:
            soil_type = st.radio(label='Soil Type',key='Soiltype',options=(0,1))
        with col3:
            pesticide_category = st.radio(label='Pesticide Category',key='pesticideCategory',options=(1,2,3))
        doses = st.text_input(label='Doses Per Week',key='dosesPerWeek',placeholder="Number of Doses per week")
        WeeksUsed = st.text_input(label='Weeks Used',key='WeeksUsed',placeholder="Number of Weeks Used")
        WeeksQuit = st.text_input(label='Weeks Quit',key='WeeksQuit',placeholder="Number of Weeks Quit")
        with col4:
            Season = st.radio(label="Season",options=(1,2,3))

        # submit the details
        submitted = st.form_submit_button("Predict")
        # Run the model if details submitted
        if submitted:
            st.success("Submitted")
            st.stop()