import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860" # Assuming 'backend' is the service name in Docker Compose/GitHub Codespaces

# Set the title of the Streamlit app
st.title("SuperKart Sales Prediction")

# Section for online prediction
st.subheader("Predict Sales for a Single Product-Store Combination")

# Collect user input for SuperKart features
product_id = st.text_input("Product ID", "FD6114")
product_weight = st.number_input("Product Weight", min_value=4.0, max_value=22.0, value=12.66)
product_sugar_content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar", "reg"])
product_allocated_area = st.number_input("Product Allocated Area", min_value=0.004, max_value=0.298, value=0.027, format="%.3f")
product_type = st.selectbox("Product Type", [
    "Fruits and Vegetables", "Snack Foods", "Frozen Foods", "Dairy",
    "Household", "Baking Goods", "Canned", "Health and Hygiene",
    "Meat", "Soft Drinks", "Breads", "Hard Drinks", "Others",
    "Starchy Foods", "Breakfast", "Seafood"
])
product_mrp = st.number_input("Product MRP", min_value=31.0, max_value=266.0, value=117.08)
store_id = st.selectbox("Store ID", ["OUT004", "OUT001", "OUT003", "OUT002"])
store_establishment_year = st.number_input("Store Establishment Year", min_value=1987, max_value=2009, value=2009, step=1)
store_size = st.selectbox("Store Size", ["Medium", "High", "Small"])
store_location_city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.selectbox("Store Type", ["Supermarket Type2", "Supermarket Type1", "Departmental Store", "Food Mart"])

# Prepare input data as a dictionary
input_data = {
    'Product_Id': product_id,
    'Product_Weight': product_weight,
    'Product_Sugar_Content': product_sugar_content,
    'Product_Allocated_Area': product_allocated_area,
    'Product_Type': product_type,
    'Product_MRP': product_mrp,
    'Store_Id': store_id,
    'Store_Establishment_Year': store_establishment_year,
    'Store_Size': store_size,
    'Store_Location_City_Type': store_location_city_type,
    'Store_Type': store_type
}

# Make prediction when the "Predict" button is clicked
if st.button("Predict Sales", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/superKart", json=input_data)
    if response.status_code == 200:
        prediction = response.json()['Predicted_Product_Store_Sales_Total']
        st.success(f"Predicted Product Store Sales Total: {prediction:.2f}")
    else:
        st.error(f"Error connecting to the prediction API: {response.status_code} - {response.text}")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Sales for Batch", type="primary"):
        files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'text/csv')}
        response = requests.post(f"{BACKEND_URL}/v1/superKartbatch", files=files)
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            # Convert dictionary to DataFrame for better display
            predictions_df = pd.DataFrame(predictions.items(), columns=['Product_Id', 'Predicted_Sales'])
            st.write(predictions_df)
        else:
            st.error(f"Error connecting to the batch prediction API: {response.status_code} - {response.text}")
