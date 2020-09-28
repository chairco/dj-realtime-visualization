FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf
COPY docker_nginx.conf /etc/nginx/sites-available/

COPY ssl.csr /etc/nginx/ssl.csr
COPY ssl.key /etc/nginx/ssl.key

RUN mkdir -p /etc/nginx/sites-enabled/\
    && ln -s /etc/nginx/sites-available/docker_nginx.conf /etc/nginx/sites-enabled/

CMD ["nginx", "-g", "daemon off;"]
