# Anime Recommendation Engine

## 🎯 Problem Statement

### Current Challenges
1. **Cold Start Problem**: 
   - 62% of new users abandon platforms when they don't receive personalized recommendations (Anime Industry Report 2023)
   - Existing content-based filters fail to capture nuanced user preferences

2. **Scalability Issues**:
   - Traditional collaborative filtering methods show 300% slower inference times at 1M+ user scale
   - Memory constraints with matrix factorization approaches

3. **Dynamic Preference Tracking**:
   - 78% of anime viewers change genre preferences seasonally
   - Static recommendation models become stale within 3 months

4. **Business Impact**:
   - Platforms with poor rec systems show 45% lower viewer retention
   - Estimated $220M annual revenue loss across top anime platforms

## 🏗️ Solution Architecture

### Neural Recommendation System
**Two-Tower Architecture**:
- **User Tower**: 
  - Processes user metadata + behavioral data 
  - Transformer-based sequence modeling for temporal patterns

- **Anime Tower**:
  - Processes content features + community metrics
  - Embedding for synopsis analysis

A Two-Tower Neural Network-based recommendation system that suggests anime based on user interactions. Built with TensorFlow, FastAPI, and deployed on GCP with Kubernetes.

## Features

- Personalized anime recommendations using collaborative filtering
- Two-Tower neural network architecture for scalable recommendations
- Real-time inference via FastAPI endpoint
- Full MLOps pipeline: data ingestion → training → deployment → monitoring
- DVC 
- Experiment tracking with Comet.ml
- CI/CD with Jenkins

## Technologies Used

**Core ML**
- TensorFlow (Two-Tower Model)
- Pandas/Numpy for data processing
- Scikit-learn for metrics

**Infrastructure**
- Google Cloud Platform (GCP)
- Google Kubernetes Engine (GKE)
- Docker for containerization
- Jenkins for CI/CD

**Tracking & Serving**
- Comet.ml for experiment tracking
- FastAPI for model serving
- Uvicorn as ASGI server

## Two-Tower Model Architecture

The recommendation system uses a dual neural network architecture:

1. **User Tower**:
   - Processes user interaction history
   - Learns dense user embeddings (128-dim)
   - Includes features like:
     - User's watched anime history
     - Rating patterns
     - Interaction frequency

2. **Item (Anime) Tower**:
   - Processes anime features
   - Generates anime embeddings (128-dim)
   - Includes features like:
     - Genre embeddings
     - Rating
     - Episode Watched
     - Episode Watching

The model learns by maximizing the cosine similarity between user and anime embeddings for positive interactions while minimizing it for negative samples.


## Getting Started

### Prerequisites

- Python 3.10.16
- Docker
- GCP account (for deployment)
- Comet.ml account (for tracking)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/HakimOwais/Recommendation-Engine.git
   cd Recommendation-Engine

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
3.  Set up Comet ml tracking API KEY in .env file:

    API_KEY="your_api_key"

### Training the Model

Prepare your dataset in data/processed/
* Run training:
    ```bash
    python pipeline/training_pipeline.py 

Training will start and the progress will be logged to Comet.ml with:

* Loss curves
* Embedding projections
* Recommendation quality metrics

### Running Locally

* Start the FastAPI server:

    ```bash
    uvicorn application.api:app --reload

The API will be available at http://localhost:8000/docs

* API Endpoint

    POST /recommend - Get anime recommendations for a user
    {
    "user_id": "11880",
    } 

### Deployment

The project includes CI/CD through Jenkins:

Build Docker image:

    ```bash
        docker build -t anime-recommendation:latest .

* Deploy to GKE (For further details navigate the Jenkinsfile and deployment.yaml )

## Future Improvements
- Enhance model performance with additional features
- Integrate a front-end dashboard for better visualization

---

## License
This project is open-source and available under the MIT License.
