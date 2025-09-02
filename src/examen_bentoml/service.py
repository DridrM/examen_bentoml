from datetime import datetime, timedelta

import numpy as np
import jwt
import bentoml


# Define params
# =============

# Duration of the token
JWT_EXP_DELTA_MINUTES = 120

# Encoding algorithm
JWT_ALGORITHM = "HS256"

# Encoding secret
JWT_SECRET = "Pu3Y2MLm7tKnZFprxKr9VQyj9qLkidnexMETw8gWQdk="


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


def verify_jwt(context: bentoml.Context) -> None:
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
    auth_header = context.request.headers.get("Authorization")
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
    
    @bentoml.api
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

        return {"error": "Invalid credentials"}
    
    @bentoml.api
    async def predict(self, features: np.ndarray, context: bentoml.Context) -> np.ndarray:
        """
        Predict given input data after veryfying
        the token and the features.
        """
        # Verify token
        claims = verify_jwt(context)
        if claims is None:
            return {"error": "Unauthorized"}

        # Predict
        return self.model.predict(features)
