FROM python:3.14-slim
# ansible-vault bez calego ansible (do (de)szyfrowania infra/ansible/secrets.yml)
RUN pip install --no-cache-dir "ansible-core>=2.16"
