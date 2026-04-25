from ninja import NinjaAPI, Router
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from .models import User, Course, Category, Lesson, Enrollment, Progress
from .schemas import *
from .security import JWTAuth, create_jwt_token, SECRET_KEY, ALGORITHM
from .decorators import is_instructor, is_admin, is_student
import jwt

api = NinjaAPI(
    title="Simple LMS API",
    description="API Documentation for Django Ninja LMS",
    version="1.0.0"
)

auth_router = Router(tags=["Authentication"])
course_router = Router(tags=["Courses"])
enrollment_router = Router(tags=["Enrollments"])

# ==========================================
# AUTENTIKASI ENDPOINT
# ==========================================
@auth_router.post("/register", response={201: UserProfileSchema, 400: dict})
def register(request, payload: RegisterSchema):
    if User.objects.filter(username=payload.username).exists():
        return 400, {"detail": "Username Sudah Ada"}
    
    user = User.objects.create(
        username=payload.username,
        email=payload.email,
        password=make_password(payload.password),
        role=payload.role
    )
    return 201, user

@auth_router.post("/login", response={200: TokenSchema, 401: dict})
def login(request, payload: LoginSchema):
    user = authenticate(username=payload.username, password=payload.password)
    if not user:
        return 401, {"detail": "Keidensial Tidak Valid"}
    
    return 200, {
        "access_token": create_jwt_token(user, "access"),
        "refresh_token": create_jwt_token(user, "refresh")
    }

@auth_router.post("/refresh", response={200: TokenSchema, 401: dict})
def refresh_token(request, payload: RefreshSchema):
    try:
        decoded = jwt.decode(payload.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if decoded.get("type") != "refresh":
            return 401, {"detail": "Tipe Token ndak Valid"}
        
        user = User.objects.get(id=decoded["user_id"])
        return 200, {
            "access_token": create_jwt_token(user, "access"),
            "refresh_token": payload.refresh_token
        }
    except jwt.PyJWTError:
        return 401, {"detail": "Token sudah tidak valid"}

@auth_router.get("/me", auth=JWTAuth(), response=UserProfileSchema)
def get_me(request):
    return request.user

@auth_router.put("/me", auth=JWTAuth(), response=UserProfileSchema)
def update_profile(request, payload: UserUpdateSchema):
    user = request.user
    if payload.email:
        user.email = payload.email
    user.save()
    return user

# ==========================================
# COURSES ENDPOINTS
# ==========================================
@course_router.get("/", response=List[CourseOutSchema])
def list_courses(request):

    return Course.objects.for_listing().all()

@course_router.get("/{course_id}", response=CourseOutSchema)
def get_course(request, course_id: int):
    return get_object_or_404(Course, id=course_id)

@course_router.post("/", auth=JWTAuth(), response={201: CourseOutSchema})
@is_instructor
def create_course(request, payload: CourseInSchema):
    course = Course.objects.create(
        title=payload.title,
        category_id=payload.category_id, # Ambil dari payload
        instructor=request.user
    )
    return 201, course

@course_router.patch("/{course_id}", auth=JWTAuth(), response={200: CourseOutSchema, 403: dict})
@is_instructor
def update_course(request, course_id: int, payload: CourseInSchema):
    course = get_object_or_404(Course, id=course_id)
    
    # Ownership Validation
    if course.instructor_id != request.user.id and request.user_role != 'admin':
        return 403, {"detail": "Anda tidak berwenang untuk ngubah kursus ini"}
        
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(course, attr, value)
    course.save()
    return 200, course

@course_router.delete("/{course_id}", auth=JWTAuth(), response={204: None})
@is_admin
def delete_course(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return 204, None

# ==========================================
# ENROLL ENDPOINTS
# ==========================================
@enrollment_router.post("/{enrollment_id}/progress", auth=JWTAuth())
@is_student
def update_progress(request, enrollment_id: int, lesson_id: int):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user)
    lesson = get_object_or_404(Lesson, id=lesson_id)

    obj, created = Progress.objects.update_or_create(
        enrollment=enrollment, 
        lesson=lesson,
        defaults={'is_completed': True}
    )
    return {"status": "success"}

@enrollment_router.get("/my-courses", auth=JWTAuth(), response=List[CourseOutSchema])
@is_student
def my_courses(request):
    # Ganti 'user' menjadi 'student'
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    return [e.course for e in enrollments]

@enrollment_router.post("/{course_id}/progress", auth=JWTAuth(), response={200: dict})
@is_student
def update_progress(request, course_id: int, payload: ProgressUpdateSchema):
    # Logic nandai lesson selesai 
    return 200, {"detail": "Progress updated"}

# Registrasi Router
api.add_router("/auth", auth_router)
api.add_router("/courses", course_router)
api.add_router("/enrollments", enrollment_router)
