from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User, Group
from .models import Educator, Tournament, Student, Battle, Team, Invite, Repository


class CKBAppViewsTest(TestCase):
    def setUp(self):
        # Create Educator user
        self.educator_user = User.objects.create_user(username='educator', password='test_password')
        self.educator_group = Group.objects.create(name='Educators')
        self.educator_user.groups.add(self.educator_group)
        self.educator = Educator.objects.create(user=self.educator_user)

        # Create Student user
        self.student_user = User.objects.create_user(username='student', password='test_password')
        self.student_group = Group.objects.create(name='Students')
        self.student_user.groups.add(self.student_group)
        self.student = Student.objects.create(user=self.student_user)

        # Create a test tournament
        self.tournament = Tournament.objects.create(
            name='Test Tournament',
            registrationDeadline='2024-02-04',
            endingDate='2024-02-14',
            description='Test Description',
            creator=self.educator
        )

        # Create a test battle
        self.battle = Battle.objects.create(
            name='Test Battle',
            maxStudentsForTeam=3,
            registrationDeadline='2024-02-06',
            submissionDeadline='2024-02-10',
            creator=self.educator,
            tournament=self.tournament
        )

        # Create a test team
        self.team = Team.objects.create(
            name='Test Team',
            numTeammates=1,
            battle=self.battle
        )
        self.team.members.add(self.student)

    def test_signup_view(self):
        response = self.client.post(reverse('signup'), {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'username': 'johndoe',
            'password1': 'test_password',
            'is_educator': False
        })
        self.assertEqual(response.status_code, 302)  # Check for a successful redirect

    def test_user_login_view(self):
        response = self.client.post(reverse('login'), {'username': 'student', 'password': 'test_password'})
        self.assertEqual(response.status_code, 302)  # Check for a successful redirect

    def test_educator_dashboard_view(self):
        self.client.login(username='educator', password='test_password')
        response = self.client.get(reverse('educator_dash'))
        self.assertEqual(response.status_code, 200)  # Check for a successful response

    def test_tournament_info_view(self):
        tournament = Tournament.objects.create(name='Test Tournament', registrationDeadline='2024-02-04', endingDate='2024-02-14', description='Test Description', creator=self.educator)
        
        # Ensure the user is logged in (either educator or student)
        self.client.login(username='educator', password='test_password')

        response = self.client.get(reverse('tournament_info', args=[tournament.id]))
        
        # Check for a successful response or redirect
        self.assertIn(response.status_code, [200, 302])
        
        if response.status_code == 200:
            # If status_code is 200, check for the content or any other specific details
            self.assertContains(response, tournament.name)

    def test_student_dashboard_view(self):
        self.client.login(username='student', password='test_password')
        response = self.client.get(reverse('student_dash'))
        self.assertEqual(response.status_code, 200)  # Check for a successful response

    def test_tournament_managment_view(self):
        # Test if the view is accessible by an educator
        self.client.force_login(self.educator_user)
        response = self.client.get(reverse('tournament_managment', args=[self.tournament.id]))
        self.assertEqual(response.status_code, 200)

        # Test form submission for creating a battle
        response = self.client.post(reverse('tournament_managment', args=[self.tournament.id]), {
            'battle_name': 'New Battle',
            'max_students_for_team': 2,
            'registration_deadline': '2024-02-07',
            'submission_deadline': '2024-02-11',
            'code_kata': '',
            'security': 'on',
            'reliability': 'on',
            'maintainability': 'on'
        })
        self.assertEqual(response.status_code, 302)  # Check for a successful redirect after form submission

    def test_tournament_status_page_educator_view(self):
        # Test if the view is accessible by an educator
        self.client.force_login(self.educator_user)
        response = self.client.get(reverse('tournament_status_page_educator', args=[self.tournament.id]))
        self.assertEqual(response.status_code, 200)

        # Test closing the tournament
        response = self.client.post(reverse('tournament_status_page_educator', args=[self.tournament.id]), {'close_tournament': 'close'})
        self.assertEqual(response.status_code, 302)  # Check for a successful redirect after closing the tournament

    def test_battle_status_page_view(self):
        # Test if the view is accessible by an educator
        self.client.force_login(self.educator_user)
        response = self.client.get(reverse('battle_status_page', args=[self.battle.id]))
        self.assertEqual(response.status_code, 200)

    def test_tournament_status_page_student_view(self):
        # Test if the view is accessible by a student
        self.client.force_login(self.student_user)
        response = self.client.get(reverse('tournament_status_page_student', args=[self.tournament.id]))
        self.assertEqual(response.status_code, 200)

    def test_battle_status_student_view(self):
        # Test if the view is accessible by a student
        self.client.force_login(self.student_user)
        response = self.client.get(reverse('battle_status_student', args=[self.battle.id]))
        self.assertEqual(response.status_code, 200)

        # Test sending an invitation
        response = self.client.post(reverse('battle_status_student', args=[self.battle.id]), {
            'action_type': 'invite_teammate',
            'teammate_username': 'new_teammate'
        })
        self.assertEqual(response.status_code, 200)  # Check for a successful response after sending an invitation

    def tearDown(self):
        # Clean up objects created during setup
        User.objects.all().delete()
        Educator.objects.all().delete()
        Student.objects.all().delete()
        Tournament.objects.all().delete()
        Battle.objects.all().delete()
        Team.objects.all().delete()
        Invite.objects.all().delete()
        Repository.objects.all().delete()