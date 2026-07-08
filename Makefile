ENV ?= local

install:
	uv sync --all-extras

clean:
	rm -rf .venv uv.lock .pytest_cache .ruff_cache
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete

run_app:
	uv run uvicorn main:app --reload --log-level debug --port 3000

run_test:
	uv run pytest -s -v

run_test_integration:
	uv run pytest -s -v -m "not slow and not full_integration and not api_integration"

run_test_full:
	uv run pytest -s -v -m ""

lint:
	uv run ruff check .

format:
	uv run ruff format .

migration_up:
	bash infra/scripts/database/migration_up.sh $(ENV)

migration_down:
	bash infra/scripts/database/migration_down.sh $(ENV)

migration_restart:
	bash infra/scripts/database/restart.sh $(ENV)

# ── ansible-vault (infra/ansible/secrets.yml) ────────────────────────────────
# Uzycie: ANSIBLE_PASSWORD='haslo' make vault_decrypt|vault_encrypt|vault_view

vault_decrypt:
	@bash infra/scripts/vault.sh decrypt

vault_encrypt:
	@bash infra/scripts/vault.sh encrypt

vault_view:
	@bash infra/scripts/vault.sh view
