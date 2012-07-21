# coding: utf-8

import mimetypes

from django.conf import settings

from boto.s3.connection import S3Connection
from boto.s3.key import Key


class S3(object):

    def __init__(self):
        self.conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        self.bucket = self.conn.lookup(settings.AWS_STORAGE_BUCKET_NAME)
        self.key = Key(self.bucket)

    def get_mimetype(self, filename):
        return mimetypes.guess_type(filename)[0]

    def store(self, filename, content):
        # TODO guess ext
        mime = self.get_mimetype(filename)
        self.key.key = filename
        self.key.set_metadata("Content-Type", mime)
        self.key.set_contents_from_file(content.file)
        self.key.set_acl("public-read")
        # k.make_public()

        url = 'http://%s.s3.amazonaws.com/%s' % (settings.AWS_STORAGE_BUCKET_NAME, filename)

        return url

    def publish(self, filename, date):
        mime = self.get_mimetype(filename)
        metadata = {'Content-Type': mime}

        self.key.key = filename

        if filename.startswith('tmp/'):
            filename = filename.lstrip('tmp/')
        date = '{year}{month:02d}{day:02d}'.format(year=date.year, month=date.month, day=date.day)
        dst_key = 'photos/{date}/{filename}'.format(date=date, filename=filename)

        self.key.copy(self.bucket.name, dst_key, metadata=metadata)

        return dst_key
