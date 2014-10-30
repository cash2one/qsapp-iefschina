#! -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re
from flask import url_for
from jinja2 import Markup
from sqlalchemy import sql
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.hybrid import hybrid_property

from studio.core.engines import db
#from iefschina.contrib.helpers import REGEX
REGEX = r'[a-zA-Z\b]+'

__all__ = [
    'SlideModel',
    'ArticleModel',
    'ArticleContentModel',
]


class SlideModel(db.Model):
    __tablename__ = 'slide'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    title = db.Column(db.Unicode(256), nullable=True, index=True)
    describe = db.Column(db.Unicode(1024), nullable=True, index=True)
    order = db.Column(db.Integer(), nullable=False, index=True)
    image = db.Column(db.Unicode(length=2083), nullable=False)
    link = db.Column(db.Unicode(length=2083), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True),
                             nullable=False, index=True,
                             server_default=db.func.current_timestamp())


class ArticleModel(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    cid = db.Column('channel_id', db.Integer(), nullable=False, index=True)
    is_sticky = db.Column(db.Boolean(), nullable=False,
                                        server_default=sql.false())
    title = db.Column(db.Unicode(64), nullable=False, unique=True, index=True)

    date_published = db.Column(db.DateTime(timezone=True),
                               nullable=False, index=True,
                                server_default=db.func.current_timestamp())
    date_created = db.Column(db.DateTime(timezone=True),
                             nullable=False, index=True,
                             server_default=db.func.current_timestamp())

    _content = db.relationship(
            'ArticleContentModel',
            backref=db.backref('article', lazy='joined', innerjoin=True),
            primaryjoin='ArticleModel.id==ArticleContentModel.id',
            foreign_keys='[ArticleContentModel.id]',
            uselist=False, cascade='all, delete-orphan')

    @property
    def language(self):
        c = re.compile(REGEX)
        if c.match(self.title):
            return 'en'
        else:
            return 'cn'

    @property
    def url(self):
        return url_for('views.article', aid=self.id)

    @hybrid_property
    def content(self):
        return self._content.content

    @content.setter
    def content_setter(self, value):
        if not self._content:
            self._content = ArticleContentModel(id=self.id, content=value)
        self._content.content = value

    @property
    def html(self):
        return Markup(self.content)

    @classmethod
    def get_article_query(cls, cids=[], limit=10):
        query = (cls.query
                    .filter(cls.cid.in_(cids))
                    .filter(cls.date_published<=func.now())
                    .order_by(ArticleModel.date_published.desc())
                    .limit(limit))

        return query

    def __str__(self):
        return self.title


class ArticleContentModel(db.Model):
    __tablename__ = 'article_content'

    id = db.Column(db.Integer(), db.ForeignKey('article.id'),
                        nullable=False, primary_key=True)
    content = db.Column(db.UnicodeText(), nullable=False)
