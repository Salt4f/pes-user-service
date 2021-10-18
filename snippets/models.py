from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


class User(models.Model):
    email = models.TextField(default = '' ,max_length = 30)
    password = models.TextField()
    nickName = models.TextField(default = '' ,max_length = 15)
    token = models.TextField(default = 'xxx')

    class Meta:
        ordering = ['id']   
