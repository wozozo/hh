# coding: utf-8

import datetime
import mimetypes
import os
import string
import time
import random
from hashlib import sha1
import urllib2

# from boto.s3.connection import S3Connection
# from boto.s3.key import Key

def _sha1(chars):
    return sha1(chars).hexdigest()

sets = string.digits + string.letters
def random_string(n, sets=sets):
    random.seed()
    return ''.join(random.choice(sets) for i in range(n))

def timebased_rename(file, addpath=None):
    today = datetime.datetime.today()
    date = '%d%02d%02d' % (today.year, today.month, today.day)
    ext = os.path.splitext(file.name)[1]
    ext = ext.lower()
    filename = '%s%i_%s%s' % (date, time.time(), random_string(10), ext)

    if addpath is not None:
        filename = os.path.join(addpath, filename)

    return filename

def _buildquery(params, encoding):
    data = []
    for k, v in params.iteritems():
        if isinstance(k, unicode): k = k.encode(encoding)
        if isinstance(v, unicode): v = v.encode(encoding)
        k = str(k)
        v = str(v)
        data.append('%s=%s' % (urllib2.quote(k), urllib2.quote(v)))
    return '&'.join(data)

def image_middle(model):
    """
    middle size
    """

    return _image_resize_path(model, 400)

def image_small(model):
    """
    small size
    """
    return _image_resize_path(model, 200)

def _image_resize_path(model, size):
    path, ext = os.path.splitext(str(model))
    return '%s_%sx%s%s' % (path, size, size, ext)

def split_path_ext(image):
    return os.path.splitext(str(image))

def detect_imagetype(image):
    header = image.read(10)
    image.seek(0)

    if header[6:10] == 'JFIF': return '.jpeg'
    if header[0:3] == 'GIF': return '.gif'
    if header[1:4] == 'PNG': return '.png'

    return False

def detect_imageformat(image):
    fmt = image.format

    if fmt == 'JPEG': return 'jpg'
    if fmt == 'GIF': return 'gif'
    if fmt == 'PNG': return 'png'

    return fmt.lower()

def splitquery(params):
    """
    >>> a='/word:hoge+piyo/item:macbook/color:red'
    >>> [{x[0]: x[1].split('+')} for x in [x.split(':') for x in a[1:].split('/')]]
        [{'word': ['hoge', 'piyo']}, {'item': ['macbook']}, {'color': ['red']}]
    """

    queries = {}
    for param in params[1:].split('/'):
        p = param.split(':')
        queries[p[0]] = [s for s in p[1].split('+') if s.strip() != '']
    return queries

def store_in_s3(filename, content):
    from django.conf import settings
    from boto.s3.connection import S3Connection
    from boto.s3.key import Key

    conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    bucket = conn.lookup(settings.AWS_STORAGE_BUCKET_NAME)
    # TODO guess ext
    mime = mimetypes.guess_type(filename)[0]
    k = Key(bucket)
    k.key = filename
    k.set_metadata("Content-Type", mime)
    k.set_contents_from_file(content.file)
    k.set_acl("public-read")

    url = 'http://%s.s3.amazonaws.com/%s' % (settings.AWS_STORAGE_BUCKET_NAME, filename)

    return url
