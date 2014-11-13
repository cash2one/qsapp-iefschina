# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from jinja2 import Markup
from flask import url_for
from studio.core.engines import db
from sqlalchemy.ext.hybrid import hybrid_property

from iefschina.models.article import ArticleModel
#from iefschina.contrib.helpers import REGEX
REGEX = r'^[a-zA-Z\b]+'

__all__ = [
    'NaviChannelModel',
    'ChannelModel',
    'ChannelSummaryModel',
    'NaviModel',
]


def articles_order_by():
    return [db.desc(ArticleModel.is_sticky),
            db.desc(ArticleModel.date_published)]


class NaviChannelModel(db.Model):
    __tablename__ = 'navi_channel'

    navi_id = db.Column(db.Integer(), db.ForeignKey('navi.id'),
                        primary_key=True, index=True)
    channel_id = db.Column(db.Integer(), db.ForeignKey('channel.id'),
                           primary_key=True, index=True)


class ChannelModel(db.Model):

    __tablename__ = 'channel'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    parent_id = db.Column(db.Integer(),
                          db.ForeignKey('channel.id'),
                          index=True)
    name = db.Column(db.Unicode(256), nullable=False, unique=True, index=True)
    date_created = db.Column(db.DateTime(timezone=True),
                             nullable=False, index=True,
                             server_default=db.func.current_timestamp())

    _summary = db.relationship(
            'ChannelSummaryModel',
            backref=db.backref('channel', lazy='joined', innerjoin=True),
            primaryjoin='ChannelModel.id==ChannelSummaryModel.id',
            foreign_keys='[ChannelSummaryModel.id]',
            uselist=False, cascade='all, delete-orphan')

    @hybrid_property
    def summary(self):
        return self._summary.content

    @summary.setter
    def summary_setter(self, value):
        if not self._summary:
            self._summary = ChannelSummaryModel(id=self.id, content=value)
        self._summary.content = value

    @property
    def html(self):
        return Markup(self.summary)

    parent = db.relationship('ChannelModel',
                             remote_side=[id],
                             backref='channels')
    articles = db.relationship(
        'ArticleModel',
        primaryjoin='and_(ChannelModel.id==ArticleModel.cid,'
                    'ArticleModel.date_published<=func.now())',
        order_by=articles_order_by,
        foreign_keys='[ArticleModel.cid]',
        passive_deletes='all', lazy='dynamic')

    all_articles = db.relationship(
        'ArticleModel',
        primaryjoin='ChannelModel.id==ArticleModel.cid',
        order_by=articles_order_by,
        foreign_keys='[ArticleModel.cid]',
        backref=db.backref(
            'channel', lazy='subquery', innerjoin=True),
        passive_deletes='all', lazy='dynamic')

    @property
    def language(self):
        c = re.compile(REGEX)
        if c.match(self.name.strip()):
            return 'en'
        else:
            return 'cn'

    @property
    def url(self):
        return url_for("views.channel", cid=self.id)

    @classmethod
    def get_channel_query(cls, language='all'):
        query = cls.query
        if language == 'cn':
            query = query.filter("name !~ '%s'" % REGEX)
        elif language == 'en':
            query = cls.query.filter("name ~ '%s'" % REGEX)

        return query

    def __str__(self):
        return self.name


class ChannelSummaryModel(db.Model):
    __tablename__ = 'channel_summary'

    id = db.Column(db.Integer(), db.ForeignKey('channel.id'),
                        nullable=False, primary_key=True)
    content = db.Column(db.UnicodeText(), nullable=False)


class NaviModel(db.Model):
    __tablename__ = 'navi'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    name = db.Column(db.Unicode(256), nullable=False, unique=True, index=True)
    date_created = db.Column(db.DateTime(timezone=True),
                             nullable=False, index=True,
                             server_default=db.func.current_timestamp())

    channels = db.relationship('ChannelModel',
                               secondary=NaviChannelModel.__table__)

    def __str__(self):
        return self.name
