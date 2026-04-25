# 📚 Simple LMS — REST API & Security System
**Project Django dengan Docker untuk mata kuliah Pemrograman Web Lanjut**
**Tugas 3: Implementasi JWT, RBAC, & Pydantic Schema Validation**

# Author
### Nama: Danendra Farrel Haryo Wibowo
### NIM: A11.2023.15025

## Daftar Isi
* [Project Structure](#-project-structure)
* [Setup & Installation](#-setup--installation)
* [Tugas 3: REST API & Security](#-tugas-3-rest-api--security)
* [API Endpoints Mapping](#-api-endpoints-mapping)
* [Tech Stack](#-tech-stack)
* [Screenshots](#-screenshots)
* [Author](#-author)


## Environment Variables

Salin konfigurasi berikut ke dalam file .env di root folder:
Ini, TOML

        SECRET_KEY=your-secret-key-123
        DEBUG=True
        ALLOWED_HOSTS=localhost,127.0.0.1
        
        DB_NAME=lms_db
        DB_USER=postgres
        DB_PASSWORD=postgres
        DB_HOST=db
        DB_PORT=5432

# Setup & Installation
### 1. Clone Repository
Bash

        git clone [https://github.com/DanendraFarrel/simple-lms.git](https://github.com/DanendraFarrel/simple-lms.git)
        cd simple-lms

### 2. Build & Jalankan Container
Bash

        docker compose up --build -d

### 3. Migrasi Database
Bash

        docker compose exec web python manage.py migrate

### 4. Membuat Superuser (Admin)
Bash

        docker compose exec web python manage.py createsuperuser

### 5. Akses Layanan

            Swagger UI (Docs): http://localhost:8000/api/docs
        
            Django Admin: http://localhost:8000/admin

## Tugas 3: REST API & Security

### 1. Authentication System (JWT)

   Sistem menggunakan Stateless Authentication dengan library PyJWT.

        Token Generation: Menghasilkan access_token (validasi request) dan refresh_token (pembaruan token).
        Password Hashing: Menggunakan library bcrypt untuk enkripsi password saat registrasi user baru.

### 2. Role-Based Access Control (RBAC)

   Implementasi proteksi endpoint menggunakan custom decorators (@is_admin, @is_instructor, @is_student).
   
        Role	Permissions	Deskripsi
        Admin	Full Access	Dapat menghapus kursus (DELETE).
        Instructor	Create & Edit	Dapat membuat kursus baru (POST) & edit kursus miliknya.
        Student	Enroll & Progress	Dapat mendaftar kursus & update progres belajar.

### 3. Schema & Model Synchronization
   Sinkronisasi ketat antara Pydantic Schema dan Django Models untuk menghindari Error 500.

        Fix Logic: Menghapus field description dan is_active pada Schema karena tidak terdefinisi di models.py.
        Integrity Handling: Penanganan FOREIGN KEY constraint failed dengan memastikan category_id valid sebelum proses create.

# API Endpoints Mapping

## Authentication
        Method	Endpoint	Auth	Deskripsi
        POST	/api/auth/register	Public	Pendaftaran user baru + hashing password.
        POST	/api/auth/login	Public	Mendapatkan JWT Access & Refresh Token.
        POST	/api/auth/refresh	Auth	Memperbarui Access Token yang expired.
        GET	/api/auth/me	JWT	Mengambil data profil user yang sedang login.
## Courses Management
        Method	Endpoint	Role	Deskripsi
        GET	/api/courses	Public	List semua kursus (Optimasi: select_related).
        POST	/api/courses	Instructor	Membuat kursus baru (Mandatory: category_id).
        PATCH	/api/courses/{id}	Owner	Update kursus (Hanya oleh instruktur pembuat).
        DELETE	/api/courses/{id}	Admin	Menghapus kursus dari database.
## Enrollments & Progress
        Method	Endpoint	Role	Deskripsi
        POST	/api/enrollments	Student	Mendaftar ke kursus tertentu.
        GET	/api/enrollments/my-courses	Student	Melihat kursus yang sedang diambil.
        POST	/api/enrollments/{id}/progress	Student	Mark lesson as completed.
        
# Tech Stack

    Backend: Django 6.0.3
    API Framework: Django Ninja 1.6.2 (UUID Fix Version)
    Security: PyJWT & Bcrypt 4.2.0
    Database: PostgreSQL 15
    Container: Docker & Docker Compose
    OS Environment: Debian 13 (Bookworm)

# Screenshots

Berikut adalah bukti fisik pengujian API di lingkungan Debian 13:

## 1. Dokumentasi Swagger UI (/api/docs)
Menampilkan seluruh list endpoint yang sudah terorganisir.
<img width="761" height="992" alt="Screenshot_20260425_115456" src="https://github.com/user-attachments/assets/e4e538f3-13ed-4ae5-9b63-259dc369f5bc" />

## 2. Login & Profile Verification
Berhasil mendapatkan Token JWT dan mengakses data user (/me).
<img width="746" height="824" alt="Screenshot_20260425_115616" src="https://github.com/user-attachments/assets/84d73441-dc62-40d7-87ef-11b661e6cd05" />
<img width="777" height="829" alt="Screenshot_20260425_115651" src="https://github.com/user-attachments/assets/2947e720-64de-407a-8c16-c807fd24ecb3" />

dan ketika saya input autorize dengan asal asalan dan bukan dari token manapun akan muncul seperti ini :
<img width="1015" height="677" alt="Screenshot_20260425_122808" src="https://github.com/user-attachments/assets/2c3fd96c-f8f9-403c-8db2-49d0da1af876" />

## 3. Role-Based Access Control (RBAC) Test
User dengan role Instructor berhasil melakukan POST Course.
<img width="945" height="655" alt="Screenshot_20260425_123111" src="https://github.com/user-attachments/assets/a880ec2a-333a-41e0-967e-34e29cfe7575" />
<img width="1015" height="958" alt="Screenshot_20260425_120042" src="https://github.com/user-attachments/assets/ce141f39-69f9-4486-994c-ebf9356fc1ff" />
<img width="1033" height="890" alt="Screenshot_20260425_115946" src="https://github.com/user-attachments/assets/16f9ba49-8097-478a-b4eb-001c85f5ec8c" />

## 4. Pencegahan Error 500 (Schema Validation)
Input data tersaring dengan benar oleh Pydantic Schema.
<img width="1015" height="958" alt="Screenshot_20260425_121219" src="https://github.com/user-attachments/assets/eca52715-4daf-4968-ae54-5bb80fbe99be" />
 
