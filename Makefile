run-gunicorn:
	gunicorn api.fast:app -w 4 -k uvicorn.workers.UvicornWorker

run-uvicorn:
	uvicorn api.fast:app --reload
