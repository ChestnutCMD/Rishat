FROM python:3.10

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY /TestTask .

ENTRYPOINT ["bash", "entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:7000"]
EXPOSE 7000