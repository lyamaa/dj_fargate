# Docker-compose up
up:
	@echo "Starting Docker images..."
	docker-compose -f docker-compose.yml up
	@echo "Docker images started!"

# Docker-compose down
down:
	@echo "Stopping Docker images..."
	docker-compose -f docker-compose.yml down --remove-orphans
	@echo "Docker images stopped!"

clean:
	@echo "Removing Docker images..."
	docker-compose -f docker-compose.yml down --rmi all --remove-orphans
	@echo "Docker images removed!"
	docker volume prune -f
	@echo "Docker volumes removed!"

build:
	@echo "stop docker containers..."
	docker-compose -f docker-compose.yml down --remove-orphans
	@echo "Building Docker images..."
	docker-compose -f docker-compose.yml up --build --remove-orphans
	@echo "Docker images built!"

# Docker-compose migrate
migrate:
	@echo "Migrating database..."
	docker-compose -f docker-compose.yml run --rm backend python manage.py migrate
	@echo "Database migrated!"

makemigrations:
	@echo "Making migrations..."
	docker-compose -f docker-compose.yml run --rm backend python manage.py makemigrations
	@echo "Migrations made!"

flush:
	@echo "Flushing database..."
	docker-compose -f docker-compose.yml run --rm backend python manage.py flush
	@echo "Database flushed!"

# Docker-compose test
test:
	@echo "Running tests..."
	docker-compose -f docker-compose.yml run --rm backend python manage.py test
	@echo "Tests finished!"

shell:
	@echo "Opening shell..."
	docker-compose -f docker-compose.yml run --rm backend python manage.py shell
	@echo "Shell closed!"

black:
	@echo "Running black..."
	black application  --exclude migrations --line-length 79 --target-version py37
	@echo "Black finished!"

isort:
	@echo "Running isort..."
	isort application --skip migrations --line-length 79 --multi-line 3 --trailing-comma --force-grid-wrap 0 --combine-as --line-width 79
	@echo "Isort finished!"


superuser:
	@echo "Creating superuser..."
	docker-compose -f docker-compose.yml run --rm backend python manage.py seed_superuser
	@echo "Superuser created!"

theme:
	@echo "Loading bootstrap theme..."
	docker-compose -f docker-compose.yml run --rm backend python manage.py loaddata admin_interface_theme_bootstrap.json
	@echo "Bootstrap theme loaded!"

dump_theme:
	@echo "Dumping bootstrap theme..."
	docker-compose -f docker-compose.yml run --rm backend python manage.py dumpdata admin_interface.Theme --indent 4 -o admin_interface_theme_{{name}}.json --pks=2
	@echo "Bootstrap theme dumped!"

collectstatic:
	@echo "Collecting static files..."
	docker-compose -f docker-compose.yml run --rm backend python manage.py collectstatic --noinput
	@echo "Static files collected!"

check:
	@echo "Running checks..."
	docker-compose -f docker-compose.yml run --rm backend python manage.py check --deploy
	@echo "Checks finished!"

ruff:
	@echo "Running ruff..."
	ruff application --exclude migrations --line-length 79 --target-version py37
	@echo "Ruff finished!"