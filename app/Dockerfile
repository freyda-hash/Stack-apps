FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Installation de uv et création d'un utilisateur 
RUN pip install --no-cache-dir uv \
    && useradd --create-home --uid 10001 appuser

# Copie séparée des dépendances pour profiter du cache Docker
COPY pyproject.toml uv.lock ./

# Installation des dépendances 
RUN uv sync --frozen --no-dev --no-install-project

# Copie du code de l'application
COPY app ./app

# Attribution des droits à l'utilisateur 
RUN chown -R appuser:appuser /app /opt/venv

USER appuser

EXPOSE 8080

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8080"]