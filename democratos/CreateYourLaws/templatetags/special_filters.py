# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import template
from importlib import import_module

register = template.Library()


@register.filter
def lookup(d, key):
    return d[key]


@register.filter
def isinst(value, class_str):
    split = class_str.split('.')
    return isinstance(value,
                      getattr(import_module('.'.join(split[:-1])), split[-1]))
