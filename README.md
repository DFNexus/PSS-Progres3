Danendra Farrel Haryo Wibowo 
A11.2023.15025
Pemrograman Sisi Server : A11.4618

# Simple LMS - Database Schema & ORM Optimization
**Progres 2: Implementasi Skema Relasional dan Manajemen Query**

Proyek ini merupakan implementasi *backend* untuk sistem manajemen pembelajaran (LMS) menggunakan Django. Fokus utama dari pengerjaan ini adalah perancangan skema database yang mendukung hierarki data kompleks serta optimasi pengambilan data untuk performa aplikasi yang lebih baik.

## Fitur Utama

Aplikasi ini mencakup beberapa logika yang diatur melalui Django Models:
* **Hierarki Kategori:** Implementasi *Self referencing Foreign Key* yang memungkinkan kategori memiliki induk dan anak (hirarki).
* **Manajemen Peran Pengguna:** Sistem autentikasi yang membedakan antara Admin, Instruktur, dan Siswa.
* **Optimasi Pengurutan:** Pengaturan urutan materi secara otomatis berdasarkan kolom *order*.
* **Integritas Data:** Penggunaan *Unique Constraints* pada tabel pendaftaran untuk mencegah duplikasi data.
* **Pelacakan Progres:** Pencatatan status penyelesaian materi bagi setiap siswa.
  
* Model Managers & Custom QuerySet
Untuk memastikan efisiensi di seluruh aplikasi, saya telah mengimplementasikan Custom Managers:
* **Course.objects.for_listing()**: Secara otomatis menerapkan `select_related('category', 'instructor')`. Ini memastikan data relasional diambil dalam satu query (digunakan pada script demo).
* **Enrollment.objects.for_student_dashboard()**: Custom QuerySet yang sudah dioptimasi untuk menampilkan progres belajar siswa tanpa memicu N+1 query pada data Lesson.


## Analisis Optimasi Query (Fakta Teknis)
Salah satu aspek krusial dalam tugas ini adalah penyelesaian masalah **N+1 Query**. Pengambilan data relasional dilakukan menggunakan teknik *Eager Loading* untuk meminimalisir beban pada database.

### Perbandingan Kinerja
Berdasarkan pengujian menggunakan script `demo_optimization.py`, berikut adalah perbandingan jumlah *query* yang dikirimkan ke database:

### Dokumentasi Eksekusi
<img width="848" height="326" alt="Screenshot_20260406_152136" src="https://github.com/user-attachments/assets/757c0e1a-36b4-402f-816d-5556123692a7" />

## Konfigurasi Admin Interface
Panel Admin Django telah dikonfigurasi untuk meningkatkan efisiensi pengelolaan data:
* **Inline Editing:** Instruktur dapat menambah atau mengedit materi (Lesson) langsung di halaman Kursus.
* **Filtering & Search:** Memudahkan pencarian data kursus berdasarkan judul, kategori, atau instruktur.
* **Informatif:** Menampilkan kolom-kolom penting secara langsung pada daftar tabel.
<img width="1920" height="825" alt="Screenshot_20260406_152207" src="https://github.com/user-attachments/assets/5cd5d707-f0a9-4331-b239-6c27a367e519" />

* note : ini adalah tampilan admin di akun saya, sudah ada beberapa data yang sudah saya tambahkan, tetapi pada saat anda coba membuat akun dan mendapati tidak ada apa apa jangan panik, itu normal karna akun anda baru, dan belum ditambahkan apa apa"

## Instalasi dan Setup

### 1. Persiapan Dependensi
Pastikan Anda berada di dalam *virtual environment*, lalu jalankan:
"pip install -r requirements.txt"

### 2. Migrasi dan Inisialisasi Data
Proyek ini menyediakan fixtures untuk memudahkan evaluasi. Jalankan perintah berikut untuk membuat database dan mengisi data awal secara otomatis:
"python3 manage.py migrate"
"python3 manage.py loaddata lms/fixtures/initial_data.json"

### 3. Menjalankan Demo Optimasi
Untuk memverifikasi efisiensi penggunaan Django ORM secara langsung, jalankan script berikut:
"python3 demo_optimization.py"

## atau agar lebih mudah bisa menggunakan docker saja 
setelah melakukan clone, jalankan saja "docker compose up -d", pastikan di system kalian sudah terinstall docker, dan jalankan di dir yang ada dockerfile dan docker composenya

## Akses Admin Panel
Untuk mengakses dashboard admin di `http://localhost:8000/admin`, Anda dapat membuat akun superuser baru melalui kontainer Docker dengan perintah berikut:
"docker compose exec web python manage.py createsuperuser"

