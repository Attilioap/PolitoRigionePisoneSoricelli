from django.shortcuts import render, redirect, get_object_or_404
from .models import Tournament, Educator, Student, BattleLeaderboard, TournamentLeaderboard, TeamLeaderboard, Battle, Team, Invite
from django.contrib import messages
from datetime import datetime, timedelta, date
from .forms import SignupForm, EvaluationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import Http404


'''
def tournament_list():
    tournaments = Tournament.objects.all()
    past_tournaments=[tournament for tournament in tournaments if tournament.endingDate < datetime.now().date()]
    ongoing_tournaments=[tournament for tournament in tournaments if tournament.endingDate >= datetime.now().date()]
    return ongoing_tournaments, past_tournaments
    '''
'''
def student_tournament_list(student):
    subscribed_tournaments = student.tournaments_subscribed.all()
    past_tournaments = [tournament for tournament in subscribed_tournaments if tournament.endingDate < datetime.now().date()]
    upcoming_tournaments = [tournament for tournament in subscribed_tournaments if tournament.endingDate >= datetime.now().date()]
    return subscribed_tournaments, upcoming_tournaments, past_tournaments
    '''


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():

            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            is_educator = form.cleaned_data['is_educator']

        
            # Create User object
            user = User.objects.create(
                first_name=firstName,
                last_name=lastName,
                email=email,
                username=username,
                password=make_password(password1),
            )

            
            
            # Assign User to the appropriate group
            if is_educator:
                educator_group = Group.objects.get(name='Educators')
                educator_group.user_set.add(user)
                Educator.objects.create(user=user)
            else:
                student_group = Group.objects.get(name='Students')
                student_group.user_set.add(user)
                Student.objects.create(user=user)

            user = authenticate(request, username=username, password=password1)
            login(request, user)
            if is_educator:
            # Redirect to login or home page as appropriate
                return redirect('educator_dash')  
            else:
                return redirect('student_dash')

    else:
        form = SignupForm()

    return render(request, 'ckbapp/signup.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # Check user's group and redirect accordingly
                if user.groups.filter(name='Educators').exists():
                    return redirect('educator_dash')  
                elif user.groups.filter(name='Students').exists():
                    return redirect('student_dash')  

            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'ckbapp/login.html', {'form': form})



def educator_dash(request):
    if request.method == 'POST':
        # Handle form submission
        name = request.POST.get('tournament_name')
        registration_deadline = request.POST.get('registration_deadline')
        ending_date = request.POST.get('ending_date')
        description = request.POST.get('description')

        # Validate and create the tournament
        if name and registration_deadline and ending_date and description:
            # Parse date strings to datetime objects
            registration_deadline = datetime.strptime(registration_deadline, '%Y-%m-%d')
            ending_date = datetime.strptime(ending_date, '%Y-%m-%d')
            
  
            if registration_deadline.date() >= datetime.now().date() and ending_date.date() > datetime.now().date() and ending_date.date() > registration_deadline.date():
                # Get the logged-in educator
                educator = request.user.educator
                
                tournament = Tournament.objects.create(
                    name=name,
                    registrationDeadline=registration_deadline,
                    endingDate=ending_date,
                    description=description,
                    creator=educator
                )

                # Add the educator to the educators field
                tournament.educators.add(educator)

                messages.success(request, "Tournament created successfully.")
                # Redirect to the educator dashboard
                return redirect('educator_dash')
            else:
                # Add an error message
                messages.error(request, "Invalid dates. Registration deadline must be after or on today, and ending date must be after today. They also cannot be the same date")
                return redirect('educator_dash')

     # Handle GET request
    educator = request.user.educator  # Assuming the educator is logged in
    ongoing_tournaments = Tournament.objects.filter(educators=educator, endingDate__gte=datetime.now().date())
    past_tournaments = Tournament.objects.filter(educators=educator, endingDate__lt=datetime.now().date())


    return render(request, 'ckbapp/educator_dashboard.html', {'ongoing_tournaments': ongoing_tournaments, 'past_tournaments': past_tournaments})

