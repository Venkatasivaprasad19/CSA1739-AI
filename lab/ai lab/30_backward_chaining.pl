% Run:  swipl 10_backward_chaining.pl
% Then try:
%   ?- ask(can_vote(anil)).
%   ?- ask(can_vote(zoya)).
%   ?- ask(can_vote(john)).

% Program 10: Backward chaining (goal driven) with proof trace
rule(can_vote(X),        [adult(X), citizen(X), registered(X)]).
rule(adult(X),           [age_over_18(X)]).
rule(registered(X),      [has_voter_id(X)]).

fact(citizen(anil)).     fact(age_over_18(anil)).   fact(has_voter_id(anil)).
fact(citizen(zoya)).     fact(age_over_18(zoya)).
fact(citizen(john)).

prove(Goal, D) :- fact(Goal),
    tab(D), format('~w  [known fact]~n', [Goal]).
prove(Goal, D) :- rule(Goal, Subgoals),
    tab(D), format('~w  [needs: ~w]~n', [Goal, Subgoals]),
    D1 is D + 3, prove_all(Subgoals, D1).

prove_all([], _).
prove_all([G|Gs], D) :- prove(G, D), prove_all(Gs, D).

ask(Goal) :- format('~nGoal: ~w~n', [Goal]),
    ( prove(Goal, 2) -> writeln('RESULT: goal is TRUE') ; writeln('RESULT: goal is FALSE') ), !.
