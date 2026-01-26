FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml .
COPY src/ src/

# Install dependencies
RUN uv sync --frozen

# Run the app
CMD ["uv", "run", "uvicorn", "prisme_saas.main:app", "--host", "0.0.0.0", "--port", "8000"]
