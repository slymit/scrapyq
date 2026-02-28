.PHONY: test

REDIS_VERSION?=7.2


md-lint:
	mdformat --check README.md

lint:
	ruff check scrapyq tests
	ruff format --check --diff scrapyq tests

format:
	ruff check --fix scrapyq tests
	ruff format scrapyq tests

test: lint
	pytest tests $(ARGS)

coverage: lint md-lint
	pytest --cov=scrapyq --cov-report=term-missing --cov-fail-under=100 tests $(ARGS)


# Docker test containers

redis-container:
	docker run -d --rm --name redis-scrapyq -p 6379:6379 \
		redis:$(REDIS_VERSION)