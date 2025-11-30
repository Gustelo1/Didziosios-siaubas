.PHONY: runserver migrate user docker lint shell

run:
	python manage.py runserver 127.0.0.1:8000

migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations

user:
	DJANGO_SUPERUSER_EMAIL=not_important@not_important.com \
	DJANGO_SUPERUSER_USERNAME=gustas \
	DJANGO_SUPERUSER_PASSWORD=gustas \
	python manage.py createsuperuser --noinput || echo "Superuser already exists"

docker:
	docker-compose up -d

rebuild_db:
	docker exec -i katalogas-postgres-1 psql -U adp -d adp-dev -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;" && \
	docker exec -i katalogas-postgres-1 psql -U adp -d adp-dev < backup.sql && \
	python manage.py migrate && \
	python manage.py rebuild_index --noinput

lint:
	ruff format .

check:
	ruff check . --fix

format:
	ruff check . --fix && \
    ruff format .

translations:
	cd vitrina && \
	poetry run python ../manage.py makemessages -l en --no-location && \
	poetry run python ../manage.py compilemessages -l en && \
	cd ..

delete_db:
	docker exec -i katalogas-postgres-1 psql -U adp -d adp-dev -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
shell:
	python manage.py shell
