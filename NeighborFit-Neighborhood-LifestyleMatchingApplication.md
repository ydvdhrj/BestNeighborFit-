# NeighborFit - Neighborhood-Lifestyle Matching Application

A full-stack web application that helps users find neighborhoods that match their lifestyle preferences through data-driven analysis and algorithmic matching.

## 🌟 Live Demo

**Try it now:** https://5000-im33md339rwf8jpw7e0vl-b4e56a94.manusvm.computer

## 📋 Project Overview

NeighborFit solves the neighborhood-lifestyle matching problem by analyzing real-world data from 9,080 California census tracts and providing personalized neighborhood recommendations based on user preferences for:

- **Population Density** - Urban vs. rural lifestyle preferences
- **Parks & Green Spaces** - Access to recreational and natural areas  
- **Restaurants & Dining** - Dining and entertainment options

## 🚀 Features

- **Intuitive Interface** - Slider-based preference input with real-time feedback
- **Real-time Recommendations** - Instant neighborhood matching based on preferences
- **Detailed Results** - Match scores, feature breakdowns, and neighborhood profiles
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile devices
- **Data-Driven** - Built on real Census Bureau and OpenStreetMap data

## 🛠 Technology Stack

**Backend:**
- Python 3.11
- Flask web framework
- NumPy & pandas for data processing
- scikit-learn for algorithm implementation
- GeoPandas for spatial data handling

**Frontend:**
- HTML5, CSS3, JavaScript (vanilla)
- Responsive design with CSS Grid and Flexbox
- Modern UI with glass morphism effects

**Data Sources:**
- U.S. Census Bureau (demographics and boundaries)
- OpenStreetMap (amenities and points of interest)

## 📊 Algorithm

The matching algorithm uses:
- **Euclidean distance** calculation in normalized feature space
- **Min-max scaling** for equal feature weighting
- **K-nearest neighbors** approach for flexible recommendation counts
- **Real-time processing** with sub-second response times

## 🗂 Project Structure

```
neighborfit_api/
├── src/
│   ├── main.py                 # Flask application entry point
│   ├── routes/
│   │   └── neighborhood.py     # API endpoints for recommendations
│   └── static/
│       ├── index.html          # Frontend interface
│       ├── styles.css          # Styling and responsive design
│       └── script.js           # Frontend logic and API integration
├── california_census_tracts_features.csv  # Processed neighborhood data
├── scaler.joblib              # Saved feature scaler for consistency
└── requirements.txt           # Python dependencies
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.11+
- pip package manager

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd neighborfit_api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python src/main.py
   ```

5. **Access the application**
   Open http://localhost:5000 in your browser

## 📡 API Endpoints

### Get Neighborhood Recommendations
```http
POST /api/neighborhoods/recommend
Content-Type: application/json

{
  "population_density": 2000,
  "parks_per_sqkm": 5,
  "restaurants_per_sqkm": 10,
  "k": 5
}
```

### Get Feature Information
```http
GET /api/neighborhoods/features
```

### Get Neighborhood Details
```http
GET /api/neighborhoods/{geoid}
```

## 🧪 Testing

The project includes comprehensive testing covering:
- API endpoint functionality
- Algorithm accuracy across user profiles
- Edge case handling
- Performance validation

Run tests with:
```bash
python test_algorithm_validation.py
```

## 📈 Performance Metrics

- **Dataset:** 9,080 California census tracts
- **Response Time:** < 1 second for typical queries
- **Test Success Rate:** 100% across all scenarios
- **Algorithm Consistency:** Reproducible results for identical inputs

## 🔍 Data Processing Pipeline

1. **Census Data Extraction** - Demographics and tract boundaries from U.S. Census Bureau
2. **Amenity Data Collection** - Parks and restaurants from OpenStreetMap
3. **Feature Engineering** - Density calculations and normalization
4. **Quality Assurance** - Data validation and consistency checks
5. **Algorithm Preparation** - Feature scaling and serialization

## 📚 Documentation

- **[Technical Documentation](technical_documentation.md)** - Comprehensive technical analysis
- **[Problem Analysis Report](problem_analysis_report.md)** - Research methodology and findings
- **[Project Summary](project_summary.md)** - Executive summary and achievements
- **[Algorithm Analysis Report](algorithm_analysis_report.md)** - Performance analysis and visualizations

## 🎯 Key Achievements

- ✅ **Zero Budget** - Built entirely with free resources
- ✅ **Real Data** - Processes actual neighborhood data from authoritative sources
- ✅ **Functional Algorithm** - Working recommendation system with validated accuracy
- ✅ **Full-Stack Implementation** - Complete web application with API and frontend
- ✅ **Comprehensive Testing** - 100% test success rate across diverse scenarios
- ✅ **Scalable Architecture** - Designed for future enhancement and expansion

## 🚧 Known Limitations

- **Geographic Scope** - Currently limited to California census tracts
- **Feature Set** - Three primary features (population, parks, restaurants)
- **Static Data** - Snapshot-based data without real-time updates
- **Recommendation Diversity** - Limited by sparse amenity distribution in dataset

## 🔮 Future Enhancements

- **Geographic Expansion** - Support for additional states and regions
- **Enhanced Features** - Safety, transportation, environmental factors
- **User Accounts** - Saved preferences and recommendation history
- **Interactive Maps** - Visual neighborhood exploration
- **Real-time Data** - Live updates from data sources

## 🤝 Contributing

This project was developed as a demonstration of data-driven neighborhood matching. For questions or suggestions, please refer to the comprehensive documentation provided.

## 📄 License

This project is developed for educational and demonstration purposes. Data sources are used in accordance with their respective terms of service.

## 🙏 Acknowledgments

- **U.S. Census Bureau** - Demographic and geographic data
- **OpenStreetMap Contributors** - Amenity and point-of-interest data
- **Flask Community** - Web framework and ecosystem
- **scikit-learn Team** - Machine learning algorithms and tools

---



