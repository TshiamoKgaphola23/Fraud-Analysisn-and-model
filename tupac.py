import streamlit as st
import pickle
import pandas as pd
from datetime import datetime

# Title of the web app
st.title('Fraud Detection Test')

# Background
background_image_url = "https://www.frost.com/wp-content/uploads/2022/04/Enterprise-Security-Concerns-Drive-Global-Demand-for-Fraud-Detection-Prevention-Solutions.jpg"
background_css = """
<style>
    .stApp {{
        background: url("{image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
</style>
""".format(image=background_image_url)
st.markdown(background_css, unsafe_allow_html=True)

# Load the serialized model
with open("Fraud_model.pkl", "rb") as pkl_file:
    model = pickle.load(pkl_file)

# Load training data (assuming it's CSV)
train = pd.read_csv("training.csv")

# Data cleaning
for col in ['TransactionId', 'AccountId', 'BatchId', 'SubscriptionId', 'CustomerId', 'ProviderId', 'ChannelId', 'ProductId']:
    train[col] = train[col].str.replace(f'{col}_', '')

# Input fields for selection
customer_id = st.selectbox('Customer ID', train['CustomerId'].unique())

# Filter based on Customer ID
dum = train[train['CustomerId'] == customer_id]
account_id = st.selectbox('Account ID', dum['AccountId'].unique())

# Filter based on Account ID
dum2 = dum[dum['AccountId'] == account_id]
product_category = st.selectbox('Product Category', dum2['ProductCategory'].unique())

# Filter based on Product Category
dum3 = dum2[dum2['ProductCategory'] == product_category]
product_id = st.selectbox('Product ID', dum3['ProductId'].unique())
channel_id = st.selectbox('Channel ID', dum3['ChannelId'].unique())
amount = st.number_input('Amount', min_value=-1000000000000.0, step=0.01)
pricing_strategy = st.selectbox('Pricing Strategy', dum3['PricingStrategy'].unique())

# Date and time input
transaction_date = st.date_input('Transaction Date')
year = transaction_date.year
month = transaction_date.month
day = transaction_date.day

transaction_time = st.time_input('Transaction Time')
hour = transaction_time.hour
minute = transaction_time.minute

# Mapping for ProductCategory
product_category_mapping = {
    'airtime': 0,
    'financial_services': 1,
    'tv': 2,
    'utility_bill': 3,
    'data_bundles': 4,
    'movies': 5,
    'ticket': 6,
    'retail': 7,
    'transport': 8
}

# Convert ProductCategory to its mapped value
product_category_encoded = product_category_mapping.get(product_category, -1)

# Button to submit the form
if st.button('Detect Fraud'):
    # Collect user inputs
    user_inputs = {
        'AccountId': int(account_id),
        'CustomerId': int(customer_id),
        'ProductId': int(product_id),
        'ProductCategory': product_category_encoded,
        'ChannelId': int(channel_id),
        'Amount': amount,
        'PricingStrategy': int(pricing_strategy),
        'year': year,
        'month': month,
        'day': day,
        'hour': hour,
        'minute': minute
    }

    # Convert user inputs to DataFrame
    user_inputs_df = pd.DataFrame([user_inputs])

    # Define the columns used in the model
    model_columns = ['AccountId', 'CustomerId', 'ProductId', 'ProductCategory', 'ChannelId',
                    'Amount', 'PricingStrategy', 'year', 'month', 'day', 'hour', 'minute']

    # Align columns in the correct order
    user_inputs_df = user_inputs_df[model_columns]

    # Perform fraud detection using the loaded model
    prediction = model.predict(user_inputs_df)

    # Display prediction result
    if prediction[0] == 1:
        st.error('Fraud Detected!')
    else:
        st.success('No Fraud Detected.')

    st.balloons()
