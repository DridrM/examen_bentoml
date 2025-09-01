from datetime import datetime, timedelta

import numpy as np
import jwt
import bentoml
from bentoml.io import JSON
from starlette.requests import Request
from starlette.responses import JSONResponse

from params import (
    JWT_EXP_DELTA_MINUTES,
    JWT_ALGORITHM,
    JWT_SECRET
)


def create_jwt(username: str) -> str:
    """
    Create a JWT token for the given username.
    
    Args
    ----
    username: str
        Username for the service.
    
    Returns
    -------
    The token corresponding to the user.
    """
    # Define the payload
    payload = {
        "sub": username,
        "exp": datetime.now() + timedelta(
            minutes=JWT_EXP_DELTA_MINUTES
        ),
    }
    
    # Create the token by encoding the payload and the secret
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    return token


def verify_jwt(request: Request) -> None:
    """
    Extract and verify JWT from the Authorization header.
    
    Args
    ----
    request: Request
        API authentication JSON request.
    
    Returns
    -------
    None.
    """
    # Verify the request format
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        
        return None

    # Extract token
    token = auth_header.split(" ")[1]
    
    # Decode the token
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        return payload
    
    except jwt.ExpiredSignatureError:
        raise bentoml.exceptions.BadInput("Token has expired")
    
    except jwt.InvalidTokenError:
        raise bentoml.exceptions.BadInput("Invalid token")


@bentoml.service(resources={"cpu": "2"}, traffic={"timeout": 20})
class Prediction:
    """
    BentoML class for University acceptance prediction.
    """
    bento_model = bentoml.models.BentoModel("elasticnet-bento-exam:latest")
    
    def __init__(self):
        """
        Load the model from the model store.
        """
        self.model = bentoml.sklearn.load_model(self.bento_model)
    
    @bentoml.api(input=JSON(), output=JSON())
    async def login(self, credentials: dict) -> dict:
        """
        Grant access to authorized users.
        """
        # Extract username and password
        username = credentials.get("username")
        password = credentials.get("password")
        
        # Check username and password -> Very basic for the sake of the exercise
        if username == "admin" and password == "password":
            token = create_jwt(username)
            
            return {"access_token": token, "token_type": "bearer"}

        return JSONResponse({"error": "Invalid credentials"}, status_code=401)
    
    @bentoml.api(input=JSON(), output=JSON())
    async def predict(self, input_data: dict, request: Request) -> dict:
        """
        Predict given input data after veryfying
        the token and the features.
        """
        # Verify token
        claims = verify_jwt(request)
        if claims is None:
            return JSONResponse({"error": "Unauthorized"}, status_code=401)
        
        # Extract features
        features = input_data.get("features")
        if features is None:
            return JSONResponse({"error": "Missing 'features' field"}, status_code=400)

        # Convert to numpy array
        X = np.array(features).reshape(1, -1)

        # Predict
        prediction = self.model.predict(X)
        
        return {"prediction": float(prediction[0])}
        
        