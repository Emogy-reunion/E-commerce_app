import os
import requests
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime

def get_access_token():
    consumer_key = os.environ.get('MPESA_CONSUMER_KEY')
    consumer_secret = os.environ.get('MPESA_CONSUMER_SECRET')
    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    auth_response = requests.get(auth_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    
    if auth_response.status_code == 200:
        return auth_response.json().get('access_token')
    else:
        raise Exception("Failed to get access token: " + auth_response.text)

def generate_password():
    shortcode = '174379'
    passkey = os.environ.get('MPESA_PASSKEY')
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = f"{shortcode}{passkey}{timestamp}"
    encoded_string = base64.b64encode(data_to_encode.encode()).decode('utf-8')
    return encoded_string, timestamp

def initiate_stk_push(amount, phone_number):
    access_token = get_access_token()
    print(access_token)
    password, timestamp = generate_password()
    shortcode = '174379'
    stk_push_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
    }

    request_body = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": '254708374149',
        "PartyB": shortcode,
        "PhoneNumber": '254708374149',
        "CallBackURL": "https://a33f-102-1-66-214.ngrok-free.app/callback",
        "AccountReference": "Test123",
        "TransactionDesc": "Payment for testing"
    }

    response = requests.post(stk_push_url, json=request_body, headers=headers)
    return response.json()
