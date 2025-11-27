from uuid import uuid4
from app.services.favorites_service import FavoritesService
from app.repositories.favorites_repo_local import FavoritesRepoLocal

def _svc() -> FavoritesService:
    return FavoritesService(FavoritesRepoLocal())

def test_add_and_list_favorites():
    svc = _svc()
    user = uuid4()
    p1, p2 = uuid4(), uuid4()
    f1 = svc.add(user, p1)
    f2 = svc.add(user, p2)
    items = svc.list_for_user(user)
    ids = {f.product_id for f in items}
    assert f1.product_id in ids and f2.product_id in ids

def test_check_and_delete_favorite():
    svc = _svc()
    user, product = uuid4(), uuid4()
    created = svc.add(user, product)
    check = svc.check(user, product)
    assert check["in_favorites"] is True
    assert check["favorite_id"] == created.id
    ok = svc.delete(created.id)
    assert ok is True
    check2 = svc.check(user, product)
    assert check2["in_favorites"] is False
    assert check2["favorite_id"] is None

