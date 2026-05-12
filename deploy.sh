#!/bin/bash

SERVER="grupo08@100.90.9.76"

echo "Deploy iniciado"

ssh $SERVER << 'EOF'

  set -e

  echo "Entrando al proyecto"

  if [ -d "$HOME/knowflow" ]; then
    cd ~/knowflow

    echo "Actualizando repositorio"
    git fetch --all
    git reset --hard origin/main
    git clean -fd

  else
    echo "Clonando repositorio"
    git clone https://github.com/MoiiLN/knowflow.git ~/knowflow
    cd ~/knowflow
  fi

  echo "Parando producción"
  docker compose -f docker-compose.prod.yml down

  echo "Construyendo producción"
  docker compose -f docker-compose.prod.yml up -d --build

  echo "Migraciones"
  docker exec django python manage.py migrate --noinput

  echo "Collectstatic"
  docker exec django python manage.py collectstatic --noinput

  echo "Estado contenedores"
  docker ps

  echo "Deploy terminado"

EOF
