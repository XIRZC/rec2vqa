FROM python:3.8.15-alpine3.16

RUN apk --update add gcc linux-headers musl-dev
WORKDIR /work
COPY requirements.txt ./
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py makemigrations api
RUN python manage.py migrate

EXPOSE 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
