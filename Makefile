ARTOOLBOX_IMAGE ?= artoolbox:develop
ARTOOLBOX_TEST_IMAGE ?= artoolbox:develop-test
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
	docker build --target=test --build-arg version=$(GIT_STAMP) -t $(ARTOOLBOX_TEST_IMAGE) .

run: COMPOSE ?= docker-compose -f compose-local.yml
run: docker-build
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

test: COMPOSE ?= docker-compose -f compose-test.yml
test: docker-build
	docker rm -f $(CI_COMMIT_SHORT_SHA) || true
	$(COMPOSE) run --name $(CI_COMMIT_SHORT_SHA) web \
		bash -c "coverage run /artoolbox/manage.py test --noinput && \
		 echo TEST COVERAGE && \
		 coverage report --skip-covered | grep TOTAL"
	$(COMPOSE) stop
	$(COMPOSE) rm -f

clean: $(CLEAN_UP)
