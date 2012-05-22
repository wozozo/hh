# coding: utf-8

import datetime
import os
import random

from django.core.files.storage import FileSystemStorage


class DateTimeFileSystemStorage(FileSystemStorage):
    def get_valid_name(self, name):
        fn, ext = os.path.splitext(name)

        d = datetime.datetime.today()
        date = '%s%s%s' % (d.year, d.month, d.day)
        # TODO detect_imageformat
        return date + str(random.randint(10000, 99999)) + (ext or '')


class UserFileSystemStorage(FileSystemStorage):
    def get_valid_name(self, name):
        return name
