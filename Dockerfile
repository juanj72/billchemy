FROM python:3.12-slim

WORKDIR /app

# 1) Sistema + LibreOffice mínimo
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libreoffice-core libreoffice-writer \
    && rm -rf /var/lib/apt/lists/*

# 2) Poetry en el entorno global
RUN pip install poetry \
    && poetry config virtualenvs.create false

# 3) Dependencias del proyecto
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-interaction --no-ansi

# 4) Código aplicación
COPY . /app

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
