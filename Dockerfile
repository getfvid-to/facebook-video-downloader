FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy project definition and install dependencies
COPY pyproject.toml setup.py requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir .

# Copy remaining code
COPY . .

# Directory for downloaded content
VOLUME ["/downloads"]

ENTRYPOINT ["fb-dl", "--output", "/downloads"]
CMD ["--help"]
