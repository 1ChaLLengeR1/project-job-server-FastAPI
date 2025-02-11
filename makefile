install_dependencies:
	pip install -r requirements.txt

clean_cache:
	find . -name "__pycache__" -exec rm -rf {} + || rmdir /s /q __pycache__
	find . -name "*.pyc" -delete || del /s /q *.pyc

lint:
	flake8 .

run_app:
	uvicorn main:app --reload --log-level debug --port 3000