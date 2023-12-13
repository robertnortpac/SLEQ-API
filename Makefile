i:
	pip freeze | xargs pip uninstall -y;
	pip install -r requirements.txt;
up:
	docker-compose up -d; docker-compose logs -f python;
down:
	docker-compose down;
reup:
	docker-compose down; docker-compose up -d; docker-compose logs -f python;