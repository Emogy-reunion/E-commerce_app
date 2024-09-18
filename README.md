# East Monarch - e-Commerce Website

## Introduction

**East Monarch** is a feature-rich eCommerce website designed for a seamless online shopping experience. This web application allows users to browse a wide range of sneakers, add them to their cart, and place orders. It includes functionalities for user registration, cart management, and payment processing, ensuring a smooth and secure shopping experience.

## Features

- **User Authentication and email verification**: Register, log in, and manage user accounts.
- **Product Catalog**: Browse sneakers by gender, brand, and other categories.
- **Shopping Cart**: Add items to the cart, update quantities, and view the cart summary.
- **Order Processing**: Place orders and manage checkout.
- **Payment Integration**: Secure payment via M-Pesa STK Push.

## Setup and Installation

### Prerequisites

* Before setting up the project, ensure you have the following installed on your machine:

- [Python 3.12+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)

### Clone the Repository

1. **Clone the repository:**

   ```sh
    https://github.com/Emogy-reunion/E-commerce_app.git
    cd E-commerce_app
    ```


### **Create and Activate Virtual Environment**
1. **Create a virtual environment:**
    ```sh
    python -m venv myenv
    ```

2. **Activate virtual environment**
    ```sh
    source myenv/bin/activate
    ```

### Install the required dependencies:
    ```sh
    pip freeze > requirements.txt
    ```

### Create the database:
* Make sure to configure your database settings in config.py.

### Run the Application
    ```sh
    flask run
    ```

* The application will be available at http://127.0.0.1:5000/.

### Configuration

* The application settings and configurations are stored in config.py. You can modify the database URI, secret keys, and other settings as needed.

### Usage
* Access the Application: Open your web browser and go to http://127.0.0.1:5000/.
* User Registration: Register a new account to start using the application.
* Browse Sneakers: Explore the sneaker catalog and add items to your cart.
* Checkout: Proceed to checkout and complete your purchase.

## Contributing

* If you want to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes and push them to your fork.
4. Submit a pull request describing your changes.
