run-gunicorn:
	gunicorn api.fast:app -w 2 -k uvicorn.workers.UvicornWorker

run-uvicorn:
	uvicorn api.fast:app --reload
