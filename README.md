**Simple LMS — REST API & Security System :**

**Author :**
Nama: Danendra Farrel Haryo Wibowo
NIM: A11.2023.15025


**Project Django dengan Docker untuk Tugas 3: Authentication, Authorization, & Rest API**

Cara Menjalankan Project
1. Clone & Build


        git clone https://github.com/DanendraFarrel/simple-lms.git
        cd simple-lms
        docker compose up --build

2. Database & Superuser

Buka terminal baru untuk melakukan migrasi dan membuat akun admin utama:


    docker compose exec web python manage.py migrate
    docker compose exec web python manage.py createsuperuser

3. Akses Dokumentasi & API

        Swagger UI (Docs): http://localhost:8000/api/docs

        Django Admin: http://localhost:8000/admin

**Tugas 3: REST API, Security, & Schema Validation :**

1. Authentication System (JWT)

Implementasi menggunakan PyJWT dengan sistem Stateless Authentication.

    Access Token: Digunakan untuk otorisasi setiap request (Header: Authorization: Bearer <token>).

    Refresh Token: Digunakan untuk mendapatkan access token baru tanpa login ulang.

    Hashing: Password disimpan menggunakan algoritma bcrypt (Secure Hashing).

2. Authorization & RBAC (Role-Based Access Control)

Pembatasan akses menggunakan custom decorators pada api.py.
Role	Izin Akses (Permissions)
Admin	Full Access, Delete Courses, Manage Users.
Instructor	Create Course, Update Course (hanya miliknya), View List.
Student	Enroll to Course, Update Learning Progress, View My Courses.

Ownership Validation: Pada fungsi update_course, sistem melakukan pengecekan course.instructor_id == request.user.id untuk mencegah instruktur lain mengubah data yang bukan miliknya.
3. Schema Synchronization & Validation

Menggunakan Pydantic (Django Ninja) untuk memastikan data input/output sinkron dengan database.
Schema	Field Terintegrasi	Penyesuaian Teknis
UserOut	id, username, email, role	Sinkron dengan Custom User Model.
CourseIn	title, category_id	Menghapus description (tidak ada di Model).
CourseOut	id, title, instructor_id	Menangani relasi Foreign Key secara eksplisit.

API Endpoints Mapping
Auth & Profile

    POST /api/auth/register — Pendaftaran user baru (Hash password via bcrypt).

    POST /api/auth/login — Pertukaran kredensial dengan JWT Token.

    GET /api/auth/me — Mengambil data profil user yang sedang aktif.

Course Management

    GET /api/courses — Menampilkan daftar kelas (Optimasi: select_related).

    POST /api/courses — [Instructor Only] Menambah kelas baru.

    DELETE /api/courses/{id} — [Admin Only] Menghapus kelas dari sistem.

Enrollment & Progress

    POST /api/enrollments — [Student Only] Mendaftar ke kursus.

    GET /api/enrollments/my-courses — Melihat daftar kursus yang diambil.

    POST /api/enrollments/{id}/progress — Menandai materi selesai (is_completed).

Bukti Fisik Pengujian 
1. Dokumentasi Swagger UI

Screenshot tampilan /api/docs yang memuat folder Auth, Courses, dan Enrollments.

    File: screenshots/01_swagger_docs.png

2. Pengujian JWT (Login & Profile)

Menampilkan hasil POST /login (mendapat token) dan GET /me (data user muncul).

    File: screenshots/02_jwt_auth_me.png

3. Implementasi RBAC (Role Instructor)

Menunjukkan user dengan role instructor berhasil melakukan POST kelas baru.

    File: screenshots/03_rbac_instructor_post.png

4. Pencegahan Error 500 (Schema Match)

Bukti bahwa input data sudah tervalidasi dan tidak terjadi IntegrityError atau Unexpected Keyword.

    File: screenshots/04_schema_validation_success.png

Docker Services
Service	Image	Port	Keterangan
web	Python 3.12-slim	8000	Django Application (Debian Based)
db	PostgreSQL 15	5432	Relational Database
Catatan Penting

    UUID Fix: Proyek ini menggunakan django-ninja>=1.6.2 untuk menghindari konflik registrasi UUID pada Django 6.

    Port: Menggunakan port default 8000. Pastikan tidak ada service lain yang berjalan di port tersebut.

    Data Integrity: Selalu pastikan category_id yang dimasukkan saat POST Course sudah ada di Django Admin.

