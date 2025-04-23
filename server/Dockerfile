FROM python:3.11.5


WORKDIR ./
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
RUN pip install eventlet

EXPOSE 80
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:80", "--worker-class", "eventlet", "-w", "1", "app:app"]