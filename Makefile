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
	COMPOSE_PROJECT_NAME=odoo1401 MSYS_NO_PATHCONV=1 docker-compose up
odoo_shell:
	COMPOSE_PROJECT_NAME=dev1404 MSYS_NO_PATHCONV=1 docker exec -it dev1404_dev_1 /odoo/src/odoo-bin shell --workers=0 --addons-path /odoo/src/addons,/mnt/addons,/mnt/extra_addons/odoo-cloud-platform-14.0,/mnt/extra_addons/queue-14.0,/mnt/extra_addons/account-financial-reporting-14.0,/mnt/extra_addons/reporting-engine-14.0,/mnt/extra_addons/server-ux-14.0,/mnt/extra_addons/server-env-14.0,/mnt/extra_addons/connector-14.0,/mnt/extra_addons/rest-framework-14.0,/mnt/extra_addons/server-tools-14.0,/mnt/extra_addons/payroll-14.0,/mnt/extra_addons/timesheet-13.0,/mnt/extra_addons/pms-14.0,/mnt/extra_addons/project-13.0,/mnt/extra_addons/project-reporting-13.0,/mnt/extra_addons/storage-14.0,/mnt/extra_addons/fleet-13.0,/mnt/extra_addons/helpdesk-13.0,/mnt/addons/odoo-enterprise,/mnt/extra_addons/web-13.0,/mnt/addons/OdooEduERP-14.0,/mnt/extra_addons/account-financial-tools-13.0,/mnt/extra_addons/bank-payment-14.0,/mnt/addons/commission-13.0,/mnt/addons/transport-management-system-13.0,/mnt/addons/search-engine-14.0,/mnt/addons/HRMS-14/core,/mnt/addons/HRMS-14/advanced_salary,/mnt/addons/HRMS-14/appraisal,/mnt/addons/HRMS-14/attendance,/mnt/addons/HRMS-14/branch_transfer,/mnt/addons/HRMS-14/checklist,/mnt/addons/HRMS-14/dashboard,/mnt/addons/HRMS-14/disciplinary_tracking,/mnt/addons/HRMS-14/entry_exit,/mnt/addons/HRMS-14/history,/mnt/addons/HRMS-14/holidays_approval,/mnt/addons/HRMS-14/info,/mnt/addons/HRMS-14/insurance,/mnt/addons/HRMS-14/loan,/mnt/addons/HRMS-14/loan_accounting,/mnt/addons/HRMS-14/overtime,/mnt/addons/HRMS-14/reminder,/mnt/addons/HRMS-14/resignation,/mnt/addons/HRMS-14/appraisal,/mnt/addons/HRMS-14/utils,/mnt/addons/HRMS-14/vacation,/mnt/addons/HRMS-14/service_request,/mnt/addons/HRMS-14/background,/mnt/addons/operating-unit-14.0,/mnt/addons/mis-builder-13.0,/mnt/addons/account-closing-12.0 --db_host=db --db_port=5432 --db_user=odoo --db_password=odoo -d dev04