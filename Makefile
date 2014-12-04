#!/usr/bin/make
PYTHON := /usr/bin/env python

lint:
	@flake8 --exclude hooks/charmhelpers hooks
	@flake8 --exclude hooks/charmhelpers unit_tests
	@charm proof

test:
	@echo Starting tests...
	@$(PYTHON) /usr/bin/nosetests --nologcapture unit_tests

publish: lint test
	bzr push lp:charms/neutron-openvswitch
	bzr push lp:charms/trusty/neutron-openvswitch
