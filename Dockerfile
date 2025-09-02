FROM python:3.13.7-slim
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock README.md ./
COPY src/ ./src/
RUN poetry install
EXPOSE 8000
CMD ["poetry", "run", "fastapi", "dev", "src/geneva/main.py", "--host", "0.0.0.0"]