FROM nginx

RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY /crm/static /crm/static

COPY /crm/upload /crm/upload

COPY /nginx/nginx.conf /etc/nginx/nginx.conf
