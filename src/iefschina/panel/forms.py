# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from wtforms.widgets import TextArea
from wtforms import TextAreaField


class CKTextAreaWidget(TextArea):

    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):

    widget = CKTextAreaWidget()