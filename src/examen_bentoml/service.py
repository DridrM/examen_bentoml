from datetime import datetime, timedelta

import pandas as pd
import jwt
import bentoml
from bentoml.exceptions import BadInput
from pydantic import BaseModel, Field
from http import HTTPStatus


# Define params
# =============

# Duration of the token
JWT_EXP_DELTA_MINUTES = 120

# Encoding algorithm
JWT_ALGORITHM = "HS256"

# Encoding secret
JWT_SECRET = "Pu3Y2MLm7tKnZFprxKr9VQyj9qLkidnexMETw8gWQdk="


class InvalidCredentialsException(BadInput):
    """
    Exception raised when invalid credentials
    are specified with error code 401.
    """
    error_code = HTTPStatus.UNAUTHORIZED


class Features(BaseModel):
    """
    Give more information about the 
    features inside the API doc.
    """
    gre_score: float = Field(alias="GRE Score", ge=0, le=340, description="Score at the GRE test")
    toefl_score: float = Field(alias="TOEFL Score", ge=0, le=120, description="Score at the TOEFL test")
    university_rating: float = Field(alias="University Rating", ge=0, le=5, description="University rating")
    sop: float = Field(alias="SOP", ge=0, le=5, description="Statement of Purpose")
    lor: float = Field(alias="LOR ", ge=0, le=5, description="Letter of recommendation")
    cgpa: float = Field(alias="CGPA", ge=0, le=10, description="Cumulative Grade Point Average")
    research: int = Field(alias="Research", ge=0, le=1, description="Experience in research")


class Credentials(BaseModel):
    """
    Class representing the credentials.
    Give more info inside the API doc.
    """
    username: str = Field(description="Name of the user")
    password: str = Field(description="User's password")


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
    print(context.request.headers)
    auth_header = context.request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        
        return None

    # Extract token
    token = auth_header.split(" ")[1]
    
    # Decode the token
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        return payload
    
    except jwt.ExpiredSignatureError:
        raise InvalidCredentialsException("Token has expired")
    
    except jwt.InvalidTokenError:
        raise InvalidCredentialsException("Invalid token")


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
    def login(self, credentials: Credentials) -> dict:
        """
        Grant access to authorized users.
        """
        # Extract username and password
        username = credentials.username
        password = credentials.password
        
        # Check username and password -> Very basic for the sake of the exercise
        if username == "admin" and password == "password":
            token = create_jwt(username)
            
            return {"access_token": token, "token_type": "Bearer"}

        else:
            raise InvalidCredentialsException("Invalid credentials")
    
    @bentoml.api
    def predict(self, features: Features, context: bentoml.Context) -> dict[str, float]:
        """
        Predict given input data after veryfying
        the token and the features.
        """
        # Verify token
        claims = verify_jwt(context)
        if not claims:
            raise InvalidCredentialsException("Unauthorized")

        # Predict
        X = pd.DataFrame.from_dict(
            {col: [value] for col, value in features.model_dump(by_alias=True).items()}
        )
        
        return {"acceptance": float(self.model.predict(X))}