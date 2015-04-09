"""
Base of package publication
"""

__author__ = 'Julien Diener'


class Publication(object):
    """ Represents one publication """

    def __init__(self, authors, title, url=None, abstract=None, pdf=None, thumbnail=None):
        self.authors = authors
        self.title = title
        self.url = url
        self.abstract = abstract
        self.pdf = pdf
        self.thumbnail = thumbnail


def pub2html(authors, template_text=None, query_class=None):
    from . import template

    if template_text is None:
        template_text = template.default

    if query_class is None:
        from .hal import Query as query_class

    temp = template.make_template(template_text)

    publications = query_class(authors=authors).query()

    return temp.render(publications=publications)