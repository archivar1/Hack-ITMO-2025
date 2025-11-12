poetry:
	poetry install && poetry shell

run:
	docker-compose down -v
	docker-compose build 
	docker-compose up -d --remove-orphans --quiet-pull
