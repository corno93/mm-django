FROM python:3.10.0a3-alpine3.12

# its recommended to run python in unbuffered mode when using docker containers as it doesnt allow python
# to buffer outputs and instead prints it directly
ENV PYTHONUNBUFFERED 1

# black uses regex which requires gcc
# edit: made black a dev dependency
#RUN apk add --no-cache bash python3 uwsgi uwsgi-python3 uwsgi-http build-base python3-dev \
#        py3-pip linux-headers git libcap-dev openssl-dev pcre-dev zlib-dev

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# create a separate user just to run the app
RUN adduser -D user
USER user