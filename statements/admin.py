from django.contrib import admin

from .models import CommerzbankStatement, StatementCategory, StatementKeyword

admin.site.register(CommerzbankStatement)
admin.site.register(StatementCategory)
admin.site.register(StatementKeyword)
