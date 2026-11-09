from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.recommend import RecommendationRequest, RecommendationResponse, RecommendationItem
from app.services.recsys_adapter import RecSysAdapter

router = APIRouter(prefix="/recommend", tags=["Recommendations"])


@router.post("", response_model=RecommendationResponse)
def get_recommendations(request: RecommendationRequest, db: Session = Depends(get_db)):
    adapter = RecSysAdapter(db)

    temp_pref = None
    if request.temperature_preference:
        temp_pref = {
            "enabled": request.temperature_preference.enabled,
            "target_temp": request.temperature_preference.target
        }

    preferences = [p.dict() for p in request.preferences]

    results = adapter.recommend(preferences, temp_pref, request.top_n)

    recommendations = []
    for _, row in results.iterrows():
        recommendations.append(RecommendationItem(
            country_id=int(row["Country"]),
            name=row["Country"],
            score=float(row["Final_Score"]),
            breakdown={},
            confidence=float(row.get("Confidence", 1.0))
        ))

    return RecommendationResponse(
        recommendations=recommendations,
        algorithm="geometric_mean",
        parameters={"gamma": 1.3, "epsilon": 0.02, "lambda": 0.08}
    )
