# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014, 2015 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""Approval action for INSPIRE arXiv harvesting."""

from flask import request

from inspire.modules.workflows.actions.core_approval import core_approval


class demo_approval(core_approval):

    """Class representing the approval action."""

    def resolve(self, bwo):
        """Resolve the action taken in the approval action."""
        bwo.remove_action()
        extra_data = bwo.get_extra_data()

        value = request.form.get("value", None)
        extra_data["approved"] = value in ('accept', 'accept_core')

        bwo.set_extra_data(extra_data)
        bwo.save()

        bwo.continue_workflow(delayed=True)

        if extra_data["approved"]:
            return {
                "message": "Suggestion has been accepted!",
                "category": "success",
            }
        else:
            return {
                "message": "Suggestion has been rejected",
                "category": "warning",
            }
