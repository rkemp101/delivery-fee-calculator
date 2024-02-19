setup:
	pip install -r requirements.txt

run_api_local:
	uvicorn api.fast:app --reload

test_utils:
	pytest tests/utils_test.py -v --color=yes

test_api:
	pytest tests/fast_test.py -v --color=yes
