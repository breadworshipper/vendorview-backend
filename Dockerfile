# Stage 1: Base image with Python and Uvicorn
FROM tiangolo/uvicorn-gunicorn:python3.11 as base

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Ensure the src directory is copied correctly
COPY ./src /app/src
# COPY .env /app/.env

# # In GitHub Actions, make .env file and insert the environment variables
# RUN echo "DATABASE_URL=${DATABASE_URL}" >> /app/.env && \
#     echo "JWT_SECRET=${JWT_SECRET}" >> /app/.env

ENV DATABASE_URL=${DATABASE_URL}
ENV JWT_SECRET=${JWT_SECRET}

# Set the working directory
WORKDIR /app

# Expose port 80
EXPOSE 80

# Stage 2: Install Redis
FROM base as redis
RUN apt-get update && apt-get install -y redis-server

# Copy the Redis configuration file if needed
# COPY redis.conf /usr/local/etc/redis/redis.conf

# Set the working directory
WORKDIR /app

# Start both Redis and Uvicorn
CMD service redis-server start && uvicorn src.main:app --host 0.0.0.0 --port 80