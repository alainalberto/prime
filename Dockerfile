FROM python:3.10-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Instala las dependencias del proyecto
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc musl-dev libpq-dev python3-dev libffi-dev \
    && pip install --upgrade pip 

# Copia los archivos necesarios al contenedor
COPY ./requirements.txt ./

RUN pip install -r requirements.txt

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app
COPY ./ ./

# Define el comando de inicio de la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]