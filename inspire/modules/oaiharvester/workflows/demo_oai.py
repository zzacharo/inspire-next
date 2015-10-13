

from invenio_workflows.tasks.logic_tasks import (
    workflow_if,
    workflow_else,
)

from invenio_oaiharvester.tasks.records import convert_record_to_json

from inspire.modules.converter.tasks import convert_record
from invenio_records.api import Record


def halt_for_approval(obj, eng):
    eng.halt(action="demo_approval", msg="This is a demo approval")


def was_approved(obj, eng):
    if obj.extra_data.get('approved'):
        return True
    return False


def create_record(obj, eng):
    Record.create(obj.data)


class demo_oai(object):

    object_type = "arXiv"

    workflow = [
        convert_record("oaiarXiv2inspire_nofilter.xsl"),
        convert_record_to_json,
        halt_for_approval,
        workflow_if(was_approved),
        [
            create_record,
        ],
    ]

    @staticmethod
    def get_title(obj, *args, **kwargs):
        if isinstance(obj.data, str):
            return "No title found"
        try:
            record = Record(obj.data)
        except Exception as err:
            return "Error occured: {0}".format(err)

        return record.get('titles.title', ['No title'])[0]

    @staticmethod
    def get_description(obj, *args, **kwargs):
        return "Some description."

    @staticmethod
    def formatter(obj, *args, **kwargs):
        return "The whole record"

    @staticmethod
    def get_additional(obj, *args, **kwargs):
        return "Additional data"

    @staticmethod
    def get_sort_data(obj, *args, **kwargs):
        return {}

    @classmethod
    def get_record(cls, obj, **kwargs):
        if isinstance(obj.data, str):
            return {}
        return obj.data
