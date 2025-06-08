FROM python:3.10-slim

WORKDIR /app

# Instalações básicas e limpeza
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Clona o repositório Piper
RUN git clone https://github.com/rhasspy/piper.git

# Instala dependências do projeto principal
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia seu app Flask
COPY app.py .

# Cria a pasta de modelos
RUN mkdir -p models/pt_BR

EXPOSE 5000

CMD ["python", "app.py"]