@login_required
def student_dash(request):
    if request.method == 'POST':
        # Handle form submission for enrolling in a tournament
        tournament_id = request.POST.get('enroll_tournament_id')

        if tournament_id:
            # Get the logged-in student
            student = request.user.student

            try:
                # Get the selected tournament
                tournament = Tournament.objects.get(id=tournament_id)

                # Check if the student is already enrolled
                if student not in tournament.students.all():
                    # Enroll the student in the tournament
                    tournament.students.add(student)

                    # Add the student to TournamentLeaderboard with score = 0
                    TournamentLeaderboard.objects.create(tournament=tournament, student=student, score=0)

                    messages.success(request, f"You've successfully enrolled in {tournament.name}.")
                else:
                    messages.warning(request, f"You are already enrolled in {tournament.name}.")
            except Tournament.DoesNotExist:
                messages.error(request, "Tournament not found.")

            # Redirect to the student dashboard
            return redirect('student_dash')

    # Handle GET request
    student = request.user.student

    # Get tournaments that the student is already enrolled in
    enrolled_tournaments = Tournament.objects.filter(students=student, endingDate__gte=datetime.now().date())

    # Get upcoming tournaments that the student is not enrolled in
    upcoming_tournaments = Tournament.objects.exclude(students=student).filter(endingDate__gte=datetime.now().date())


    return render(request, 'ckbapp/student_dashboard.html', {'enrolled_tournaments': enrolled_tournaments, 'upcoming_tournaments': upcoming_tournaments})


def tournament_managment(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)

    if request.method == 'POST':
        # Check if the form is for granting permissions or creating a battle
        if 'username' in request.POST:
            # Handle granting permissions
            username = request.POST.get('username')

            try:
                educator = Educator.objects.get(user__username=username)

                if educator not in tournament.educators.all():
                    tournament.educators.add(educator)
                    messages.success(request, f"Permission granted to {educator.user.username}.")
                else:
                    messages.warning(request, f"{educator.user.username} already has permission.")

            except Educator.DoesNotExist:
                messages.error(request, "Educator not found.")

        else:
            # Handle battle creation form submission
            name = request.POST.get('battle_name')
            max_students_for_team = request.POST.get('max_students_for_team')
            registration_deadline = datetime.strptime(request.POST.get('registration_deadline'), '%Y-%m-%d').date()
            submission_deadline = datetime.strptime(request.POST.get('submission_deadline'), '%Y-%m-%d').date()
            code_kata = request.FILES.get('code_kata')

            try:
                battle = Battle.objects.create(
                    name=name,
                    maxStudentsForTeam=max_students_for_team,
                    registrationDeadline=registration_deadline,
                    submissionDeadline=submission_deadline,
                    codeKata=code_kata,
                    creator=request.user.educator,
                    tournament=tournament
                )


                messages.success(request, 'Battle created successfully.')
                return redirect('tournament_managment', tournament_id=tournament_id)

            except Exception as e:
                messages.error(request, f'Error creating battle: {e}')
    
    return render(request, 'ckbapp/tournament_managment.html', {'tournament_id': tournament_id})

@login_required
def tournament_status_page_educator(request, tournament_id):
    educator = request.user.educator
    tournament = get_object_or_404(Tournament, id=tournament_id, creator=educator)
    
    # Filter battles where the creator is the logged-in educator
    all_battles = Battle.objects.filter(tournament=tournament, creator=educator)

    # Separate battles into ongoing and ended based on submissionDeadline
    ongoing_battles = []
    ended_battles = []

    for battle in all_battles:
        if battle.submissionDeadline >= timezone.now().date():
            ongoing_battles.append(battle)
        else:
            ended_battles.append(battle)

    tournament_leaderboard = TournamentLeaderboard.objects.filter(tournament=tournament)

    if request.method == 'POST' and 'close_tournament' in request.POST:
        # Handle closing the tournament
        tournament.endingDate = timezone.now().date() - timedelta(days=1)
        tournament.save()
        return redirect('educator_dash')

    return render(request, 'ckbapp/tournament_status_page_educator.html', {
        'tournament': tournament,
        'ongoing_battles': ongoing_battles,
        'ended_battles': ended_battles,
        'tournament_leaderboard': tournament_leaderboard,
    })



