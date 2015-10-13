# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2014, 2015 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

from flask import current_app


from invenio_deposit.types import SimpleRecordDeposition
from invenio_deposit.tasks import dump_record_sip, \
    prepare_sip, process_sip_metadata, \
    render_form
from invenio_workflows.tasks.workflows_tasks import log_info

from inspire.utils.helpers import get_record_from_model

from ..demo_form import DemoForm


class demo(SimpleRecordDeposition):

    """Simple demo submission for Invenio User Workshop."""

    workflow = [
        # Render form and wait for user to submit
        render_form(draft_id='default'),
        # Create the submission information package by merging form data
        # from all drafts (in this case only one draft exists).
        prepare_sip(),
        # Dump unmodified SIP
        dump_record_sip(),
        # Process metadata to match your JSONAlchemy record model. This will
        # call process_sip_metadata() on your subclass.
        process_sip_metadata(),
        # Print success message.
        log_info('Hello World! The workflow finished successfully.')
    ]

    name = "Demo deposition"
    name_plural = "Demo depositions"
    group = "Invenio User Workshop"
    draft_definitions = {
        'default': DemoForm,
    }

    @classmethod
    def get_record(cls, obj, **kwargs):
        """Return a dictionary-like object representing the current object.

        This object will be used for indexing and be the basis for display
        in Holding Pen.
        """
        try:
            model = cls.model(obj)
            return get_record_from_model(model).dumps()  # Turn into pure dict
        except Exception as err:
            current_app.logger.exception(err)
            return {}
