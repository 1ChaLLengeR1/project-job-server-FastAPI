install_dependencies:
	pip install -r requirements.txt

run_app:
	uvicorn main:app --reload --log-level debug --port 3000