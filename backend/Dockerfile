# Build stage
FROM python:3.11-slim-bookworm AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.7.13 /uv /usr/local/bin/uv

# Set up environment
ENV UV_HOME=/usr/local
ENV PATH="/usr/local/bin:${PATH}"

WORKDIR /backend
COPY . .
COPY scripts/start_app.sh /backend/start_app.sh
RUN chmod +x /backend/start_app.sh

# Install dependencies
RUN uv lock && uv sync

# Runtime stage
FROM python:3.11-slim-bullseye

WORKDIR /backend

# Copy only necessary files from builder
COPY --from=builder /backend /backend


ENV PATH="/backend/.venv/bin:$PATH"

# Expose port and run application
EXPOSE 8000
ENTRYPOINT  ["/backend/start_app.sh"]
