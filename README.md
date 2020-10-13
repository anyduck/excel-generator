# Генератор ексельок😁

### Використано
* [Python 3.6+](https://www.python.org)
* [FastAPI](https://fastapi.tiangolo.com)
* [Docker](https://www.docker.com)
* [Skeleton CSS](http://getskeleton.com)


### Установка


1. Клонуйте репозиторій
```sh
git clone https://github.com/moodduckk/excel-generator.git
```
2. Зберіть образ
```sh
docker build -t excel-generator ./excel-generator/
```
4. Запустіть контейнер
```sh
docker run -d --name excel-generator -p 8000:80 excel-generator
```
5. Відкрийте в браузері [127.0.0.1:8000](http://127.0.0.1:8000)
