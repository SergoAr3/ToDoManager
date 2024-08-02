from fastapi import HTTPException
from starlette import status

HTTP_404_NOT_FOUND_TASK = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
HTTP_404_NOT_FOUND_USER = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
HTTP_400_BAD_REQUEST_ACCESS = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                            detail="The user does not have access")
HTTP_403_FORBIDDEN = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                   detail="Access denied")
HTTP_409_CONFLICT_USER_EXISTS = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                              detail='User with this username already exists!')

HTTP_500_INTERNAL_ERROR = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail="Internal Server Error")
