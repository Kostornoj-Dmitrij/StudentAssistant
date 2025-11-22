FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/chroma_db /app/logs

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install PyPDF2 python-docx

CMD ["sh", "-c", "python scripts/initial_setup.py && python main.py"]