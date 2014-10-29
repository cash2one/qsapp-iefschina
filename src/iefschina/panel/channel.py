# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from wtforms import validators
from jinja2 import Markup
from flask.ext.admin.contrib.sqla import ModelView
from studio.core.engines import db
from iefschina.models import NaviModel, ChannelModel

from .forms import CKTextAreaField


class Navi(ModelView):

    column_labels = {'name': '名称', 'channels': '频道列表'}
    column_list = ['id', 'name', 'channels', 'date_created']

    def _list_channels(self, context, model, name):
        lis = ''
        for channel in model.channels:
            lis += '<li>%s</li>' % (channel)
        return Markup('<ol>' + lis + '</ol>')

    column_formatters = {
        'channels': _list_channels,
    }

    def __init__(self, **kwargs):
        super(Navi, self).__init__(NaviModel, db.session, **kwargs)

    def create_form(self, obj=None):
        form = super(Navi, self).create_form()
        delattr(form, 'date_created')
        return form

    def edit_form(self, obj=None):
        form = super(Navi, self).edit_form(obj=obj)
        delattr(form, 'date_created')
        return form


class Channel(ModelView):

    create_template = 'panel/channel_edit.html'
    edit_template = 'panel/channel_edit.html'
    column_labels = {'name': '名称',
                     'parent': '主分类(本身为主分类，不填写)',
                     'summary': '简介',
                     'date_created': '创建时间'}
    column_searchable_list = ['name', ]
    column_default_sort = ('date_created', True)
    form_extra_fields = {
        'summary': CKTextAreaField('简介',
                                   validators=[validators.Required()]),
    }

    def __init__(self, **kwargs):
        super(Channel, self).__init__(ChannelModel, db.session, **kwargs)

    def create_form(self, obj=None):
        form = super(Channel, self).create_form()
        delattr(form, 'articles')
        delattr(form, 'channels')
        delattr(form, 'all_articles')
        delattr(form, 'date_created')
        return form

    def edit_form(self, obj=None):
        form = super(Channel, self).edit_form(obj=obj)
        delattr(form, 'articles')
        delattr(form, 'channels')
        delattr(form, 'all_articles')
        delattr(form, 'date_created')
        return form