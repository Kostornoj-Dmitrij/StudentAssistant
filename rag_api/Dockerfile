FROM python:3.11-slim

COPY . .

RUN pip install PyPDF2 python-docx

CMD ["sh", "-c", "python scripts/initial_setup.py && python main.py"]