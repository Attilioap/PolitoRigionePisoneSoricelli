# ckbapp/admin.py

from django.contrib import admin
from .models import Student, Educator, Team, Tournament, Battle, BattleLeaderboard, TournamentLeaderboard, TeamLeaderboard, Invite
from django.contrib.auth.models import Group

from .forms import TournamentAdminForm

# Create Educator group
educator_group, created = Group.objects.get_or_create(name='Educators')

# Create Student group
student_group, created = Group.objects.get_or_create(name='Students')


admin.site.register(Student)
admin.site.register(Educator)
admin.site.register(Team)

admin.site.register(Battle)
admin.site.register(Invite)
admin.site.register(BattleLeaderboard)
admin.site.register(TeamLeaderboard)
admin.site.register(TournamentLeaderboard)

class TournamentAdmin(admin.ModelAdmin):
    form = TournamentAdminForm
    list_display = ('name', 'registrationDeadline', 'endingDate', 'description')
    filter_horizontal = ('students',)

admin.site.register(Tournament, TournamentAdmin)