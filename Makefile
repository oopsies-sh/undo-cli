PACKAGE_NAME = undo_cli
VERSION = $(shell poetry version -s)
WHEEL_FILE = dist/$(PACKAGE_NAME)-$(VERSION)-py3-none-any.whl

.PHONY: build install

build:
	poetry build

install: build
	pipx install $(WHEEL_FILE) --force