import requests


def test_authentication():
    """
    Test the authentication to the predict
    endpoint with a valid token.
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
    
    # Check if we obtain a prediction
    assert content.get("acceptance") is not None


def test_invalid_token():
    """
    Test the authentication with an invalid token
    """
    # Invalid token
    token = "1111111111111111111"
    
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
    
    assert content.get("error") == "Authorization error"
    
    