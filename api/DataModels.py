from typing import List, Optional
from fastapi import Cookie
from pydantic import BaseModel

class UserForm(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    password_confirm: Optional[str] = None
    perms: Optional[list] = None

class Token(BaseModel):
    token: Optional[str] = None