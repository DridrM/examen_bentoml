import requests


def test_login():
    """
    Test API authentication.
    """
    content = requests.post(
        "http://localhost:3000/login",
        data='''{
            "credentials": {
                "username": "admin",
                "password": "password"
            }
        }'''
    ).json()
    
    # Verify access token is present
    assert content.get("access_token") is not None
    
    # Verify if the token type is 'Bearer'
    assert content.get("token_type") == "Bearer"


def test_invalid_credentials():
    """
    Test login with invalid credentials.
    """
    content = requests.post(
        "http://localhost:3000/login",
        data='''{
            "credentials": {
                "username": "hello",
                "password": "world"
            }
        }'''
    ).json()
    
    assert content.get("error") == "Authorization error"