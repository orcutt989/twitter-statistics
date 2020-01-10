FROM python:3
ADD banno.py /
RUN pip install requests emoji requests_async
CMD [ "python", "./banno.py" ]