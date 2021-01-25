# sibdev-test

A test project for processing deals in Django, 
with processing csv files sent to the server and returning the best buyers data.

Requirements
------------
The project was built in Django using the following requirements:
- rest_framework

Deploy
------
The project runs as a Docker app with multiple containers.
Build and run docker using command:
> docker-compose -f docker-compose.yml up -d --build
