run:
	MSYS_NO_PATHCONV=1 docker-compose up
shell:
	MSYS_NO_PATHCONV=1 docker-compose run web odoo shell
test:
	MSYS_NO_PATHCONV=1 docker-compose run web odoo -i base,opa --addons-path=/mnt/addons,/mnt/extra_addons/queue,/mnt/extra_addons --without-demo=all --test-enable  --test-tags opa --log-level=test --stop-after-init -d test_opa