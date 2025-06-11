# Desinsight Workspace Docker Image
# Multi-stage build for optimized deployment across 5 devices

# Base Python environment
FROM python:3.11-slim AS base-workspace

# Metadata
LABEL maintainer="Desinsight Team"
LABEL description="Distributed RAG Workspace for 5-Device + 3-NAS Architecture"
LABEL version="1.0.0"

# System dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    vim \
    nano \
    build-essential \
    nodejs \
    npm \
    rsync \
    openssh-client \
    htop \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy entire workspace
COPY . .

# Create necessary directories
RUN mkdir -p \
    /workspace/data \
    /workspace/logs \
    /workspace/models \
    /workspace/embeddings \
    /workspace/config \
    /workspace/temp

# Set permissions
RUN chmod +x /workspace/scripts/*.sh || true

# Environment variables
ENV PYTHONPATH=/workspace
ENV DEVICE_TYPE=auto_detect
ENV DEVICE_ROLE=auto_detect

# Expose common ports
EXPOSE 8000 8001 8002 8003 8004 8005

# Default command
CMD ["/workspace/docker/entrypoint.sh"]

# ============================================
# Central Controller (HOME iMac i7 64GB)
# ============================================
FROM base-workspace AS central-controller

ENV DEVICE_TYPE=home_imac_i7_64gb
ENV DEVICE_ROLE=central_controller

# Install additional packages for controller
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    websockets \
    aiohttp

# Copy controller-specific files
COPY docker/central-controller/ /workspace/docker/controller/

# Expose controller ports
EXPOSE 8000 8001 3000

# Controller startup
CMD ["/workspace/docker/controller/start_controller.sh"]

# ============================================
# Embedding Server (Mac Mini M2 Pro 32GB)
# ============================================
FROM base-workspace AS embedding-server

ENV DEVICE_TYPE=mac_mini_m2pro_32gb
ENV DEVICE_ROLE=embedding_server

# Install ML/AI packages for embedding
RUN pip install --no-cache-dir \
    sentence-transformers \
    torch \
    torchvision \
    transformers \
    chromadb

# Copy embedding-specific files
COPY docker/embedding-server/ /workspace/docker/embedding/

# Expose embedding ports
EXPOSE 8002 8006

# Embedding startup
CMD ["/workspace/docker/embedding/start_embedding.sh"]

# ============================================
# Inference Server (Office Mac Studio M4 Pro)
# ============================================
FROM base-workspace AS inference-server

ENV DEVICE_TYPE=mac_studio_m4pro_64gb
ENV DEVICE_ROLE=inference_server

# Install inference packages
RUN pip install --no-cache-dir \
    ollama \
    langchain \
    openai

# Copy inference-specific files
COPY docker/inference-server/ /workspace/docker/inference/

# Expose inference ports
EXPOSE 8003 8007

# Inference startup
CMD ["/workspace/docker/inference/start_inference.sh"]

# ============================================
# UI Server (Office iMac i7 40GB)
# ============================================
FROM base-workspace AS ui-server

ENV DEVICE_TYPE=office_imac_i7_40gb
ENV DEVICE_ROLE=ui_server

# Install UI packages
RUN pip install --no-cache-dir \
    streamlit \
    gradio \
    flask

# Install Node.js dependencies
RUN npm install -g \
    @angular/cli \
    react-scripts \
    serve

# Copy UI-specific files
COPY docker/ui-server/ /workspace/docker/ui/

# Expose UI ports
EXPOSE 8004 8008

# UI startup
CMD ["/workspace/docker/ui/start_ui.sh"]

# ============================================
# Development Environment (Multi-purpose)
# ============================================
FROM base-workspace AS development

ENV DEVICE_TYPE=development
ENV DEVICE_ROLE=development

# Install all packages for development
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    sentence-transformers \
    torch \
    ollama \
    streamlit \
    jupyter \
    notebook

# Install development tools
RUN npm install -g \
    nodemon \
    typescript \
    @types/node

# Copy development-specific files
COPY docker/development/ /workspace/docker/dev/

# Expose all ports for development
EXPOSE 8000 8001 8002 8003 8004 8005 8888 3000

# Development startup
CMD ["/workspace/docker/dev/start_development.sh"] 