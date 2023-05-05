FROM python:3.8-alpine
COPY app /src
WORKDIR /src
RUN pip install -r requirements.txt
CMD ["python", "monitoring.py"]