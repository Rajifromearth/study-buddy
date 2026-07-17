from fastapi import APIRouter, Header, HTTPException, status

from ..models.user import User, UserCreate, UserLogin
from ..services.auth_service import authenticate_user, create_access_token, create_user, decode_access_token, get_user_by_id

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/signup')
def signup(payload: UserCreate) -> dict:
    try:
        user = create_user(payload.email, payload.password, payload.username)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
    return {'user': user, 'token': create_access_token(user.id)}


@router.post('/login')
def login(payload: UserLogin) -> dict:
    user = authenticate_user(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid email or password.')
    return {'user': user, 'token': create_access_token(user.id)}


@router.get('/me', response_model=User)
def me(authorization: str | None = Header(default=None)) -> User:
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Missing or invalid authorization token.')
    user_id = decode_access_token(authorization.removeprefix('Bearer ').strip())
    user = get_user_by_id(user_id) if user_id else None
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or expired authorization token.')
    return user
