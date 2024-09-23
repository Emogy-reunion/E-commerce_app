'''
contains routes that handle payments using daraja api
'''
import requests
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime

def get_access_token():
    '''
    retrieves the OAuth access token by making a request to the safaricom api
    it validate that the application is authenticated to make requests
    '''

    consumer_key = 'YOUR_CONSUMER_KEY'
    consumer_secret = 'YOUR_CONSUMER_SECRET'

    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    auth_response = requests.get(auth_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    if auth_response.status_code == 200:
        return auth_response.json().get('access_token')
    else:
        raise Exception("Failed to get access token: " + auth_response.text)

def generate_password():
    '''
    creates a base64 encoded string from the passkey, shortcode and timestamp
    The password ensures that only your application can initiate the STK Push transaction for the specified shortcode.
    '''
    
    # test credentials
    shortcode = '174379'
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2c2cb7308f7a0c1db7d0b529d77b7e74'

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  # Current timestamp
    data_to_encode = f"{shortcode}{passkey}{timestamp}"  # Shortcode + Passkey + Timestamp
    encoded_string = base64.b64encode(data_to_encode.encode()).decode('utf-8')
    return encoded_string, timestamp

def initiate_stk_push(amount, phone_number):
    '''
    initiates an stk push to the customer
    '''
    access_token = get_access_token()
    password, timestamp = generate_password(shortcode, passkey)
    shortcode = '174379'
    callback_url = ''
    stk_push_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}

    request_body = {
        "BusinessShortCode": shortcode,  # Shortcode (test: 174379)
        "Password": password,  # Generated password
        "Timestamp": timestamp,  # Generated timestamp
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,  # Payment amount (1 for test)
        "PartyA": phone_number,  # Customer phone number (test: 254708374149)
        "PartyB": shortcode,  # Business shortcode (test: 174379)
        "PhoneNumber": phone_number,  # Customer phone number (test: 254708374149)
        "CallBackURL": callback_url,  # Your callback URL for receiving response
        "AccountReference": "Test123",  # Account reference
        "TransactionDesc": "Payment for testing"  # Transaction description
    }

    response = requests.post(stk_push_url, json=request_body, headers=headers)
    return response.json()
