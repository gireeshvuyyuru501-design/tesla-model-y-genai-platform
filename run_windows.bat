python -m venv .venv
call .venv\Scripts\activate
python -m pip install -r requirements.txt
uvicorn src.main:app --reload
