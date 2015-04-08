"""
Provide access to hal.archives-ouvertes.fr
"""

__author__ = 'Julien Diener'

from urllib2 import urlopen
import json
import traceback

from . import Publication


class Query(object):
    _base_url = "http://api.archives-ouvertes.fr/search/?q="
    _title_field = 'title_s'
    _authors_field = 'authFullName_s'
    _url_field = "uri_s"
    _fields = '&fl=' + ','.join([_authors_field, _title_field, _url_field])

    def __init__(self, authors):
        self.authors = authors
        self._errors = []

    @classmethod
    def _authors_search(cls, base_url, names):
        names = names.replace(" ", "%20")
        return base_url + "authFullName_t:" + '"' + names + '"' + cls._fields

    def query(self):
        url = self._authors_search(self._base_url, self.authors)

        try:
            hal_json = json.load(urlopen(url))
        except TypeError:
            self._errors.append("Invalid json? \n\n" + urlopen(url).read())
            return None

        publications = []
        try:
            pub_json = hal_json['response']['docs']
            for doc in pub_json:
                authors = doc[self._authors_field]
                title = ' '.join(doc[self._title_field])
                url = doc[self._url_field]
                publication = Publication(authors=authors, title=title, url=url)
                publications.append(publication)

            return publications

        except Exception:
            self._errors = traceback.format_exc()
            return None