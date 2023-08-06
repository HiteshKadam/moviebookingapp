FROM python:3.10.11
ENV PYTHONUNBUFFERED 1
WORKDIR /moviebookingapp
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY . .
CMD gunicorn moviebookingapp.wsgi:application --bind 0.0.0.0:8000
EXPOSE 8000