# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from wtforms import validators
from jinja2 import Markup
from flask.ext.admin.contrib.sqla import ModelView
from studio.core.engines import db

from iefschina.models import SlideModel, ArticleModel
from .forms import CKTextAreaField


class Article(ModelView):

    create_template = 'panel/article_edit.html'
    edit_template = 'panel/article_edit.html'
    column_labels = {'id': 'ID',
                     'title': '标题',
                     'is_sticky': '置顶',
                     'channel': '频道',
                     'date_published': '发布时间',
                     'date_created': '创建时间'}
    column_list = ['id', 'channel', 'is_sticky', 'title',
                   'date_published', 'date_created']
    column_searchable_list = ['title', ]
    column_filters = ['id', 'channel.name']
    column_default_sort = ('date_published', True)
    form_extra_fields = {
        'content': CKTextAreaField('内容',
                                   validators=[validators.Required()]),
    }

    def __init__(self, **kwargs):
        super(Article, self).__init__(ArticleModel, db.session, **kwargs)

    def create_form(self, obj=None):
        form = super(Article, self).create_form()
        delattr(form, 'cid')
        delattr(form, 'date_created')
        return form

    def edit_form(self, obj=None):
        form = super(Article, self).edit_form(obj=obj)
        delattr(form, 'cid')
        delattr(form, 'date_created')
        return form


class Slide(ModelView):
    column_labels = {'id': 'ID',
                     'order': '排序',
                     'title': '标题',
                     'describe': '描述',
                     'image': '图片链接',
                     'link': '链接',
                     'date_created': '创建时间'}
    column_list = ['id', 'order', 'title', 'describe', 'image', 'link', 'date_created']
    column_default_sort = ('order', True)
    form_args = {
        'image': {'label': '图片', 'validators': [validators.Required(),
                                               validators.URL()]},
        'link': {'label': '链接', 'validators': [validators.Required(),
                                               validators.URL()]},
    }

    def _show_image(self, context, model, name):
        image = model.image.strip() if model.image else ''
        return Markup('<img src=%s width=200 height=200 />' % image)

    column_formatters = {
        'image': _show_image,
    }

    def __init__(self, **kwargs):
        super(Slide, self).__init__(SlideModel, db.session, **kwargs)

    def create_form(self, obj=None):
        form = super(Slide, self).create_form()
        delattr(form, 'date_created')
        return form

    def edit_form(self, obj=None):
        form = super(Slide, self).edit_form(obj=obj)
        delattr(form, 'date_created')
        return form