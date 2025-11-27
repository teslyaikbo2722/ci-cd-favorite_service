from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class FavoriteCreate(BaseModel):
    user_id: UUID
    product_id: UUID

class FavoriteItem(BaseModel):
    id: UUID
    user_id: UUID
    product_id: UUID
    created_at: datetime

class FavoriteCheckResponse(BaseModel):
    user_id: UUID
    product_id: UUID
    in_favorites: bool
    favorite_id: UUID | None = None
