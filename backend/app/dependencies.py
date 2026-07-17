from fastapi import Header, HTTPException, status
from .services.auth_service import decode_access_token, get_user_by_id

def current_user_id(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Missing or invalid authorization token.')
    user_id = decode_access_token(authorization.removeprefix('Bearer ').strip())
    if not user_id or not get_user_by_id(user_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or expired authorization token.')
    return user_id
