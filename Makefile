ARTOOLBOX_IMAGE ?= artoolbox:develop
CI_COMMIT_SHORT_SHA ?= $(shell git rev-parse --short HEAD)
GIT_STAMP ?= $(shell git describe)
UNTAGGED_IMAGES ?= $(shell docker images -q --filter "dangling=true")
POSTGRES_PASSWORD ?= postgres
POSTGRES_USER ?= postgres
POSTGRES_DB ?= artoolbox
ARTOOLBOX_HOST ?= 0.0.0.0:8000
.EXPORT_ALL_VARIABLES:

ifeq ($(UNTAGGED_IMAGES),)
  CLEAN_UP =
else
  CLEAN_UP = docker-clean
endif

docker-clean:
	docker rmi $(UNTAGGED_IMAGES)

docker-build:
	docker build --build-arg version=$(GIT_STAMP) -t $(ARTOOLBOX_IMAGE) .

run: COMPOSE ?= docker-compose -f compose-local.yml
run: docker-build
	$(COMPOSE) up

tensor: COMPOSE ?= docker-compose -f compose-local.yml -f compose-tensor.yml
tensor: docker-build
	$(COMPOSE) up

mm: COMPOSE ?= docker-compose -f compose-local.yml
mm: docker-build
	$(COMPOSE) run --name $(CI_COMMIT_SHORT_SHA) web \
	python3 /artoolbox/manage.py makemigrations
	$(COMPOSE) stop
	docker rm $(CI_COMMIT_SHORT_SHA)

script: COMPOSE ?= docker-compose -f compose-local.yml
script: docker-build
	$(eval SCRIPT ?= $(shell read -p "Script: " SCRIPT; echo $$SCRIPT))
	$(COMPOSE) run --name $(CI_COMMIT_SHORT_SHA) web \
	./manage.py $(SCRIPT)
	$(COMPOSE) stop
	docker rm $(CI_COMMIT_SHORT_SHA)


clean: $(CLEAN_UP)
