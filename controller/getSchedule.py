from fastapi import *
from fastapi.security import OAuth2PasswordBearer
from model.getSchedule import getSchedule
from view.getSchedule import renderSchedule

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/auth")

@router.get("/api/booking")
def Schedule(request:Request,token: str= Depends(oauth2_scheme)):
    db_pool = request.state.db_pool.get("spot")
    redis_pool = request.state.redis_pool

    result = getSchedule(db_pool,token,redis_pool)
    return renderSchedule(result)
