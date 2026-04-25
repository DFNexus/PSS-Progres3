from functools import wraps
from ninja.errors import HttpError

def is_instructor(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user_role not in ['instructor', 'admin']:
            raise HttpError(403, "Akses ditolak: Butuh role Instructor")
        return func(request, *args, **kwargs)
    return wrapper

def is_admin(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user_role != 'admin':
            raise HttpError(403, "Akses ditolak: Butuh role Admin Bosss")
        return func(request, *args, **kwargs)
    return wrapper

def is_student(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        # Admin dan Instructor dapat ngakses endpoint student
        if request.user_role not in ['student', 'instructor', 'admin']:
             raise HttpError(403, "Akses ditolak: Membutuhkan role Student")
        return func(request, *args, **kwargs)
    return wrapper
