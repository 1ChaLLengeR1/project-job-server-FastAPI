FROM nginx:stable-alpine

COPY dockerfiles/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
