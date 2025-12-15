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

lint:
	ruff format .

check:
	ruff check . --fix

format:
	ruff check . --fix && \
    ruff format .

shell:
	python manage.py shell
