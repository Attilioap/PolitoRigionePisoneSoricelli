# create_repositories.py
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



def create_github_repository(battle_name):
    
    github_token = settings.GITHUB_ACCESS_TOKEN
    g = Github(github_token)
    user = g.get_user()
    repo = user.create_repo(battle_name)
    return repo.html_url



def create_repository_entry(battle, student, repo_url):
    # Create a new Repositories entry in the database
    Repository.objects.create(battle=battle, student_id=student, link=repo_url)
    print(f"Repository entry created for {student} in battle {battle.id}")

def start_all_pending_battles():

    pending_battles = Battle.objects.filter(has_started=False)

    for battle in pending_battles:
        battle_id = battle.id

        try:
            # Get the battle
            battle = Battle.objects.get(id=battle_id)
            
            # Check if the battle has started
            if battle.registrationDeadline < timezone.now().date():
                print("okkkkk")
                # Create GitHub repository
                repo_url = create_github_repository(battle.name)

                # Notify enrolled students about the repository link
                enrolled_students = set()

                # Iterate over teams and collect emails
                for team in battle.teams.all():
                    enrolled_students.update(team.members.values_list('user', flat=True))

                # Create Repositories entry for each student
                for student in enrolled_students:
                    create_repository_entry(battle, student, repo_url)

                # Set has_started to True after repository creation and entries
                battle.has_started = True
                battle.save()

                print(f"All repositories for battle {battle_id} created and entries added.")
            else:
                print(f"The battle {battle_id} has not started yet.")
        except Battle.DoesNotExist:
            print(f"Battle with id {battle_id} does not exist.")

if __name__ == "__main__":
    start_all_pending_battles()




'''
def add_webhook_to_repository(github_instance, repo_full_name):
    # Get the repository object
    repo = github_instance.get_repo(repo_full_name)

    # Define the webhook URL in your Django app
    webhook_url = 'https://petite-geese-return.loca.lt/webhook/github/'

    # Set up the webhook
    webhook_config = {
        'url': webhook_url,
        'content_type': 'json',
        'events': ['push'],  # Listen to push events
    }

    # Create the webhook
    repo.create_hook('web', webhook_config, active=True)

def create_github_repository(battle_name):
    github_token = settings.GITHUB_ACCESS_TOKEN
    g = Github(github_token)
    user = g.get_user()
    repo = user.create_repo(battle_name)

    # Get the repository's full name (username/repo_name)
    repo_full_name = repo.full_name

    # Add a webhook for push events to the repository
    #add_webhook_to_repository(g, repo_full_name)
    return repo.html_url



def create_repository_entry(battle, student, repo_url):
    # Create a new Repositories entry in the database
    Repository.objects.create(battle=battle, student_id=student, link=repo_url)
    print(f"Repository entry created for {student} in battle {battle.id}")

def start_all_pending_battles():

    pending_battles = Battle.objects.filter(has_started=False)

    for battle in pending_battles:
        battle_id = battle.id

        try:
            # Get the battle
            battle = Battle.objects.get(id=battle_id)

            # Check if the battle has started
            if battle.registrationDeadline < timezone.now().date():

                # Create GitHub repository
                repo_url = create_github_repository(battle.name)

                # Notify enrolled students about the repository link
                enrolled_students = set()

                # Iterate over teams and collect emails
                for team in battle.teams.all():
                    enrolled_students.update(team.members.values_list('user', flat=True))

                # Create Repositories entry for each student
                for student in enrolled_students:
                    create_repository_entry(battle, student, repo_url)

                # Set has_started to True after repository creation and entries
                battle.has_started = True
                battle.save()

                print(f"All repositories for battle {battle_id} created and entries added.")
            else:
                print(f"The battle {battle_id} has not started yet.")
        except Battle.DoesNotExist:
            print(f"Battle with id {battle_id} does not exist.")

if __name__ == "__main__":
    start_all_pending_battles()
'''