# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2015 CERN.
#
# INSPIRE is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

from wtforms import validators

from invenio.base.i18n import _
from invenio_deposit import fields
from invenio_deposit.form import WebDepositForm
from invenio_deposit.field_widgets import ColumnInput, \
    ExtendedListWidget, \
    ItemWidget


class AuthorInlineForm(WebDepositForm):

    """Author inline form."""

    name = fields.TextField(
        widget_classes='form-control',
        widget=ColumnInput(
            class_="col-xs-6", description="Family name, First name"),
    )
    affiliation = fields.TextField(
        autocomplete='affiliation',
        placeholder='Start typing for suggestions',
        autocomplete_limit=5,
        widget_classes='form-control',
        widget=ColumnInput(
            class_="col-xs-4 col-pad-0", description="Affiliation"),
    )


class DemoForm(WebDepositForm):

    """Demo form fields."""

    template = 'deposit/demo.html'

    title = fields.TitleField(
        label=_('Title'),
        widget_classes="form-control",
        validators=[validators.DataRequired()],
    )

    authors = fields.DynamicFieldList(
        fields.FormField(
            AuthorInlineForm,
            widget=ExtendedListWidget(
                item_widget=ItemWidget(),
                html_tag='div',
            ),
        ),
        label='Authors',
        add_label='Add another author',
        min_entries=1,
        widget_classes='',
    )

    collaboration = fields.TextField(
        label=_('Collaboration'),
        widget_classes="form-control"
    )

    experiment = fields.TextField(
        placeholder=_("Start typing for suggestions"),
        label=_('Experiment'),
        widget_classes="form-control",
    )

    abstract = fields.TextAreaField(
        label=_('Abstract'),
        default='',
        widget_classes="form-control",
    )

    #
    # Form Configuration
    #
    _title = _("My demo submission")

    # Group fields in categories

    groups = [
        ('Basic Information',
            ['title', 'authors', 'collaboration', 'experiment']),
        ('Other Information',
            ['abstract'])]
