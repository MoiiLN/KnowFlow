#!/bin/bash

SERVER="grupo08@100.90.9.76"
APP_DIR="~/knowflow"

echo "Deploy iniciado"

ssh $SERVER << 'EOF'
  echo "Entrando al proyecto"
  if [ -d "$HOME/knowflow" ]; then
    cd ~/knowflow
    echo "Actualizando repositorio"
    git pull
  else
    echo "Clonando repositorio"
    git clone https://github.com/MoiiLN/knowflow.git ~/knowflow
    cd ~/knowflow
  fi

  echo "Parando contenedores"
  docker-compose down

  echo "Construyendo contenedor"
  docker-compose up -d --build
  docker exec django python manage.py collectstatic --noinput

  echo "Deploy terminado"
EOF
