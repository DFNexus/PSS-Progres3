#pakek python slim biar enteng 
FROM python:3.11-slim

#set avr env bair python ngga buat file .pyc dan output lngsg ke terminal biar tampilannya bersih 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#nentuin workdir 
WORKDIR /app

# instal dependensi sistem untuk database PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

#copy dan install lib py 
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode proyek ke dalam kontainer
COPY . .

