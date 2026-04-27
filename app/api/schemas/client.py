from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ClientCreateRequest(BaseModel):
    """Store client create request payload.
    Args:
        """
    client_id: int
    name: str
    is_active: bool = True


class ClientResponse(BaseModel):
    """Store client response payload.
    Args:
        """
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    is_active: bool
    created_at: datetime
