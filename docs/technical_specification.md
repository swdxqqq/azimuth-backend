# Nomad Compass — Technical Specification

## Project Overview

**Nomad Compass** is a data-driven platform that helps digital nomads, students, and remote workers choose the best countries to live in based on their personal priorities. The system combines historical Numbeo data with real-time external APIs to provide comprehensive analytics, machine learning insights, and personalized recommendations.

The platform consists of:
- **Python Backend**: FastAPI REST API serving analytics and ML models
- **PostgreSQL Database**: Centralized storage for historical and real-time data
- **Android Mobile App**: Kotlin-based client consuming the backend API

---

## Technology Stack

### Backend
- **Python 3.10+**: Core language for data processing and ML
- **FastAPI**: Modern async web framework for REST API
- **PostgreSQL**: Relational database for structured data storage
- **psycopg2**: Python driver for direct PostgreSQL interaction
- **pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **scikit-learn**: Machine learning (clustering, recommendations, anomaly detection)
- **Prophet**: Time-series forecasting
- **Docker**: Containerization for deployment
- **Apache Airflow**: ETL orchestration (post-MVP)
- **PySpark**: Distributed data processing (post-MVP)

### Mobile
- **Kotlin**: Primary language for Android development
- **Jetpack Compose**: Modern UI toolkit
- **Retrofit**: HTTP client for API consumption
- **Room**: Local database for offline caching
- **MPAndroidChart**: Data visualization
- **Google Maps SDK**: Geospatial features

### External APIs
- **World Bank API**: Economic indicators (GDP, inflation, unemployment)
- **Open Exchange Rates**: Currency conversion rates
- **NewsAPI**: Country-specific news headlines
- **OpenWeatherMap**: Weather data and forecasts
- **REST Countries**: Population, languages, visa-free access

---

## Data Architecture

### Base Layer: Numbeo Historical Data (2014-2026)
The foundation consists of 54 countries with complete data across 12 years (648 rows total). Metrics include:
- Cost of Living Index
- Rent Index
- Groceries Index
- Restaurant Price Index
- Local Purchasing Power Index
- Crime Index & Safety Index
- Health Care Index
- Pollution Index
- Traffic Index
- Climate Index
- Quality of Life Index
- Property Price to Income Ratio

### Dynamic Layers: External APIs
Real-time data integrated from multiple sources to enrich the static Numbeo base:
- **Economic data**: GDP growth, inflation rates, unemployment, currency exchange rates
- **Safety data**: News headlines, global events, travel advisories
- **Weather data**: Current temperature, forecasts, air quality index
- **Social metrics**: Population statistics, internet speed, visa-free travel access

### Database Structure
The PostgreSQL database will contain tables for:
- Numbeo country metrics by year
- Economic indicators from external APIs
- News and safety data
- Weather and environmental data
- Social and demographic metrics
- ML clustering results
- User recommendation history

---

## Machine Learning Functionality

### 1. Clustering
Group countries into 4-6 meaningful clusters based on similarity across all metrics. Algorithms to explore: K-Means, DBSCAN, Hierarchical Clustering. Clusters will have interpretable labels like "Affordable & Safe", "Expensive & High Quality", "Developing Markets", etc.

### 2. Recommendation Engine
Content-based filtering system where users specify priority weights for different metrics (safety, cost, healthcare, etc.). The system computes weighted scores and returns top-10 countries matching user preferences.

### 3. Time-Series Forecasting
Predict future values (2027-2028) for key metrics like Cost of Living Index and Crime Index using statistical models (ARIMA, Prophet) or deep learning (LSTM).

### 4. Anomaly Detection
Identify countries with unusual year-over-year changes in metrics using Isolation Forest algorithm. Useful for flagging sudden economic shifts or safety concerns.

### 5. Sentiment Analysis (Post-MVP)
Analyze news headlines to compute sentiment scores per country using NLP techniques (VADER or Transformer models).

### 6. Similarity Search (Post-MVP)
Find countries similar to a target country using cosine similarity on normalized feature vectors.

