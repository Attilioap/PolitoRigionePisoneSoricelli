open util/integer

abstract sig User{
recivesNotification: set Notification
}

sig Student extends User{
participates: set Tournament,
recives: set Badge,
joins: set Team,
is_present: set StudentTournamentLeaderboard,
is_in: set StudentBattleLeaderboard
}

sig Educator extends User{
manages: set Tournament,
creates: set Badge,
makes: set ManualEvaluation,
managesBattle: set Battle
}

sig Tournament{
leaderboard: one StudentTournamentLeaderboard,
made_of: set Battle,
is_managed_by: some Educator,
enrolled_sudents: set Student,
has: set Badge
}


sig StudentTournamentLeaderboard{
referres_to: set Student,
relative_to: one Tournament
}

sig Battle{
studentLeaderboard: one StudentBattleLeaderboard,
teamLeaderboard: one TeamBattleLeaderboard,
managed_by: one Educator,
belongs_to: one Tournament,
teams: set Team,
relative_codeKata: one CodeKata
}

sig CodeKata{
battle: one Battle,
softwareProject: one SoftwareProject
}

sig SoftwareProject{
is_included: one CodeKata,
has: some TestCase
}

sig TestCase{
softwareProject: one SoftwareProject
}


sig StudentBattleLeaderboard{
referres_to: set Student,
relative_to: one Battle
}

sig TeamBattleLeaderboard{
referres_to: set Team,
relative_to: one Battle
}

sig Team{
battle : one Battle,
made_of: some Student,
score: one Score,
is_in: one TeamBattleLeaderboard
}

sig Score{
relative_to: one Team,
contribute1: lone ManualEvaluation,
contribute2: one AutomaticEvaluation
}


sig ManualEvaluation{
educator: one Educator,
score: one Score
}

sig AutomaticEvaluation{
score: one Score,
automaticEvaluationTool: one AutomaticEvaluationTool
}

sig Badge{
assigned_to: set Student,
tournament: one Tournament,
created_by: one Educator
}

sig AutomaticEvaluationTool{
makes: set AutomaticEvaluation
}

sig Notification{
is_recived_by: some User
}

//FACTS

//if an educator manages a tournament, then that educator should be included in the set of educators managing that particular tournament.
fact relEducatorTournament{
 all  e: Educator, t: Tournament | t in e.manages implies e in t.is_managed_by
}

// if a battle (b) is managed by an educator (b.managed_by = e), then that educator (e) should be included in the set of educators managing the tournament (e in t.is_managed_by) relative to the battle.
fact BattleIsCreatedOnlyFromEducatorWithTournamentManagmentPermissions{
	all b: Battle, e: Educator, t: Tournament | b.managed_by=e implies e in t.is_managed_by
}

// if a student (s) is enrolled in a tournament (s in t.enrolled_sudents), then that tournament (t) should be included in the set of tournaments in which the student participates (t in s.participates).
fact studentPartecipatesToMultipleTournaments{
 all s:Student, t:Tournament | s in t.enrolled_sudents implies t in s.participates
}

//if a student (s) is a member of a team (s in t.made_of), then that student should also be enrolled in the tournament to which the team's battle belongs (s in t.battle.belongs_to.enrolled_sudents).
fact studentsInATeamEntrolledInTheTournament{
	all s: Student, t: Team | s in t.made_of implies s in t.battle.belongs_to.enrolled_sudents
}

//if an automatic evaluation (ae) is made by an automatic evaluation tool (ae.automaticEvaluationTool = aet), then that automatic evaluation should be included in the set of evaluations 
//made by that specific automatic evaluation tool (ae in aet.makes).
fact AutomaticEvaluationIsMadeByAET{
	all ae: AutomaticEvaluation, aet: AutomaticEvaluationTool | ae.automaticEvaluationTool=aet implies ae in aet.makes
}

//each automatic evaluation (ae) is associated with exactly one automatic evaluation tool, and no two distinct automatic evaluation tools share the same set of evaluations.
fact eachAutomaticEvaluationIsMadeByOneAutomaticEvaluationTool{
	all ae: AutomaticEvaluation, disj aet1, aet2: AutomaticEvaluationTool | ae in aet1.makes implies ae not in aet2.makes
}

//if a manual evaluation (me) is created by an educator (me in e.makes), then that educator (e) must be the one managing the battle to which the manual evaluation is associated (e = (me.score.relative_to.battle.managed_by)).
fact educatorEvaluateOnlyWithPermissions{
	all me: ManualEvaluation, e: Educator | me in e.makes implies (e=(me.score.relative_to.battle.managed_by))
}

//there is a one-to-one correspondence between scores (s) and manual evaluations (me) in the context of the "contribute1" relationship.
fact singleManualEvaluationForScore{
	all s: Score, me: ManualEvaluation | s.contribute1=me iff me.score=s
}

// there is a one-to-one correspondence between scores (s) and automatic evaluations (ae) in the context of the "contribute2" relationship.
fact singleAutomaticEvaluationForScore{
	all s: Score, ae: AutomaticEvaluation | s.contribute2=ae iff ae.score=s
}

