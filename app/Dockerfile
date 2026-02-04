FROM python:3.11-slim

WORKDIR /app

RUN pip install uv 

COPY pyproject.toml uv.lock ./

RUN uv sync 

COPY app ./app

RUN useradd -m appuser

COPY . . 

USER appuser 

EXPOSE 8080

CMD ["uv", "run", "uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8080"]
