run-gunicorn:
	gunicorn api.fast:app -w 2 -k uvicorn.workers.UvicornWorker

run-uvicorn:
	uvicorn api.fast:app --reload

test-prep:
	mv data/2022 data/2022-real
	mkdir data/2022
	echo "Make sure to set export TESTING=1"

test-end:
	export TESTING=0
	rm -rf data/2022
	mv data/2022-real data/2022
	echo "Make sure to set export TESTING=''"
