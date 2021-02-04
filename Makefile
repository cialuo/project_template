up:
	COMPOSE_PROJECT_NAME=dev1403 MSYS_NO_PATHCONV=1 docker-compose up --remove-orphans
down:
	COMPOSE_PROJECT_NAME=dev1403 MSYS_NO_PATHCONV=1 docker-compose down
shell:
	COMPOSE_PROJECT_NAME=dev1401 MSYS_NO_PATHCONV=1 docker exec -it dev1401_yugabyte_1 /bin/bash
test:
	COMPOSE_PROJECT_NAME=dev1401 MSYS_NO_PATHCONV=1 docker exec -it dev1403_odoo_1 odoo -i base,opa --addons-path=/mnt/addons,/mnt/extra_addons --without-demo=all --test-enable  --test-tags opa --log-level=test --stop-after-init -d test_opa3
