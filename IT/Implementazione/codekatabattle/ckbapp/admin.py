# ckbapp/admin.py

from django.contrib import admin
from .models import User, Student, Educator, Team, Tournament, Battle

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Educator)
admin.site.register(Team)
admin.site.register(Tournament)
admin.site.register(Battle)
