from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Body
from app.repositories.favorites_repo_local import FavoritesRepoLocal
from app.services.favorites_service import FavoritesService
from app.models.favorites_models import FavoriteCreate, FavoriteItem, FavoriteCheckResponse

favorites_router = APIRouter(prefix="/favorites", tags=["Favorites"])

_repo = FavoritesRepoLocal()  # in-memory для простоты

def get_service() -> FavoritesService:
    return FavoritesService(_repo)

@favorites_router.post("/", response_model=FavoriteItem, status_code=201)
def add_to_favorites(data: FavoriteCreate, svc: FavoritesService = Depends(get_service)):
    return svc.add(data.user_id, data.product_id)

@favorites_router.delete("/{favorite_id}")
def remove_favorite(favorite_id: UUID, svc: FavoritesService = Depends(get_service)):
    ok = svc.delete(favorite_id)
    if not ok:
        raise HTTPException(404, "favorite not found")
    return {"id": str(favorite_id), "deleted": True}

@favorites_router.get("/", response_model=list[FavoriteItem])
def list_favorites(user_id: UUID, svc: FavoritesService = Depends(get_service)):
    return svc.list_for_user(user_id)

@favorites_router.get("/check", response_model=FavoriteCheckResponse)
def check_favorite(user_id: UUID, product_id: UUID, svc: FavoritesService = Depends(get_service)):
    return svc.check(user_id, product_id)
