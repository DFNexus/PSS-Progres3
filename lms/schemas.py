from ninja import Schema
from typing import List, Optional
from datetime import datetime

# --- Auth Schemas ---
class RegisterSchema(Schema):
    username: str
    password: str
    email: str
    role: str = "student"

class LoginSchema(Schema):
    username: str
    password: str

class TokenSchema(Schema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshSchema(Schema):
    refresh_token: str

class UserProfileSchema(Schema):
    id: int
    username: str
    email: str
    role: str

class UserUpdateSchema(Schema):
    email: Optional[str] = None

# --- Course Schemas ---
class CourseInSchema(Schema):
    title: str
    category_id: int

class CourseOutSchema(Schema):
    id: int
    title: str
    instructor_id: int
    category_id: int

class UserOutSchema(Schema):
    id: int
    username: str
    email: str
    role: str

# --- Enrollment Schemas ---
class ProgressUpdateSchema(Schema):
    lesson_id: int
    is_completed: bool
