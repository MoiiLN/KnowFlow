# Despliegue KnowFlow - Comandos seguros

.PHONY: dev prod migrate collectstatic logs

# Desarrollo local
dev:
	docker compose up --build

# Producción (sin exponer puertos sensibles)
prod:
	docker compose -f docker-compose.prod.yml up -d --build

# Migraciones
migrate:
	docker compose exec backend python manage.py migrate

collectstatic:
	docker compose exec backend python manage.py collectstatic --noinput

# Logs
logs:
	docker compose logs -f

logs-backend:
	docker compose logs backend -f

logs-nginx:
	docker compose logs nginx -f

# Limpieza
clean:
	docker compose down -v
	docker system prune -f

# Backup DB
backup-db:
	docker exec knowflow-db-1 pg_dump -U knowflow knowflow > backup.sql

# Restore DB
restore-db:
	docker exec -i knowflow-db-1 psql -U knowflow knowflow < backup.sql

