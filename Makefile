.PHONY: test

REDIS_VERSION?=7.2


rst-lint:
	rst-lint README.rst

flake8:
	flake8 scrapyq tests setup.py

test: flake8
	pytest tests $(ARGS)

coverage: flake8 rst-lint
	coverage run --source scrapyq -m pytest tests $(ARGS)
	coverage report --show-missing --fail-under 100


# Docker test containers

redis-container:
	docker run -d --rm --name redis-scrapyq -p 6379:6379 \
		redis:$(REDIS_VERSION)