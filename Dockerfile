# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:2.7

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

RUN pip install -r requirements.txt

CMD exec honcho start
