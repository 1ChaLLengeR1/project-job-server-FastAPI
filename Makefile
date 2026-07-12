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

# Dump bazy: MODE=full (custom, do pg_restore) lub MODE=data (plain SQL, tylko dane)
MODE ?= full
db_dump:
	bash infra/scripts/database/dump.sh $(ENV) $(MODE)

# Wgrywa dane z dumpow docs/*.sql (data-only) - uruchamiac PO migration_restart
seed_dump:
	bash infra/scripts/database/seed_from_dump.sh $(ENV)

# Pelny reset: schemat od zera + dane z dumpow
migration_restart_with_data: migration_restart seed_dump

# ── ansible-vault (infra/ansible/secrets.yml) ────────────────────────────────
# Uzycie: ANSIBLE_PASSWORD='haslo' make vault_decrypt|vault_encrypt|vault_view

vault_decrypt:
	@bash infra/scripts/vault.sh decrypt

vault_encrypt:
	@bash infra/scripts/vault.sh encrypt

vault_view:
	@bash infra/scripts/vault.sh view
