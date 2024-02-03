import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codekatabattle.settings') 

# Initialize Django
django.setup()

from github import Github
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from ckbapp.models import Battle, Repository



def create_github_repository(battle_name, code_kata_path):
    
    github_token = settings.GITHUB_ACCESS_TOKEN
    g = Github(github_token)
    user = g.get_user()
    repo = user.create_repo(battle_name)
    # Upload code kata file to the repository
    with open(code_kata_path, 'rb') as kata_file:
        repo.create_file('code_katas/code_kata.py', 'Initial commit', kata_file.read(), branch='main')
 
    # Add a webhook for your Django app
    webhook_config = {
        'url': settings.DJANGO_APP_WEBHOOK_URL,
        'content_type': 'json',
        'events': ['push'],
    }

    repo.create_hook(name='web', config=webhook_config, events=webhook_config['events'], active=True)

    return repo.html_url



def create_repository_entry(battle, student, repo_url):
    # Create a new Repositories entry in the database
    Repository.objects.create(battle=battle, student_id=student, link=repo_url)


def start_all_pending_battles():

    pending_battles = Battle.objects.filter(has_started=False)

    for battle in pending_battles:
        battle_id = battle.id

        try:
            # Get the battle
            battle = Battle.objects.get(id=battle_id)
            
            # Check if the battle has started
            if battle.registrationDeadline < timezone.now().date():
                code_kata_path = battle.codeKata.path
                
                # Create GitHub repository
                repo_url = create_github_repository(battle.name, code_kata_path)

                # Notify enrolled students about the repository link
                enrolled_students = set()

                # Iterate over teams
                for team in battle.teams.all():
                    enrolled_students.update(team.members.values_list('user', flat=True))

                # Create Repositories entry for each student
                for student in enrolled_students:
                    create_repository_entry(battle, student, repo_url)

                # Set has_started to True after repository creation and entries
                battle.has_started = True
                battle.save()
            
        except Battle.DoesNotExist:
            pass

if __name__ == "__main__":
    start_all_pending_battles()