@login_required
def battle_status_page(request, battle_id):
    battle = get_object_or_404(Battle, id=battle_id)

    battle_leaderboard = BattleLeaderboard.objects.filter(battle=battle).order_by('-score')

    # Retrieve TeamLeaderboard objects ordered by descending scores
    team_leaderboard = TeamLeaderboard.objects.filter(battle=battle).order_by('-score')

    # Create a list to store student usernames and their scores
    student_data = []

    # Iterate through BattleLeaderboard entries and gather student data
    for leaderboard_entry in battle_leaderboard:
        # Retrieve the Student object for the given student_id
        student = Student.objects.get(pk=leaderboard_entry.student_id)

        student_data.append({
            'username': student.user.username,
            'score': leaderboard_entry.score,
        })



    show_evaluate_section = False

    if request.method == 'POST' and 'evaluate_students_work' in request.POST:
        # Handle form submission for evaluating students' work
        form = EvaluationForm(battle, request.POST)
        if form.is_valid():
            # Process the form data (update team scores, etc.)
            for team in battle.teams.all():
                field_name = f'team_{team.id}_score'
                score = form.cleaned_data.get(field_name, 0)

                # Update TeamLeaderboard or create a new model to store evaluations
                team_leaderboard_entry, created = TeamLeaderboard.objects.get_or_create(
                    team=team,
                    battle=battle,
                    defaults={'score': score}
                )
                if not created:
                    team_leaderboard_entry.score = score
                    team_leaderboard_entry.save()

            return redirect('battle_status_page', battle_id=battle.id)  # Redirect to the same page

    else:
        form = EvaluationForm(battle)

    # Check if the submission deadline has passed
    if battle.submissionDeadline < date.today():
        show_evaluate_section = True

    return render(request, 'ckbapp/battle_status_page.html', {
        'battle': battle,
        'team_leaderboard': team_leaderboard,
        'battle_leaderboard': battle_leaderboard,
        'student_data' : student_data,
        'form': form,
        'show_evaluate_section': show_evaluate_section,
    })


@login_required
def tournament_status_page_student(request, tournament_id):
    student = request.user.student

    tournament = get_object_or_404(Tournament, id=tournament_id)



   # Initialize variables
    enrolled_battles = Battle.objects.filter(teams__members=student, tournament=tournament)
    upcoming_battles = Battle.objects.filter(tournament=tournament, registrationDeadline__gte=timezone.now().date()).exclude(teams__members=student)
    tournament_leaderboard = TournamentLeaderboard.objects.filter(tournament=tournament)

    # Get received invitations for the currently logged-in student
    received_invitations = Invite.objects.filter(invited_student=request.user.student, is_accepted=False, battle__tournament__id=tournament.id)

    if request.method == 'POST':

        action_type = request.POST.get('action_type')
        battle_id = request.POST.get('battle_id')
        invitation_id = request.POST.get('invitation_id')

        if action_type == 'join_battle' and battle_id:
            battle_to_join = get_object_or_404(Battle, id=battle_id)

            # Check if the student is already enrolled in the selected battle
            if Team.objects.filter(battle=battle_to_join, members=student).exists():
                messages.error(request, 'You are already enrolled in this battle.')
            else:
                # Create a new team for the student
                new_team = Team(name=student.user.username, numTeammates=1, battle=battle_to_join)
                new_team.save()

                # Add the student to the team
                new_team.members.add(student)

                # Add the new team to the teams attribute of the battle
                battle_to_join.teams.add(new_team)
                
                # Create or update the team leaderboard entry
                team_leaderboard, created = TeamLeaderboard.objects.get_or_create(
                    team=new_team,
                    battle=battle_to_join
                )

                # If the entry was created, it means it's a new team, so set the score to 0
                if created:
                    team_leaderboard.score = 0
                    team_leaderboard.save()

                # Create or update the team leaderboard entry
                battle_leaderboard, created = BattleLeaderboard.objects.get_or_create(
                    student=student,
                    battle=battle_to_join
                )

                # If the entry was created, it means it's a new team, so set the score to 0
                if created:
                    battle_leaderboard.score = 0
                    battle_leaderboard.save()

                # Delete all invitations related to the specified battle_id
                Invite.objects.filter(battle_id=battle_id).delete()


                messages.success(request, 'Successfully joined the battle.')

                # Update the enrolled_battles list after joining a new battle
                enrolled_battles = Battle.objects.filter(teams__members=student, tournament=tournament)


        elif action_type == 'invitation_response' and invitation_id:
            invitation = get_object_or_404(Invite, id=invitation_id)

            print(invitation)

            # Check if the invitation is for the logged-in student
            if invitation.invited_student == student:
                
                if request.POST.get('response') == 'accept':
                    print("ok")
                    # Enroll the student in the battle in the invited team
                    invited_team = invitation.team
                    invited_team.members.add(student)

                    # Set the value of is_accepted to True in the Invite model
                    invitation.is_accepted = True
                    invitation.save()

                    # Create or update the team leaderboard entry
                    battle_leaderboard = BattleLeaderboard.objects.get_or_create(
                        student=invitation.invited_student,
                        battle=invitation.battle,
                        score = TeamLeaderboard.objects.get(team_id=invitation.team).score
                        )
                    
                    # Get the queryset of invitations with the specified battle ID
                    invitations_to_delete = Invite.objects.filter(battle=invitation.battle_id)
                    print(battle_id)
                    print(invitations_to_delete)
                    # Delete all invitations in the queryset
                    invitations_to_delete.delete()

                    messages.success(request, 'Successfully accepted the team invitation.')

                elif request.POST.get('response') == 'decline':
                    print("nok")
                    # Remove the invitation
                    print(f"Invitation ID to delete: {invitation_id}")
                    invitation = get_object_or_404(Invite, id=invitation_id)

                    # Delete the invitation
                    invitation.delete()
                    messages.success(request, 'Successfully declined the team invitation.')



    return render(request, 'ckbapp/tournament_status_page_student.html', {
        'tournament': tournament,
        'enrolled_battles': enrolled_battles,
        'upcoming_battles': upcoming_battles,
        'tournament_leaderboard': tournament_leaderboard,
        'received_invitations' : received_invitations
    })

