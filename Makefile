.PHONY: setup ingest features train backtest brief evals test dashboard daily

PY := .venv/bin/python

setup:
	python3 -m venv .venv
	.venv/bin/pip install -q -e ".[dev]"

ingest:
	$(PY) -m dispatch.ingest.run --months 24

features:
	$(PY) -m dispatch.models.features

train:
	$(PY) -m dispatch.models.train

backtest:
	$(PY) -m dispatch.models.backtest

brief:
	$(PY) -m dispatch.analyst.brief

evals:
	$(PY) -m dispatch.analyst.evals

test:
	$(PY) -m pytest

dashboard:
	.venv/bin/streamlit run dashboard/app.py

daily: ingest brief
