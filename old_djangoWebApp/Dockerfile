FROM python:3.10-slim
# EXPOSE 8000
WORKDIR /app 
COPY requirements.txt /app
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /app