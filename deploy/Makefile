build:
	sh download_models.sh
	docker-compose build
up:
	docker-compose up -d
restart:
	make build
	make up

down:
	docker-compose down
