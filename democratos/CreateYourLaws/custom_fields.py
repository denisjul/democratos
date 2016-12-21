# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models


class TableField(models.TextField):
    # __metaclass__ = models.SubfieldBase
    description = """Stores a python Table/Array (list of list (of list...)).
    Work for simple list of course."""

    def __init__(self, *args, **kwargs):
        super(TableField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return []
        nb_lignes = value.count("[")
        if nb_lignes <= 1:
            valpy = value.split(",")
            for x in range(len(valpy)):
                valpy[x] = valpy[x].replace('[', "")
                valpy[x] = valpy[x].replace(']', "")
                try:
                    valpy[x] = float(valpy[x])
                    try:
                        valpy[x] = int(valpy[x])
                    except:
                        pass
                except:
                    pass
        else:
            i = 0
            while value[i] != "[":
                i += 1
            i += 1
            valpy, i = self.get_dat_list(value, i)
        return valpy

    def get_dat_list(self, text, i):
        valpy = []
        contents = ""
        while text[i] != "]":
            if text[i] == "[":
                i += 1
                newlist, i = self.get_dat_list(text, i)
                valpy.append(newlist)
            try:
                a = text[i + 1]
            except:
                break
            contents += text[i]
            i += 1
        if valpy == []:
            valpy = contents.split(",")
            for x in range(len(valpy)):
                valpy[x] = valpy[x].replace("[", "")
                valpy[x] = valpy[x].replace("]", "")
                try:
                    valpy[x] = float(valpy[x])
                    try:
                        valpy[x] = int(valpy[x])
                    except:
                        pass
                except:
                    pass
        return valpy, i

    def get_prep_value(self, value):
        return value

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class TableModel(models.Model):
    test_list = TableField()