def battle_status_student(request, battle_id):
    battle = get_object_or_404(Battle, id=battle_id)
    
    # Retrieve BattleLeaderboard objects ordered by descending scores
    battle_leaderboard = BattleLeaderboard.objects.filter(battle=battle).order_by('-score')

    # Retrieve TeamLeaderboard objects ordered by descending scores
    team_leaderboard = TeamLeaderboard.objects.filter(battle=battle).order_by('-score')

    # Create a list to store student usernames and their scores
    student_data = []

    # Iterate through BattleLeaderboard entries and gather student data
    for leaderboard_entry in battle_leaderboard:
        # Retrieve the Student object for the given student_id
        student = Student.objects.get(pk=leaderboard_entry.student_id)

        student_data.append({
            'username': student.user.username,
            'score': leaderboard_entry.score,
        })

    

    # Handling sending an invitation
    if request.method == 'POST':
        invited_student_username = request.POST.get('teammate_username')
        
        print(get_object_or_404(User, id=request.user.id).username)
        
        if Team.objects.filter(battle_id=battle_id, name=get_object_or_404(User, id=request.user.id).username).exists():

            if invited_student_username:

                try:
                    invited_student = get_object_or_404(User, username=invited_student_username)
                    invited_student_instance = get_object_or_404(Student, user=invited_student)
                    team = get_object_or_404(Team, name=request.user.username, battle=battle_id)

                    print(request.user.student, invited_student_instance, team,battle)
                    if invited_student:
                        
                        invite = Invite.objects.all()
                        insert = True
                        for inv in invite:
                            if inv.inviting_student == request.user.student and inv.invited_student==invited_student_instance and inv.battle==battle:
                                insert = False
                        
                        if insert:
                            Invite(
                            inviting_student=request.user.student,
                            invited_student=invited_student_instance,
                            team = team,
                            battle=battle,
                            is_accepted = False).save()
                            messages.success(request, 'Invitation sent successfully.')
                        
                        else:
                            messages.warning(request, 'Invitation already sent to this student.')
                        
                        

                    
                            
                except Http404:
                    messages.warning(request, 'Invalid username.')    
            
        else:
            messages.warning(request, 'You cannot invite a teammate, you are not the Team Leader.')  

    return render(request, 'ckbapp/battle_status_student.html', {
        'battle': battle,
        'battle_leaderboard': battle_leaderboard,
        'team_leaderboard': team_leaderboard,
        'student_data': student_data
    })
#{% url 'tournament_info' tournament.id %}

#"{% url 'battle_status_page' battle.id %}"

#"{% url 'evaluate_students_work' battle.id %}"

#"{% url 'check_battle_status' battle.id %}"

#"{% url 'respond_to_invitation' invitation.id %}

#(0.000) INSERT INTO "ckbapp_invite" ("inviting_student_id", "invited_student_id", "team_id", "battle_id", "is_accepted")
# VALUES (24, 27, 49, 33, 0) RETURNING "ckbapp_invite"."id"; args=(24, 27, 49, 33, False); alias=default