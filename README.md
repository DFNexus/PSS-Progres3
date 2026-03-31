# Simple LMS - Django & PostgreSQL Containerization

Proyek ini adalah tugas implementasi sistem manajemen pembelajaran sederhana (Simple LMS) menggunakan framework **Django** dan database **PostgreSQL** yang dijalankan sepenuhnya di dalam environment **Docker**.

## Penjelasan env
Proyek ini menggunakan variabel lingkungan untuk menjaga keamanan kredensial. Pastikan Anda telah membuat file .env berdasarkan daftar berikut:

    DEBUG: Mengaktifkan mode pengecekan error dan fitur pengembangan (Contoh: True).

    SECRET_KEY: Kunci kriptografi unik yang digunakan Django untuk menjaga keamanan data (Contoh: django-insecure-xxx).

    DB_NAME: Nama database yang akan digunakan di dalam PostgreSQL (Contoh: lms_db).

    DB_USER: Username yang diberikan hak akses untuk mengelola database (Contoh: lms_user).

    DB_PASSWORD: Kata sandi rahasia untuk otentikasi database (Contoh: lms_password).

    DB_HOST: Alamat host database, diisi dengan nama service database pada docker-compose (Contoh: db).

    DB_PORT: Port internal yang digunakan untuk komunikasi layanan PostgreSQL (Contoh: 5432).

## Cara Menjalankan Project
Ikuti urutan perintah berikut di terminal Linux Anda untuk menjalankan infrastruktur secara utuh:

### 1. Inisialisasi Environment
Salin template variabel lingkungan agar aplikasi dapat membaca konfigurasi database, ketikkan perntah berikut pada terminal di folder anda:
"cp .env.example .env"

### 2. Membangun Infrastruktur Docker
Jalankan Docker Compose untuk membangun image dan menyalakan container web (Django) serta db (PostgreSQL) di latar belakang:
"sudo docker compose up -d --build"

### 3. Migrasi Database
Sinkronkan skema database Django ke dalam PostgreSQL yang berjalan di container:
"sudo docker compose run --rm web python manage.py migrate"

### 4. Akses Aplikasi
Buka browser dan arahkan ke alamat berikut:

    Django App: http://localhost:8000

    Django Admin: http://localhost:8000/admin

### 5. Screenshot Django welcome page
Berikut adalah tampiland ari Django Welcome page jika sudah berhasil:
<img width="1919" height="1035" alt="Screenshot_20260331_153510" src="https://github.com/user-attachments/assets/6a887dec-e262-4608-aafc-9d331a41e135" />

