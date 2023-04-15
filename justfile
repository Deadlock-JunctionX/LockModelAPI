dev: build stop
    docker-compose up -d
    docker-compose logs -f app

stop:
    docker-compose down

build:
    docker-compose build

test:
    docker-compose run app pytest
