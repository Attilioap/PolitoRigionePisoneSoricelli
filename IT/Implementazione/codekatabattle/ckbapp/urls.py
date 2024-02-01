from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import educator_dash, signup, user_login, student_dash, tournament_managment, tournament_status_page_educator, battle_status_page, tournament_status_page_student, battle_status_student, tournament_info
from ckbapp.views import GitHubWebhookView

urlpatterns = [
    path('educator_dashboard/', educator_dash, name='educator_dash'),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name ='login'),
    path('student_dashboard/', student_dash, name ='student_dash'),
    path('tournament_managment/<int:tournament_id>/', tournament_managment, name='tournament_managment'),
    path('tournament_status_page_educator/<int:tournament_id>/', tournament_status_page_educator, name='tournament_status_page_educator'),
    path('battle/<int:battle_id>/', battle_status_page, name='battle_status_page'),
    path('tournament/<int:tournament_id>/status/', tournament_status_page_student, name='tournament_status_page_student'),
    path('battle_status_student/<int:battle_id>/', battle_status_student, name='battle_status_student'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('tournament/<int:tournament_id>/info/', tournament_info, name='tournament_info'),

    # Add the GitHub webhook URL
    path('webhook/github/', GitHubWebhookView.as_view(), name='github_webhook'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)