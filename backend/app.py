# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
super_kart_predictor_api = Flask("Super Kart Predictor")

# Load the trained machine learning model
model = joblib.load("super_kart_sales_prediction_model.joblib")

# Define a route for the home page (GET request)
@super_kart_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Sales Prediction API!"

# Define an endpoint for single product prediction (POST request)
@super_kart_predictor_api.post('/v1/superKart')
def super_kart_predict_single():
    """
    This function handles POST requests to the '/v1/superKart' endpoint.
    It expects a JSON payload containing product and store details and returns
    the predicted sales as a JSON response.
    """
    # Get the JSON data from the request body
    product_data = request.get_json()

    # Extract relevant features from the JSON data for SuperKart
    sample = {
        'Product_Id': product_data['Product_Id'],
        'Product_Weight': product_data['Product_Weight'],
        'Product_Sugar_Content': product_data['Product_Sugar_Content'],
        'Product_Allocated_Area': product_data['Product_Allocated_Area'],
        'Product_Type': product_data['Product_Type'],
        'Product_MRP': product_data['Product_MRP'],
        'Store_Id': product_data['Store_Id'],
        'Store_Establishment_Year': product_data['Store_Establishment_Year'],
        'Store_Size': product_data['Store_Size'],
        'Store_Location_City_Type': product_data['Store_Location_City_Type'],
        'Store_Type': product_data['Store_Type']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction (model already outputs actual sales)
    predicted_sales = model.predict(input_data)[0]

    # Convert predicted_sales to Python float and round
    predicted_sales = round(float(predicted_sales), 2)

    # Return the actual sales prediction
    return jsonify({'Predicted_Product_Store_Sales_Total': predicted_sales})


# Define an endpoint for batch prediction (POST request)
@super_kart_predictor_api.post('/v1/superKartbatch')
def predict_super_kart_batch():
    """
    This function handles POST requests to the '/v1/superKartbatch' endpoint.
    It expects a CSV file containing product and store details for multiple entries
    and returns the predicted sales as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all products in the DataFrame
    predicted_sales_list = model.predict(input_data).tolist()

    # Round predictions to 2 decimal places
    predicted_sales_rounded = [round(float(s), 2) for s in predicted_sales_list]

    # Create a dictionary of predictions with Product_Ids as keys
    product_ids = input_data['Product_Id'].tolist()  # Assuming 'Product_Id' is the unique identifier
    output_dict = dict(zip(product_ids, predicted_sales_rounded))

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    super_kart_predictor_api.run(debug=True)
