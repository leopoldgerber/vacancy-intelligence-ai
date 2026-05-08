from app.api.schemas.analytics import AnalyticsRunResponse
from app.api.schemas.features import FeatureRunResponse
from app.api.schemas.ml_dataset import MlDatasetRunResponse
from pydantic import BaseModel


class Pipeline2FullRunResponse(BaseModel):
    """Pipeline 2 full run response schema."""

    status: str
    is_success: bool

    summary: AnalyticsRunResponse
    salary_features: FeatureRunResponse
    publication_activity_features: FeatureRunResponse
    text_features: FeatureRunResponse
    time_features: FeatureRunResponse
    categorical_features: FeatureRunResponse
    ml_dataset: MlDatasetRunResponse
