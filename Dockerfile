FROM python:3.6
LABEL maintainer "Bhargav Shukla <shukla.bhargav.k@gmail.com>"
RUN apt-get update
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt
EXPOSE 5000