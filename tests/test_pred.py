import requests


def test_prediction():
    """
    Test prediction with valid input.
    """
    # Obtain valid token
    content = requests.post(
        "http://localhost:3000/login",
        data='''{
            "credentials": {
                "username": "admin",
                "password": "password"
            }
        }'''
    ).json()
    token = content.get("access_token")
    
    # Request the prediction endpoint
    content = requests.post(
        "http://localhost:3000/predict",
        headers={"Authorization": f"Bearer {token}"},
        data='''{
            "features": {
                "GRE Score": 340,
                "TOEFL Score": 120,
                "University Rating": 5,
                "SOP": 5,
                "LOR ": 5,
                "CGPA": 10,
                "Research": 1
            }
        }'''
    ).json()
    
    assert isinstance(content.get("acceptance"), float)
    assert content.get("acceptance") >= 0.0
    assert content.get("acceptance") <= 1.0


def test_invalid_input():
    """
    Test if invalid input throw an error.
    """
    # Obtain valid token
    content = requests.post(
        "http://localhost:3000/login",
        data='''{
            "credentials": {
                "username": "admin",
                "password": "password"
            }
        }'''
    ).json()
    token = content.get("access_token")
    
    # Request the prediction endpoint
    content = requests.post(
        "http://localhost:3000/predict",
        headers={"Authorization": f"Bearer {token}"},
        data='''{
            "features": {
                "GRE Score": 341,
                "TOEFL Score": 121,
                "University Rating": 6,
                "SOP": 6,
                "LOR ": 6,
                "CGPA": 11,
                "Research": 2
            }
        }'''
    ).json()
    
    assert content.get("error") == "7 validation error for Input"