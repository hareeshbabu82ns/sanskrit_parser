FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 9000
CMD python ./sanskrit_parser/rest_api/run.py