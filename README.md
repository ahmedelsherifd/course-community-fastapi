## Clone repo

```
git clone https://github.com/ahmedelsherifd/course-community-fastapi6
```

## Install backend

```
cd course-community-fastapi6
python -m venv venv
# activate venv in linux
source venv/bin/activate
# install requirements
pip install requirements.txt
# migrate database
alembic upgrade head
# run server
uvicorn app.main:app --reload
```
