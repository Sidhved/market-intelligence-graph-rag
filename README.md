# Automotive Market Intelligence System

A graph-based Retrieval-Augmented Generation (RAG) system that provides real-time automotive market insights and competitor analysis using Groq LLM.

## 🌐 Live Demo
[https://automotive-market-intelligence.onrender.com](https://automotive-market-intelligence.onrender.com)

## ✨ Features

### Market Intelligence
- Semantic search for automotive market insights
- Real-time competitor analysis
- Feature comparison across vehicles
- Price segment analysis
- Market positioning insights

### Technical Capabilities
- Graph-based knowledge representation
- Semantic similarity matching
- LLM-powered market analysis
- Real-time data processing
- RESTful API endpoints

## 🛠️ Technology Stack

### Backend
- FastAPI: Modern web framework
- Python: Core programming language
- Groq: LLM API integration
- NetworkX: Graph database management
- Sentence Transformers: Semantic embeddings

### Frontend
- HTML5/JavaScript: Core web technologies
- Tailwind CSS: Styling and components
- Font Awesome: Icons and visual elements

### Deployment
- Render: Cloud hosting platform
- GitHub: Version control and CI/CD

## 📚 API Documentation

### Endpoints

#### Add Car
```http
POST /api/add_car
```
```json
{
    "name": "Tesla Model 3",
    "manufacturer": "Tesla",
    "segment": "Electric Sedan",
    "features": ["Autopilot", "Over-the-air updates"],
    "price_range": "$40,000-$60,000",
    "competitors": ["BMW i4", "Polestar 2"],
    "market_position": "Premium Electric Vehicle"
}
```

#### Query Market
```http
POST /api/query_market
```
```json
{
    "query": "Compare charging infrastructure between Tesla and other EV manufacturers",
    "top_k": 3
}
```

#### System Status
```http
GET /api/status
```

## 🚀 Local Development

### Prerequisites
- Python 3.8+
- Groq API key

### Setup

1. Clone the repository
```bash
git clone https://github.com/Sidhved/market-intelligence-graph-rag.git
cd automotive-market-intelligence
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```bash
# Create .env file
echo "GROQ_API_KEY=your_groq_api_key" > .env
```

5. Run the application
```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000` in your browser.

## 📁 Project Structure
```
market-intelligence/
├── README.md
├── requirements.txt
├── .env
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── market_intelligence.py
│   └── api/
│       ├── __init__.py
│       └── routes.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── templates/
    └── index.html
```

## 💡 Usage Examples

### Adding a New Car
```python
car_data = {
    "name": "Tesla Model 3",
    "manufacturer": "Tesla",
    "segment": "Electric Sedan",
    "features": ["Autopilot", "Over-the-air updates"],
    "price_range": "$40,000-$60,000",
    "competitors": ["BMW i4", "Polestar 2"],
    "market_position": "Premium Electric Vehicle"
}

response = requests.post("http://localhost:8000/api/add_car", json=car_data)
```

### Querying Market Intelligence
```python
query_data = {
    "query": "Compare charging infrastructure between Tesla and other EV manufacturers",
    "top_k": 3
}

response = requests.post("http://localhost:8000/api/query_market", json=query_data)
```

## 🔒 Security

- Environment variables for sensitive data
- API input validation
- Error handling and logging
- CORS protection

## 🔜 Future Enhancements

- Data visualization features
- Advanced analytics dashboard
- Database integration
- Authentication system
- Export capabilities
- Real-time market updates

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Contact

Your Name - [sidhved.warik@gmail.com]

Project Link: [https://github.com/Sidhved/market-intelligence-graph-rag](https://github.com/Sidhved/market-intelligence-graph-rag)