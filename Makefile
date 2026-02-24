.PHONY: test

REDIS_VERSION?=7.2


md-lint:
	mdformat --check README.md

flake8:
	flake8 scrapyq tests

test: flake8
	pytest tests $(ARGS)

coverage: flake8 md-lint
	pytest --cov=scrapyq --cov-report=term-missing --cov-fail-under=100 tests $(ARGS)


# Docker test containers

redis-container:
	docker run -d --rm --name redis-scrapyq -p 6379:6379 \
		redis:$(REDIS_VERSION)