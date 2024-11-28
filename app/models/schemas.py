from pydantic import BaseModel
from typing import List

class CarEntity(BaseModel):
    name: str
    manufacturer: str
    segment: str
    features: List[str]
    price_range: str
    competitors: List[str]
    market_position: str

class Query(BaseModel):
    query: str
    top_k: int = 3

class CompetitorAnalysis(BaseModel):
    car_name: str