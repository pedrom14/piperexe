# Usa imagem oficial com PyTorch 2.1 CPU
FROM pytorch/pytorch:2.1.0-cpu

WORKDIR /app

# Instala dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsndfile1 libsndfile1-dev ffmpeg libsm6 libxext6 && \
    rm -rf /var/lib/apt/lists/*

# Copia tudo para o container
COPY . /app

# Atualiza pip e instala dependências restantes
RUN pip install --upgrade pip && \
    pip install Flask==2.3.2 soundfile TTS==0.21.1

EXPOSE 5000
CMD ["python3", "app.py"]




