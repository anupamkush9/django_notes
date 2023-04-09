FROM python:3.8
RUN pip install --upgrade pip
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

RUN mkdir /backend_api
WORKDIR /backend_api
COPY . /backend_api/
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]


# command for creating docker image
# docker build .t backend_api:v1
# docker build .t <image_id>

# command for running docker image
# docker run -p 8000:8000 <image_id>
# docker run -p 8000:8000 -v .:/backend_api <image_id>

