FROM python:3.10.0a3-alpine3.12

# its recommended to run python in unbuffered mode when using docker containers as it doesnt allow python
# to buffer outputs and instead prints it directly
ENV PYTHONUNBUFFERED 1

# black uses regex which requires gcc
# edit: made black a dev dependency
#RUN apk add --no-cache bash python3 uwsgi uwsgi-python3 uwsgi-http build-base python3-dev \
#        py3-pip linux-headers git libcap-dev openssl-dev pcre-dev zlib-dev

RUN apk add --update --no-cache postgresql-client

# in order to keep the applications docker image as light as possible, here we set up aliases for
# temporary build dependencies. on line 23 we then delete these dependencies
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev


COPY ./requirements.txt /requirements.txt
COPY ./.flake8 /.flake8
RUN pip install -r /requirements.txt

RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# create a separate user just to run the app
RUN adduser -D user
USER user