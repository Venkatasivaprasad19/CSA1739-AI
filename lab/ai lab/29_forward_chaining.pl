% Run:  swipl 09_forward_chaining.pl
% Then try:
%   ?- show_facts.
%   ?- forward.
%   ?- show_facts.

% Program 9: Forward chaining (data driven)
:- dynamic fact/1.

% rules: rule(Conclusion, [Conditions])
rule(has_wings,      [is_bird]).
rule(can_fly,        [has_wings, has_light_body]).
rule(builds_nest,    [is_bird]).
rule(lays_eggs,      [builds_nest]).
rule(can_migrate,    [can_fly, lays_eggs]).

fact(is_bird).
fact(has_light_body).

all_true([]).
all_true([C|T]) :- fact(C), all_true(T).

% fire any rule whose conditions hold and whose conclusion is new
step :- rule(Concl, Conds), \+ fact(Concl), all_true(Conds),
        assertz(fact(Concl)),
        format('Rule fired: ~w  ==>  new fact: ~w~n', [Conds, Concl]).

forward :- step, !, forward.
forward :- writeln('No more rules can fire. Inference complete.').

show_facts :- findall(F, fact(F), L), format('Facts in memory: ~w~n', [L]).
