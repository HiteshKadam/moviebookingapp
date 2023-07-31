FROM python:3.10.11
ENV PYTHONUNBUFFERED 1
WORKDIR /moviebookingapp
COPY requirements.txt ./
RUN pip install -r requirements.txt