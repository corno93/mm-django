FROM python:3.10.0a3-alpine3.12

# its recommended to run python in unbuffered mode when using docker containers as it doesnt allow python
# to buffer outputs and instead prints it directly
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# create a separate user just to run the app
RUN adduser -D user
USER user