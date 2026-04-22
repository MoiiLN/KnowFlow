#!/bin/bash

SERVER="grupo08@100.90.9.76"
APP_DIR="~/knowflow"

echo "Deploy iniciado"

ssh $SERVER << 'EOF'
  echo "Entrando al proyecto"
  cd ~/knowflow

  echo "Actualizando repositorio"
  git pull

  echo "Parando contenedores"
  docker-compose down

  echo "Construyendo contenedor"
  docker-compose up -d --build
  docker exec django python manage.py collectstatic --noinput

  echo "Deploy terminado"
EOF
