.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: rundesk
rundesk:
	python main.py

.PHONY: runweb
runweb:
	python web.py

.PHONY: build
build:
	python build.py