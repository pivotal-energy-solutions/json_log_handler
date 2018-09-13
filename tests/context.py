# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json_handler

OrderedDictFormatter = json_handler.handlers.OrderedDictFormatter
JSONFormatter = json_handler.handlers.JSONFormatter


