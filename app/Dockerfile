FROM python:3.8.6

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r ./requirements.txt

EXPOSE 8000

COPY . /app

# ENTRYPOINT [ "./entrypoint.sh" ]