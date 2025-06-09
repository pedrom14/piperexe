FROM python:3.10-slim

WORKDIR /app

# Instala dependências do sistema, incluindo libsndfile1 para o soundfile funcionar
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-distutils \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos do projeto
COPY . /app

# Atualiza o pip
RUN python -m pip install --upgrade pip

# Instala dependências Python (torch, flask, soundfile, etc.)
RUN pip install -r requirements.txt

# Expõe a porta usada pela API Flask
EXPOSE 5000

# Comando para iniciar o servidor Flask
CMD ["python", "app.py"]


