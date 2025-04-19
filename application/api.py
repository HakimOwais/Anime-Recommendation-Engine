from fastapi import FastAPI
import uvicorn
from pipeline.prediction_pipeline import hybrid_recommendation
from application.schema import UserRequest

app = FastAPI()

@app.get("/")
def index():
    return "Service is healthy and running"

@app.post("/recommend")
async def get_recommendations(data: UserRequest):
    try:
        recommendations = hybrid_recommendation(data.userID)
        return {"userID": data.userID, "recommendations": recommendations}
    except Exception as e:
        return {"error": "An error occurred", "details": str(e)}


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)