### 7. Multi-Objective Optimization (Post-MVP)
Compute Pareto-optimal countries that represent best trade-offs between competing objectives (e.g., minimizing cost while maximizing safety).

---

## API Specification

### MVP Endpoints

**GET /api/countries**
List all countries with their latest metrics (2026 data).

**GET /api/countries/{name}**
Retrieve detailed information for a specific country across all available years.

**GET /api/clusters**
Return clustering results with cluster assignments and labels for all countries.

**POST /api/recommend**
Accept user priority weights as JSON payload and return top-10 recommended countries ranked by weighted score.

### Post-MVP Endpoints

**GET /api/anomalies**
Return countries with anomalous year-over-year metric changes.

**GET /api/forecast/{country}**
Provide forecasted values for key metrics for the specified country.

**GET /api/sentiment/{country}**
Return aggregated news sentiment score for the specified country.

**GET /api/similar/{country}**
Return countries most similar to the specified target country.

---

## Development Phases

### Phase 1: Data Foundation (2-3 days)
- Set up PostgreSQL database with appropriate schema
- Add 2026 Numbeo data to the existing dataset
- Implement data loading pipeline to transfer CSV data into PostgreSQL
- Validate data integrity and create indexes for performance

### Phase 2: ML Clustering (2-3 days)
- Normalize data using Min-Max or Z-score normalization
- Implement K-Means clustering algorithm
- Determine optimal number of clusters using elbow method or silhouette score
- Assign interpretable labels to clusters
- Store cluster assignments in database

### Phase 3: ML Recommendations (1-2 days)
- Design user preference input schema (metric weights)
- Implement weighted scoring algorithm
- Create ranking function to return top-N countries
- Test with various user profiles

### Phase 4: FastAPI Core (2-3 days)
- Set up FastAPI project structure
- Implement the 4 MVP endpoints
- Configure database connection pooling
- Add input validation and error handling
- Generate automatic API documentation with Swagger

### Phase 5: External API Integration (2-3 days)
- Integrate World Bank API for economic data
- Integrate NewsAPI for country-specific headlines
- Implement caching strategy to reduce API calls
- Design data refresh schedule for real-time updates

### Phase 6: Testing & Documentation (1-2 days)
- Write unit tests for ML models and API endpoints
- Create integration tests for database operations
- Document API usage with examples
- Write deployment instructions

**Total MVP Duration:** 2-3 weeks

### Post-MVP Extensions
- Advanced ML models (forecasting, sentiment analysis, similarity search)
- Real-time data pipelines (weather, currency, daily news updates)
- ETL orchestration with Apache Airflow
- Android mobile app development
- Authentication and rate limiting for API
- CORS configuration for web clients
- Containerization with Docker
- CI/CD pipeline setup

---

## Android Application Integration

The Android app will consume the FastAPI backend and provide:
- Country browsing and filtering interface
- Interactive maps showing country locations
- Personalized recommendation wizard
- Offline caching of favorite countries
- Push notifications for anomaly alerts
- Charts and visualizations of trends
- News feed per country

Hardware permissions will be utilized for:
- **GPS**: Detect user's current location and suggest nearby countries
- **Camera**: Potential feature for scanning travel documents or QR codes (optional)
- **Sensors**: Accelerometer for gesture-based navigation (optional)

---

## Success Metrics

- **Data Coverage**: 54 countries with complete historical data (2014-2026)
- **API Response Time**: < 200ms for country listing, < 500ms for recommendations
- **ML Model Accuracy**: Clustering silhouette score > 0.5, recommendation relevance validated by user feedback
- **Database Performance**: Query execution time < 100ms with proper indexing
- **External API Reliability**: 99% uptime with fallback caching mechanisms

---

## Future Considerations

- Expand country coverage as Numbeo data becomes available
- Add city-level analysis if data volume permits
- Implement user authentication and personalized profiles
- Create admin dashboard for monitoring data freshness
- Explore GraphQL as alternative to REST API
- Consider serverless deployment options (AWS Lambda, Google Cloud Functions)

---

**Document Version:** 1.0  
**Last Updated:** October 12, 2026