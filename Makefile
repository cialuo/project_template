up:
	ODOO_QUEUE_JOB_PORT=8069 COMPOSE_PROJECT_NAME=dev1404 MSYS_NO_PATHCONV=1 docker-compose -f docker-compose.dev.yml up --remove-orphans
up_with_build:
	ODOO_QUEUE_JOB_PORT=8069 COMPOSE_PROJECT_NAME=dev1404 MSYS_NO_PATHCONV=1 docker-compose -f docker-compose.dev.yml  up --build --remove-orphans
down:
	COMPOSE_PROJECT_NAME=dev1404 MSYS_NO_PATHCONV=1 docker-compose -f docker-compose.dev.yml down 
down_with_vl:
	COMPOSE_PROJECT_NAME=dev1404 MSYS_NO_PATHCONV=1 docker-compose -f docker-compose.dev.yml down --volumes
shell:
	COMPOSE_PROJECT_NAME=dev1404 MSYS_NO_PATHCONV=1 docker exec -it dev01_odoo_1 /bin/bash
test:
	COMPOSE_PROJECT_NAME=dev1405 MSYS_NO_PATHCONV=1 docker-compose -f docker-compose.test.dev.yml run test
dev:
	COMPOSE_PROJECT_NAME=dev1401 MSYS_NO_PATHCONV=1 docker-compose -f docker-compose.test.dev.yml up
start:
	COMPOSE_PROJECT_NAME=dev1404 MSYS_NO_PATHCONV=1 docker-compose up