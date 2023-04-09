"""
User models
"""

# pylint: disable=too-few-public-methods

from datetime import datetime
from typing import Optional

from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr


class UserAuth(BaseModel):
    """User register and login auth"""

    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    """Updatable user fields"""

    email: Optional[EmailStr] = None

    # User information
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserOut(UserUpdate):
    """User fields returned to the client"""

    email: Indexed(EmailStr, unique=True)
    is_admin: bool = False
    disabled: bool = False


class User(Document, UserOut):
    """User DB representation"""

    password: str
    is_admin: bool = False
    email_confirmed_at: Optional[datetime] = None

    def _repr_(self) -> str:
        return f"<User {self.email}>"

    def _str_(self) -> str:
        return self.email

    def _hash_(self) -> int:
        return hash(self.email)

    def _eq_(self, other: object) -> bool:
        if isinstance(other, User):
            return self.email == other.email
        return False

    @property
    def created(self) -> datetime:
        """Datetime user was created from ID"""
        return self.id.generation_time

    @classmethod
    async def by_email(cls, email: str) -> "User":
        """Get a user by email"""
        return await cls.find_one(cls.email == email)