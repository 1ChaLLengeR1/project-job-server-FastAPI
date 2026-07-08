ENV ?= local

install:
	uv sync --all-extras
	uv run pre-commit install

clean:
	rm -rf .venv uv.lock .pytest_cache .ruff_cache
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete

run_app:
	uv run uvicorn main:app --reload --log-level debug --port 3000

lint:
	uv run ruff check .

format:
	uv run ruff format .

migration_up:
	bash infra/scripts/database/migration_up.sh $(ENV)

migration_down:
	bash infra/scripts/database/migration_down.sh $(ENV)

VAULT_IMAGE = project_job_vault

vault_build:
	docker build -t $(VAULT_IMAGE) -f infra/dockerfiles/dockerfile/vault.dockerfile infra/dockerfiles/dockerfile

vault_encrypt: vault_build
	docker run --rm -e ANSIBLE_PASSWORD -v "$(CURDIR)/infra/ansible:/work" $(VAULT_IMAGE) \
		sh -c 'echo "$$ANSIBLE_PASSWORD" > /tmp/vp && ansible-vault encrypt secrets.yml --vault-password-file /tmp/vp'

vault_decrypt: vault_build
	docker run --rm -e ANSIBLE_PASSWORD -v "$(CURDIR)/infra/ansible:/work" $(VAULT_IMAGE) \
		sh -c 'echo "$$ANSIBLE_PASSWORD" > /tmp/vp && ansible-vault decrypt secrets.yml --vault-password-file /tmp/vp'

vault_view: vault_build
	docker run --rm -e ANSIBLE_PASSWORD -v "$(CURDIR)/infra/ansible:/work" $(VAULT_IMAGE) \
		sh -c 'echo "$$ANSIBLE_PASSWORD" > /tmp/vp && ansible-vault view secrets.yml --vault-password-file /tmp/vp'
