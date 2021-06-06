# :page_facing_up: drf-api-sandbox

<br>

## :pushpin: Overview

- Frontend 학습할 때 Backend와 API 통신을 실습하기 위해 직접 만든 API입니다.

<br>

## :pushpin: Tech Stack

- Language : `Python 3.7.4`
- Framework : `Django 3.2.4`, `Django Rest Framework 3.12.4`
- Database : `sqlite3`
- OS : `Windows10 Home`

<br>

## :pushpin: Getting Started

- 아래 명령어를 입력하기 전 `Python 3.7.4`와 `sqlite3`를 반드시 설치해주세요.

- Clone to Repository

```bash
git clone https://github.com/wally-wally/drf-api-sandbox.git
cd drf-api-sandbox
```

- Run Virtual Environment

```bash
python -m venv venv
source venv/Scripts/activate
```

- Install Packages

```bash
pip install -r requirements.txt
```

- Migrate Database

```bash
python manage.py migrate
```

- Load Dump Data

```bash
python manage.py loaddata todos/dummy.json
```

- Run to Server at local

```bash
python manage.py runserver
```

- `http://127.0.0.1:8000/api/v1/todos/`에 접속해서 아래와 같이 나오면 성공

![todo](https://user-images.githubusercontent.com/52685250/120889336-89a93200-c637-11eb-9584-f3b5e629011c.PNG)

<br>

## :pushpin: API Documentation

> 로컬에서 서버를 구동한 후 접속해서 확인할 수 있습니다.

- swagger 문서 : `http://127.0.0.1:8000/api/v1/swagger/`
- redocs 문서 : `http://127.0.0.1:8000/api/v1/redocs/`