//if a manual evaluation (me) is associated with an educator (me.educator = e), then that manual evaluation should be included in the set of manual evaluations created by that specific educator (me in e.makes).
fact RelManualEvaluationEducator{
	all me: ManualEvaluation, e: Educator | me.educator=e implies me in e. makes
}

//each manual evaluation (me) is associated with exactly one educator, and no two distinct educators share the same set of manual evaluations.
fact singleEducatorForManualEvaluation{
	all me: ManualEvaluation, disj e1,e2: Educator | me in e1.makes implies me not in e2.makes
}

//there is a one-to-one correspondence between student battle leaderboards (sbl) and battles (b) in the context of the relative_to relationship.
fact singleStudentBattleLeaderboardForBattle{
	all sbl: StudentBattleLeaderboard, b: Battle | sbl.relative_to=b iff b.studentLeaderboard=sbl
}

//there is a one-to-one correspondence between team battle leaderboards (tbl) and battles (b) in the context of the relative_to relationship.
fact singleTeamBattleLeaderboardForBattle{
	all tbl: TeamBattleLeaderboard, b: Battle | tbl.relative_to=b iff b.teamLeaderboard=tbl
}

// there is a one-to-one correspondence between student tournament leaderboards (stl) and tournaments (t) in the context of the "relative_to" relationship.
fact singleTournamentLeaderboardForTournament{
	all stl: StudentTournamentLeaderboard, t: Tournament | stl.relative_to=t iff t.leaderboard=stl
}

// that there is a one-to-one correspondence between CodeKatas (ck) and Battles (b) in the context of the "relative_codeKata" relationship.
fact singleCodeKataForBattle{
	all b: Battle, ck: CodeKata | b.relative_codeKata=ck iff ck.battle=b
}

//there is a one-to-one correspondence between SoftwareProjects (sp) and CodeKatas (ck) in the context of the "is_included" relationship.
fact singleSoftwareProjectForcodeKata{
	all sp: SoftwareProject, ck: CodeKata | sp.is_included=ck iff ck.softwareProject=sp
}


//if a TestCase (tc) is associated with a SoftwareProject (tc.softwareProject = sp), then that TestCase should be included in the set of TestCases belonging to that specific SoftwareProject (tc in sp.has).
fact singleSoftwareProjectForTestCase{
	all sp: SoftwareProject, tc: TestCase | tc.softwareProject=sp implies tc in sp.has
}

//each SoftwareProject (sp) has a distinct set of TestCases, meaning that if a TestCase (tc) is in the set of TestCases of one SoftwareProject (tc in sp1.has), it should not be in the set of TestCases of another distinct SoftwareProject 
//(tc not in sp2.has).
fact eachSPHasDifferentTestCases{
	all disj sp1,sp2: SoftwareProject, tc: TestCase | tc in sp1.has implies tc not in sp2.has
}

//if a team (t) is associated with a battle (t.battle = b), then that team should be included in the set of teams associated with that specific battle (t in b.teams).
fact teamRelativeToABattle{
	all t: Team, b:Battle | t.battle=b implies t in b.teams
}

//each team (t) is associated with exactly one battle, meaning that if a team is in the set of teams associated with one battle (t in b1.teams), it should not be in the set of teams associated with another distinct battle (t not in b2.teams).
fact singleBattleForTeam{
	all disj b1, b2: Battle, t: Team | t in b1.teams implies t not in b2.teams
}

// there is a one-to-one correspondence between scores (s) and teams (t) in the context of the relative_to relationship.
fact singleScoreForTeam{
	all s: Score, t:Team | s.relative_to=t iff t.score=s
}

//each educator creates a unique set of badges, meaning that the set of badges created by one educator is not the same as the set of badges created by another educator.
fact educatorsCreatesDifferentBadges{
	all disj e1, e2: Educator | e1.creates != e2.creates
}

//each badge (b) is associated with exactly one educator (e), meaning that if a badge is created by an educator (b.created_by = e), then that badge should be included in the set of badges created by that specific educator
//(b in e.creates).
fact EachBadgeIsRelativeToAnEducator{
	all b: Badge, e: Educator | b.created_by=e iff b in e.creates
}

// if a badge (b) is created by an educator (b.created_by = e), then that educator should be one of the educators managing the tournament in which he's creating the badge.
fact EachEducatorCreatesBadgeWithPermissions{
	all b: Badge, e: Educator, t: Tournament | b.created_by=e implies e in t.is_managed_by
}

//if a badge (b) is associated with a specific tournament (b.tournament = t), then that badge should be included in the set of badges associated with that specific tournament (b in t.has).
fact  badgeAssignedInASingleTournament{
	 all b: Badge, t: Tournament | b.tournament=t implies b in t.has
}



pred createScenario{
	#Educator=2
	#Student=3
	#Tournament=1
	#Battle=2
	#TestCase=4
	#Team=2
	#ManualEvaluation=2
	#AutomaticEvaluationTool=1
	#Student=3
}

run createScenario for 5
