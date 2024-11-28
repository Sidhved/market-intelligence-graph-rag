from typing import List, Dict, Optional
from dataclasses import dataclass
import networkx as nx
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@dataclass
class CarEntity:
    name: str
    manufacturer: str
    segment: str
    features: List[str]
    price_range: str
    competitors: List[str]
    market_position: str

class AutoMarketGraphRAG:
    def __init__(self, groq_api_key: str):
        self.client = Groq(api_key=groq_api_key)
        self.graph = nx.Graph()
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.entity_embeddings = {}
        
    def add_car_entity(self, car: CarEntity):
        """Add a car entity to the knowledge graph"""
        logger.debug(f"Adding car: {car.name}")
        
        # Add main car node
        self.graph.add_node(car.name, 
                           type='car',
                           manufacturer=car.manufacturer,
                           segment=car.segment,
                           features=car.features,
                           price_range=car.price_range,
                           market_position=car.market_position)
        
        # Add competitor relationships
        for competitor in car.competitors:
            self.graph.add_edge(car.name, competitor, relationship='competes_with')
            
        # Create and store embedding
        car_text = f"{car.name} {car.manufacturer} {car.segment} {' '.join(car.features)} {car.price_range} {car.market_position}"
        self.entity_embeddings[car.name] = self.encoder.encode(car_text)
        
        logger.debug(f"Successfully added car: {car.name}")
        
    # Add this method to AutoMarketGraphRAG class
    def analyze_market_segment(self, segment: str) -> Dict:
        """Analyze all vehicles in a specific segment"""
        segment_cars = [
            node for node, attrs in self.graph.nodes(data=True)
            if attrs.get('segment') == segment
        ]
        
        features_freq = {}
        price_ranges = []
        competitors_graph = nx.Graph()
        
        for car in segment_cars:
            car_data = self.graph.nodes[car]
            
            # Analyze features
            for feature in car_data['features']:
                features_freq[feature] = features_freq.get(feature, 0) + 1
            
            # Collect price ranges
            price_ranges.append(car_data['price_range'])
            
            # Build competitor relationships
            competitors = list(self.graph.neighbors(car))
            for comp in competitors:
                if comp in segment_cars:
                    competitors_graph.add_edge(car, comp)
        
        return {
            "segment": segment,
            "vehicle_count": len(segment_cars),
            "common_features": sorted(features_freq.items(), key=lambda x: x[1], reverse=True),
            "price_ranges": price_ranges,
            "most_connected": max(competitors_graph.degree(), key=lambda x: x[1])[0] if competitors_graph.nodes else None
        }
    
    def query_market(self, query: str, top_k: int = 3) -> List[Dict]:
        """Query the market intelligence system"""
        logger.debug(f"Processing query: {query} with top_k={top_k}")
        
        if not self.entity_embeddings:
            logger.warning("No cars in database")
            return [{
                "car": "No data",
                "similarity": 0.0,
                "insight": "No cars in database. Please add some cars first.",
                "competitors": [],
                "data": None
            }]

        try:
            # Encode query
            query_embedding = self.encoder.encode(query)
            
            # Find most relevant cars based on semantic similarity
            similarities = {}
            for car_name, embedding in self.entity_embeddings.items():
                similarity = float(cosine_similarity([query_embedding], [embedding])[0][0])
                similarities[car_name] = similarity
                
            top_cars = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:top_k]
            
            results = []
            for car_name, similarity in top_cars:
                car_data = self.graph.nodes[car_name]
                
                # Get competitor information
                competitors = list(self.graph.neighbors(car_name))
                
                context = f"""
                Provide a brief, focused analysis of {car_name} regarding this specific query: {query}

                Key Context:
                - Manufacturer: {car_data['manufacturer']}
                - Segment: {car_data['segment']}
                - Key Features: {', '.join(car_data['features'])}
                - Market Position: {car_data['market_position']}
                - Main Competitors: {', '.join(competitors[:3])}
                """

                


                
                try:
                    # Update the Groq API call:
                    response = self.client.chat.completions.create(
                        model="mixtral-8x7b-32768",
                        messages=[
                            {"role": "system", "content": "You are an automotive market intelligence expert. Provide concise, specific insights in 2-3 sentences."},
                            {"role": "user", "content": context}
                        ],
                        max_tokens=150,  # Reduced for more focused responses
                        temperature=0.7
                    )
                    
                    insight = response.choices[0].message.content
                except Exception as e:
                    logger.error(f"Error generating insight: {str(e)}")
                    insight = f"Error generating insight: {str(e)}"
                
                results.append({
                    "car": car_name,
                    "similarity": similarity,
                    "data": {
                        "manufacturer": car_data['manufacturer'],
                        "segment": car_data['segment'],
                        "features": car_data['features'],
                        "price_range": car_data['price_range'],
                        "market_position": car_data['market_position']
                    },
                    "competitors": competitors,
                    "insight": insight
                })
            
            logger.debug(f"Query results: {results}")
            return results
            
        except Exception as e:
            logger.error(f"Error in query_market: {str(e)}")
            raise