from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import date


class CaloriesRequest(BaseModel):
    food_name: str


class CaloriesResponse(BaseModel):
    food_name: str
    calories: float
    serving_description: str
    protein: float
    fat: float
    carbohydrates: float


class HumanAPIAuthResponse(BaseModel):
    authorization_url: str
    state: str


class HumanAPITokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: str = "Bearer"


class StepsResponse(BaseModel):
    date: str
    steps: Optional[int] = None
    distance: Optional[float] = None
    calories: Optional[float] = None


class CaloriesBurnedResponse(BaseModel):
    date: str
    calories: float
    activities_count: Optional[int] = None


class ActivityResponse(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration: Optional[int] = None
    calories: Optional[float] = None
    distance: Optional[float] = None
    steps: Optional[int] = None


class ActivitiesResponse(BaseModel):
    date: str
    activities: List[ActivityResponse]
    total_calories: Optional[float] = None
