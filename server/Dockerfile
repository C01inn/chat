FROM python:latest


WORKDIR /var/www/
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
RUN ls
EXPOSE 80
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:80", "--worker-class", "eventlet", "-w", "1", "app:app"]