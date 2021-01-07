FROM python:3
ENV PIP_NO_CACHE_DIR=1
RUN pip install --upgrade pip && pip install 'django<4' \
        'djangorestframework<4' \
        'djangorestframework-simplejwt<5' \
        'django-import-export<3' \
        'django-rest-passwordreset<2' \
        'psycopg2<3' \
        'gunicorn<21' \
        'django-cors-headers<4' \
        'requests<3' \
        'uuid<2'
WORKDIR /code
ADD ./entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]