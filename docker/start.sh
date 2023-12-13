pip install --no-cache-dir --upgrade -r ../requirements.txt

python pre_start.py

python initial.py

python populate_test_data.py

uvicorn app:app --reload --host "0.0.0.0" --port 80