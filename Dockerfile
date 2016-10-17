#FROM ubuntu:14.04
FROM python:3-onbuild
MAINTAINER Carlos Navarro cnavarro@paradigmadigital.com
WORKDIR /usr/src/app
CMD ["python3", "concept_service.py", "2812"]
EXPOSE 2812
