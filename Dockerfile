FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-distutils \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    libsndfile1 \
    libsndfile1-dev \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN python -m pip install --upgrade pip

# Instala as dependências usando o índice extra do PyTorch para pacotes CPU
RUN pip install --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]




