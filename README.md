# NeighborFit: Neighborhood-Lifestyle Matching Application

[![Flask](https://img.shields.io/badge/Flask-3.1.1-blue)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

NeighborFit is a web application that matches users with neighborhoods based on their lifestyle preferences. The application uses a sophisticated algorithm to analyze population density, parks, restaurants, and other amenities to recommend the most suitable neighborhoods for users.

![NeighborFit Screenshot](https://via.placeholder.com/800x400?text=NeighborFit+Screenshot)

## 🌟 Features

- **Personalized Recommendations**: Adjust lifestyle preferences using intuitive sliders
- **Flexible Results**: Specify the number of neighborhood recommendations (3, 5, or 10)
- **Detailed Insights**: Receive ranked neighborhood matches with detailed scores
- **Comprehensive Profiles**: View neighborhood profiles with amenity data
- **Real-time Processing**: Get instant recommendations based on your preferences

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/neighborfit.git
   cd neighborfit
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application
   ```bash
   python main.py
   ```

4. Open your browser and navigate to `http://localhost:5000`

## 🔍 How It Works

NeighborFit uses a Euclidean distance-based algorithm in normalized feature space to match user preferences with neighborhood characteristics:

1. **Data Collection**: Processes California census tracts with demographic and amenity data
2. **Feature Normalization**: Uses min-max scaling to ensure equal feature weighting
3. **Similarity Calculation**: Computes Euclidean distance between user preferences and neighborhoods
4. **Recommendation Generation**: Returns the closest matching neighborhoods based on calculated distances

## 📊 Project Structure

```
neighborfit/
├── main.py                  # Application entry point
├── requirements.txt         # Project dependencies
├── src/                     # Source code
│   ├── routes/              # API routes
│   │   └── neighborhood.py  # Neighborhood recommendation endpoints
├── static/                  # Static files (HTML, CSS, JS)
│   ├── index.html           # Main application page
│   ├── script.js            # Frontend JavaScript
│   └── styles.css           # CSS styles
└── california_census_tracts_features.csv  # Dataset
```

## 🛠️ Technologies Used

- **Backend**: Flask, Python
- **Data Processing**: Pandas, NumPy, Scikit-learn
- **Frontend**: HTML, CSS, JavaScript
- **Data Sources**: U.S. Census Bureau, OpenStreetMap


## 🚀 Deploying on Render

1. **Push your code to GitHub**
   - Initialize a git repo if you haven't:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     git branch -M main
     git remote add origin https://github.com/yourusername/neighborfit.git
     git push -u origin main
     ```

2. **Create a new Web Service on [Render](https://render.com/)**
   - Connect your GitHub repo.
   - Render will auto-detect your `render.yaml` and `Procfile`.
   - Set any required environment variables (e.g., `CENSUS_API_KEY`).
   - Click "Deploy".

3. **Access your live app**
   - Once deployed, Render will provide a public URL for your app.

## 🖥️ Running Locally

1. Clone the repo and install dependencies:
   ```bash
   git clone https://github.com/yourusername/neighborfit.git
   cd neighborfit
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python main.py
   ```
3. Open [http://localhost:5000](http://localhost:5000) in your browser.

## 📈 Future Enhancements

- Expand to additional geographic regions
- Incorporate more lifestyle factors (safety, transportation, environment)
- Implement interactive mapping interfaces
- Add user accounts and personalization

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- U.S. Census Bureau for demographic data
- OpenStreetMap for amenity data
- Flask and Python communities for excellent documentation