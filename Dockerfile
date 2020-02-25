FROM python:3
COPY . /app
RUN pip install requests emoji requests_async
CMD python banno.py -run