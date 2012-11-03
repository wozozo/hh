# coding: utf-8

from django import forms

from s3 import S3
from utils.text import timebased_rename


class UserForm(forms.Form):

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)


class UserModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if kwargs.has_key('initial') and kwargs['initial'].get('user'):
            self.user = kwargs['initial']['user']
        super(UserModelForm, self).__init__(*args, **kwargs)


class S3Form(forms.Form):

    def __init__(self, *args, **kwargs):
        self.s3 = S3()
        super(S3Form, self).__init__(*args, **kwargs)


class UploadForm(S3Form):
    photo = forms.ImageField()

    def __init__(self, *args, **kwargs):

        # Unit of `limit` is MB (default 12MB)
        if kwargs.has_key('limit'):
            limit = kwargs['limit']
        else:
            limit = 12

        self.limit = 1000 * 1024 * limit

        super(UploadForm, self).__init__(*args, **kwargs)

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo.size > self.limit:
            raise forms.ValidationError('写真のサイズは %sMB までです。' % self.limit)
        return self.cleaned_data['photo']

    def save(self):
        photo = self.cleaned_data['photo']
        filename = timebased_rename(photo)
        filepath = 'tmp/' + filename
        url = self.s3.store(filepath, photo)

        dataset = {'url': url, 'filename': filename, 'filepath': filepath}
        return dataset


