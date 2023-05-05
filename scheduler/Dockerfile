FROM python:3.8-alpine
COPY src /src
WORKDIR /src
RUN pip install -r requirements.txt
CMD ["python", "scheduler.py"]