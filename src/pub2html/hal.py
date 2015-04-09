"""
Provide access to hal.archives-ouvertes.fr
"""

__author__ = 'Julien Diener'

from urllib2 import urlopen
import json
import traceback
from os.path import splitext

from . import Publication

_image_ext = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}


class Query(object):
    _base_url = "http://api.archives-ouvertes.fr/search/?q="
    _title_field = 'title_s'
    _authors_field = 'authFullName_s'
    _url_field = "uri_s"
    _files = "files_s"
    _annexes = "fileAnnexes_s"

    _fields = '&fl=' + ','.join([_authors_field, _title_field, _url_field, _files, _annexes])

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
                title   = ' '.join(doc[self._title_field])
                url     = doc[self._url_field]

                pdf   = None
                files = doc[self._files]
                for f in files:
                    if splitext(f)[-1].lower() == '.pdf':
                        pdf = f
                        break

                thumbnail = None
                annexes = doc[self._annexes]
                for annex in annexes:
                    if splitext(annex) in _image_ext:
                        thumbnail = annex
                        break

                publication = Publication(authors=authors, title=title, url=url,
                                          pdf=pdf, thumbnail=thumbnail)
                publications.append(publication)

            return publications

        except Exception:
            self._errors = traceback.format_exc()
            return None