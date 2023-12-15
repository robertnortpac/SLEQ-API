pip install --no-cache-dir --upgrade -r requirements-freeze.txt

python pre_start.py

python initial.py

python populate_test_data.py

pytest --disable-warnings

uvicorn app.main:app --reload --host "0.0.0.0" --port 80