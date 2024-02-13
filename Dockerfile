FROM python:3.10.9-slim-buster
# pull docker image for ultralytics
FROM ultralytics/ultralytics:latest-cpu

# Copy the source files into the container
WORKDIR /flask-docker
COPY . /flask-docker

RUN apt-get update && apt-get install -y python3.11-venv
# Install pip requirements
RUN pip3 install virtualenv
RUN python3 -m venv web-app 
RUN . web-app/bin/activate
RUN python3 -m pip install -r requirements.txt

EXPOSE 5000
ENV PORT 5000

# Define the command to be run when the container is started
CMD exec gunicorn --bind :$PORT main:app --workers 1 --threads 8 --timeout 0