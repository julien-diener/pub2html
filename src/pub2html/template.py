__author__ = 'juh'

import jinja2

default = """
<div id="publications">

  {%- for pub in publications %}
    <p> <a href="{{ pub.url }}"> {{ pub.title }}, {{ pub.authors }} </a> </p>
  {%- endfor %}

</div>  <!-- publications -->
"""


def make_template(template_text):
    return jinja2.Template(template_text)