FROM python:3-alpine
WORKDIR /usr/src/app
EXPOSE 5080
COPY requirements.txt .
RUN pip install -qr requirements.txt
COPY app .
CMD [ "python", "./app.py" ]