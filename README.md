# VendorView
VendorView is an application that allows street vendors to create a profile, list their products, and track their whereabouts. This Backend Application is built using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints. We also used SQLAlchemy as the ORM to interact with the database. PostgreSQL is used as the database to store the data and redis is used for storing temporary vendor location data.

## Table of Contents
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Running the Application](#running-the-application)
* [Project Structure](#project-structure)
* [Environment Variables](#environment-variables)
* [Postman](#postman)

## Prerequisites
Ensure you have the following installed on your local development environment:

* Python 3.7+
* pip
* virtualenv

## Installation
Clone the repository:
```bash 
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```


Create a virtual environment:
```bash
python -m venv venv
```


Activate the virtual environment:

    
On Windows:

      
      .\venv\Scripts\activate
      


    
On macOS/Linux:

      
      source venv/bin/activate
      


Install the dependencies:

    
    pip install -r requirements.txt
    


Running the Application
Start the FastAPI server:

    
    uvicorn main:app --reload
    


Access the application:
* Open your browser and navigate to http://127.0.0.1:8000
* Test our deployed app http://34.128.76.163:30001

API Documentation:    
* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc

## Project Structure
The project structure is as follows:

```
.
├── src
│   ├── __pycache__
│   ├── controllers
│   │   ├── __pycache__
│   │   ├── auth.py
│   │   ├── item.py
│   │   └── tracking.py
│   ├── models
│   │   ├── __pycache__
│   │   ├── auth.py
│   │   ├── item.py
│   │   └── tracking.py
│   ├── schemas
│   │   ├── __pycache__
│   │   ├── auth.py
│   │   ├── item.py
│   │   └── tracking.py
│   ├── services
│   │   ├── __pycache__
│   │   ├── auth.py
│   │   ├── item.py
│   │   └── tracking.py
│   ├── utils
│   │   ├── __pycache__
│   │   ├── auth.py
│   │   └── tracking.py
│   ├── database.py
│   ├── main.py
```

## Environment Variables
The following environment variables are used in the application:
* `DATABASE_URL` - The database URL
* `JWT_SECRET` - The secret key for encoding and decoding JWT tokens

Put all of those environment variables in a `.env` file in the root of the project.

## Postman
You can test the API endpoints using Postman. The collection is available [here](https://www.postman.com/gold-comet-697852/workspace/vendorview).