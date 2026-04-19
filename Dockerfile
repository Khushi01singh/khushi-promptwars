# ==========================================
# Stage 1: Build the React Frontend
# ==========================================
FROM node:22-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy package files and install dependencies
COPY frontend/package*.json ./
RUN npm install

# Copy the rest of the frontend source code and build
COPY frontend/ ./
RUN echo "Force clean build"
RUN npm run build

# ==========================================
# Stage 2: Serve Frontend (Nginx) & Backend (FastAPI/Gunicorn)
# ==========================================
FROM python:3.10-slim

# Install Nginx
RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*

# Copy built frontend assets from Stage 1 to Nginx's default serving directory
COPY --from=frontend-builder /app/frontend/dist /var/www/html

# Configure Nginx to serve the React app and proxy API requests
RUN rm -f /etc/nginx/sites-enabled/default && \
    rm -f /etc/nginx/sites-available/default && \
    echo 'server { \
    listen 8080; \
    include /etc/nginx/mime.types; \
    location / { \
        root /var/www/html; \
        index index.html index.htm; \
        try_files $uri $uri/ /index.html; \
    } \
    location /api/ { \
        proxy_pass http://127.0.0.1:8000; \
        proxy_set_header Host $host; \
        proxy_set_header X-Real-IP $remote_addr; \
    } \
}' > /etc/nginx/conf.d/webapp.conf

# Set up Backend directory
WORKDIR /app/backend

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Install gunicorn and uvicorn for production serving
RUN pip install --no-cache-dir gunicorn uvicorn

# Copy the rest of the backend source code
COPY backend/ .

# Expose Nginx port and Backend port
EXPOSE 8080 8000

# Create a startup script to run both Nginx and Gunicorn simultaneously
RUN echo '#!/bin/sh\n\
    echo "Starting FastAPI Backend..."\n\
    cd /app/backend\n\
    gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 &\n\
    \n\
    echo "Starting Nginx..."\n\
    nginx -g "daemon off;"\n\
    ' > /app/start.sh

RUN chmod +x /app/start.sh

# Run the startup script
CMD ["/app/start.sh"]
