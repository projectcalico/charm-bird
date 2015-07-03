#!/usr/bin/make
PYTHON := /usr/bin/env python

.venv:
	sudo apt-get install -y python-virtualenv
	virtualenv .venv
	.venv/bin/pip install nose flake8 six pyyaml mock netaddr netifaces

lint: .venv
	@.venv/bin/flake8 --exclude hooks/charmhelpers hooks
	@.venv/bin/flake8 --exclude hooks/charmhelpers unit_tests
	@charm proof

test: .venv
	@echo Starting tests...
	@.venv/bin/nosetests --nologcapture unit_tests

bin/charm_helpers_sync.py:
	@mkdir -p bin
	@bzr cat lp:charm-helpers/tools/charm_helpers_sync/charm_helpers_sync.py \
		> bin/charm_helpers_sync.py

sync: bin/charm_helpers_sync.py
	@$(PYTHON) bin/charm_helpers_sync.py -c charm-helpers-sync.yaml

