build:
	docker compose up --build

up:
	docker compose up

upd:
	docker compose up -d

down:
	docker compose down

downv:
	docker compose down -v

ps:
	docker compose ps

csu:
	docker compose run --rm web python manage.py createsuperuser

mk:
	docker compose run --rm web python manage.py makemigrations

migrate:
	docker compose run --rm web python manage.py migrate

shell:
	docker compose run --rm web python manage.py shell

test:
	docker compose run --rm web pytest

bash:
	docker compose run --rm web /bin/bash

logs:
	docker compose logs web
