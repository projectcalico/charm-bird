#!/usr/bin/python

from charmhelpers.core.services.base import ServiceManager
from charmhelpers.core.services import helpers

import actions
import relations


def manage():
    manager = ServiceManager([
        {
            'service': 'bird',
            'ports': [9905, 9906],
            'provided_data': [
                relations.BgpRRRelation(),
            ],
            'required_data': [
                relations.BgpRRRelation(),
            ],
            'data_ready': [
                helpers.render_template(
                    source='bird.conf',
                    target='/etc/bird/bird.conf'),
                actions.log_start,
            ],
        },
    ])
    manager.manage()
