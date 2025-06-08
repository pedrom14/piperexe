FROM python:3.10-slim 

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-distutils \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]


