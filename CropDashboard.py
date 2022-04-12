import streamlit as st
import time
import pickle
import pandas as pd
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
            if nitrogen and phosphorus and potassium and temperature and humidity and ph and rainfall:
                st.success("Submitted")
                model = pickle.load(open('model.pkl', 'rb'))
                final_features = np.array([[int(nitrogen), int(phosphorus), int(potassium), float(temperature), float(humidity), int(ph), int(rainfall)]])
                prediction = model.predict(final_features)
                output = prediction[0]
                st.write(output)
                st.stop()
            else:
                st.error("All feilds are mandatory")
            
elif service=='Fertilizer':
    with st.form('Fertliser_for_crop_form'):
        st.title("Find out the best Fertiliser for your Crop")
        df = pd.read_csv("Data/fertilizer.csv",usecols=["Crop","N","P","K","pH","soil_moisture"])
        # Input crop and soil details in widget
        Crop = st.selectbox(label="Crop",options=df['Crop'])
        nitrogen = int(st.text_input(label='Nitrogen',key='NitrogenVal',placeholder="0-140"))
        phosphorus = int(st.text_input(label='Phosphorus',key='Phosphorus',placeholder="5-145"))
        potassium = int(st.text_input(label='Potassium',key='Potassium',placeholder="5-205"))
        moisture = int(st.text_input(label='Soil Moisture',key='SoilMoisture',placeholder="Moisture Content Value"))

        # submit the details
        submitted = st.form_submit_button("Suggest")
        # Run the model if details submitted
        if submitted:
            st.success("Submitted")
        
            nr = df[df['Crop'] == Crop]['N'].iloc[0]
            pr = df[df['Crop'] == Crop]['P'].iloc[0]
            kr = df[df['Crop'] == Crop]['K'].iloc[0]

            n = nr - nitrogen
            p = pr - phosphorus
            k = kr - potassium
            temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
            max_value = temp[max(temp.keys())]
            if max_value == "N":
                if n < 0:
                    output = 'High in Nitrogen'
                else:
                    output = "Low in Nitrogen"
            elif max_value == "P":
                if p < 0:
                    output = 'High in Phosphorus'
                else:
                    output = "Low in Phosphorus"
            else:
                if k < 0:
                    output = 'High in Potassium'
                else:
                    output = "Low in Potassium"
            st.write(output)
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
            model1 = pickle.load(open('health.pkl', 'rb'))

            Estimated_Insects_Count = int(insect_count)
            Crop_Type = int(crop_type)
            if(Crop_Type == 0):
                Crop_Type_0 = 1
                Crop_Type_1 = 0
            else:
                Crop_Type_0 = 0
                Crop_Type_1 = 1
            
            Soil_Type = int(soil_type)
            if(Soil_Type == 0):
                Soil_Type_0 = 1
                Soil_Type_1 = 0
            else:
                Soil_Type_0 = 0
                Soil_Type_1 = 1
            
            Pesticide_Use_Category = int(pesticide_category)
            if(Pesticide_Use_Category == 1):
                Pesticide_Use_Category_1 = 1
                Pesticide_Use_Category_2 = 0
                Pesticide_Use_Category_3 = 0
            elif(Pesticide_Use_Category == 2):
                Pesticide_Use_Category_1 = 0
                Pesticide_Use_Category_2 = 1
                Pesticide_Use_Category_3 = 0
            else:
                Pesticide_Use_Category_1 = 0
                Pesticide_Use_Category_2 = 0
                Pesticide_Use_Category_3 = 1
            
            Number_Doses_Week = int(doses)
            Number_Weeks_Used = int(WeeksUsed)
            Number_Weeks_Quit = int(WeeksQuit)
            
            Season = int(Season)
            if(Season == 1):
                Season_1 = 1
                Season_2 = 0
                Season_3 = 0
            elif(Season == 2):
                Season_1 = 0
                Season_2 = 1
                Season_3 = 0
            else:
                Season_1 = 0
                Season_2 = 0
                Season_3 = 1

            final_features = np.array([[Estimated_Insects_Count,Number_Doses_Week, Number_Weeks_Used, Number_Weeks_Quit, Crop_Type_0, Crop_Type_1, Soil_Type_0, Soil_Type_1, Pesticide_Use_Category_1, Pesticide_Use_Category_2, Pesticide_Use_Category_3, Season_1, Season_2, Season_3]])
            prediction = model1.predict(final_features)
            output = prediction[0]

            if output== 0:
                output = "No health Issues"
            elif output == 1:
                output = "Damage due to other Cause"
            else:
                output = "Damage due to Pesticides"
            st.write(output)
            st.stop()