from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
import logging
import traceback
from app.models.schemas import CarEntity, Query, CompetitorAnalysis
from app.core.market_intelligence import AutoMarketGraphRAG
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()
rag = AutoMarketGraphRAG(groq_api_key=settings.GROQ_API_KEY)

@router.post("/add_car")
async def add_car(car: CarEntity) -> Dict[str, Any]:
    try:
        logger.debug(f"Adding car: {car.dict()}")
        rag.add_car_entity(car)
        return {
            "status": "success",
            "message": f"Successfully added {car.name}"
        }
    except Exception as e:
        logger.error(f"Error adding car: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/query_market")
async def query_market(query: Query) -> Dict[str, Any]:
    try:
        logger.debug(f"Processing query: {query.dict()}")
        results = rag.query_market(query.query, query.top_k)
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        logger.error(f"Error in query_market: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/status")
async def get_status() -> Dict[str, Any]:
    """Get the current status of the market intelligence system"""
    # Count only car nodes, excluding competitor nodes that don't exist in the database
    car_nodes = set(node for node, attrs in rag.graph.nodes(data=True) 
                    if attrs.get('type') == 'car')
    
    return {
        "status": "online",
        "cars_in_database": len(car_nodes),
        "graph_nodes": len(car_nodes),  # Only count actual car nodes
        "graph_edges": len(rag.graph.edges)
    }

@router.get("/test_data")
async def test_data() -> Dict[str, Any]:
    """Test endpoint to check data structure"""
    sample_results = [{
        "car": "Test Car",
        "similarity": 0.95,
        "insight": "This is a test insight",
        "competitors": ["Competitor 1", "Competitor 2"],
        "data": {
            "manufacturer": "Test Manufacturer",
            "segment": "Test Segment",
            "features": ["Feature 1", "Feature 2"],
            "price_range": "$20,000-$30,000",
            "market_position": "Test Position"
        }
    }]
    
    return {
        "status": "success",
        "results": sample_results
    }

# In app/api/routes.py
@router.get("/analyze_segment/{segment}")
async def analyze_segment(segment: str) -> Dict[str, Any]:
    """Analyze a specific market segment"""
    try:
        analysis = rag.analyze_market_segment(segment)
        return {
            "status": "success",
            "analysis": analysis
        }
    except Exception as e:
        logger.error(f"Error analyzing segment: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )