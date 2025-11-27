from uuid import UUID
from app.repositories.favorites_repo_local import FavoritesRepoLocal
from app.models.favorites_models import FavoriteItem

class FavoritesService:
    def __init__(self, repo: FavoritesRepoLocal):
        self.repo = repo

    def add(self, user_id: UUID, product_id: UUID) -> FavoriteItem:
        return self.repo.add(user_id, product_id)

    def delete(self, favorite_id: UUID) -> bool:
        return self.repo.remove_by_id(favorite_id)

    def list_for_user(self, user_id: UUID):
        return self.repo.list_by_user(user_id)

    def check(self, user_id: UUID, product_id: UUID):
        f = self.repo.find(user_id, product_id)
        return {
            "user_id": user_id, "product_id": product_id,
            "in_favorites": f is not None, "favorite_id": (f.id if f else None)
        }
