# -*- coding: utf-8 -*-
"""handlers.py: json_handler"""

import sys
import time

import datetime
import logging
import socket
import json

from collections import OrderedDict

import tzlocal

from json_handler.encoder import JSONLogEncoder

if sys.version_info > (3,):
    basestring = str
    long = int

__author__ = 'Steven Klass'
__date__ = '9/6/18 2:04 PM'
__copyright__ = 'Copyright 2011-2018 Pivotal Energy Solutions. All rights reserved.'
__credits__ = ['Steven Klass', ]

log = logging.getLogger(__name__)

DEFAULT_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

BUILT_IN_MAP = [

    ('asctime', 'timestamp'),

    ('levelname', 'level_name'),
    ('levelno', 'level_no'),

    ('name', 'name'),
    ('module', 'module'),
    ('funcName', 'function_name'),
    ('lineno', 'line_no'),

    ('msg', 'msg'),
    ('message', 'message'),
    ('args', 'args'),
    ('exc_text', 'exception_text'),
    ('exc_info', 'exception_info'),
    ('stack_info', 'stack_info'),

    ('thread', 'thread'),
    ('threadName', 'thread_name'),
    ('processName', 'process_name'),
    ('process', 'process'),

    ('filename', 'filename'),
    ('pathname', 'path'),

    # ('created', 'created'),
    ('relativeCreated', 'relative_created'),
    # ('msecs', 'msecs')
]

def parse_django_request(data):
    pass


class OrderedDictFormatter(logging.Formatter):
    """Used for formatting log records into a dict."""

    def __init__(self, fmt=None, datefmt=None, include_hostname=True, ensure_ascii=True, record_map=None):
        self.include_hostname = socket.gethostname() if include_hostname is True else False
        self.record_map = record_map if record_map else BUILT_IN_MAP
        self.ensure_ascii = ensure_ascii
        super(OrderedDictFormatter, self).__init__(fmt=fmt, datefmt=datefmt)

    def usesTime(self):
        return True

    def converter(self, timestamp):
        return datetime.datetime.fromtimestamp(timestamp, tzlocal.get_localzone())

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            s = ct.strftime(DEFAULT_TIME_FORMAT)
        return s




    #
    # def value_scrub(self, value):
    #
    #     if isinstance(value, (list, tuple)):
    #         return [self.value_scrub(v) for v in value]
    #     elif isinstance(value, dict):
    #         return {self.value_scrub(k): self.value_scrub(v) for k, v in value.items()}
    #     elif isinstance(value, basestring):
    #         return value if len(value) else None
    #     elif isinstance(value, (int, float, long, complex, bool)):
    #         return value
    #     else:
    #         return "{!r}".format(value)
    #
    # def collect_request(self, request):
    #
    #     data = OrderedDict()
    #     try:
    #         data['url'] = request.path
    #     except:
    #         pass
    #
    #     data['request'] = {}
    #     try:
    #         data['request']['GET'] = {k: v for k, v in self.value_scrub(request.GET).items() if v}
    #     except:
    #         pass
    #
    #     try:
    #         data['request']['POST'] = {k: v for k, v in self.value_scrub(request.POST).items() if v}
    #     except:
    #         pass
    #
    #     try:
    #         data['request']['COOKIES'] = {k: v for k, v in self.value_scrub(request.COOKIES).items() if v}
    #     except:
    #         pass
    #
    #     try:
    #         _meta_dict = request.META
    #         keys = sorted([k for k, v in _meta_dict.items()])
    #         meta = OrderedDict()
    #         for k in keys:
    #             meta[k] = cleanse_setting(k, self.value_scrub(_meta_dict[k]))
    #         data['request']['META'] = meta
    #     except:
    #         pass
    #
    #     try:
    #         data['user'] = request.user.username
    #         data['user_id'] = request.user.id
    #         data['user_email'] = request.user.email
    #         data['user_full_name'] = "{} {}".format(request.user.first_name, request.user.last_name)
    #     except AttributeError:
    #         pass
    #
    #     try:
    #         data['company'] = request.company.name
    #         data['company_id'] = request.company.id
    #     except AttributeError:
    #         pass
    #
    #     try:
    #         if request.is_impersonate:
    #             data['is_impersonate'] = request.is_impersonate
    #             data['impersonator'] = request.impersonator
    #     except AttributeError:
    #         pass
    #
    #     return data
    #
    # def collect_user_details(self, user_id):
    #
    #     data = OrderedDict()
    #     from .models import User
    #     user = User.objects.get(id=user_id)
    #     try:
    #         data['user_id'] = user_id
    #         data['user'] = user.username
    #         data['user_email'] = user.email
    #         data['user_full_name'] = "{} {}".format(user.first_name, user.last_name)
    #     except AttributeError:
    #         pass
    #
    #     try:
    #         data['company'] = user.company.name
    #         data['company_id'] = user.company.id
    #     except AttributeError:
    #         pass
    #     return data
    #

    def format(self, record):
        super(OrderedDictFormatter, self).format(record)
        ordered_record = [] if not self.include_hostname else [('hostname', self.include_hostname)]
        for original, new in self.record_map:
            ordered_record.append((new, record.__dict__.pop(original, None)))

        for key, value in record.__dict__.items():
            if key in ['created', 'msecs']:
                continue
            ordered_record.append((key, value))
        return OrderedDict(ordered_record)


class JSONFormatter(OrderedDictFormatter):
    """Formats messages as JSON."""

    def format(self, record):
        message_dict = super(JSONFormatter, self).format(record)
        return json.dumps(message_dict, sort_keys=False, ensure_ascii=self.ensure_ascii, default=JSONLogEncoder)
        # try:
        #     return json.dumps(message_dict, sort_keys=False, default=JSONLogEncoder)
        # except:
        #     return self.scrub(message_dict)
