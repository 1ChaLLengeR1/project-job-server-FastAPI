FROM nginx:stable-alpine

COPY infra/dockerfiles/nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
