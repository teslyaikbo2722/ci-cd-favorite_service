from __future__ import annotations

from typing import List
from uuid import UUID, uuid4
from datetime import datetime
from app.models.favorites_models import FavoriteItem

class FavoritesRepoLocal:
    def __init__(self) -> None:
        self._storage: list[FavoriteItem] = []

    def add(self, user_id: UUID, product_id: UUID) -> FavoriteItem:
        item = FavoriteItem(id=uuid4(), user_id=user_id, product_id=product_id, created_at=datetime.utcnow())
        self._storage.append(item)
        return item

    def remove_by_id(self, favorite_id: UUID) -> bool:
        before = len(self._storage)
        self._storage = [f for f in self._storage if f.id != favorite_id]
        return len(self._storage) < before

    def list_by_user(self, user_id: UUID) -> List[FavoriteItem]:
        return [f for f in self._storage if f.user_id == user_id]

    def find(self, user_id: UUID, product_id: UUID) -> FavoriteItem | None:
        for f in self._storage:
            if f.user_id == user_id and f.product_id == product_id:
                return f
        return None
