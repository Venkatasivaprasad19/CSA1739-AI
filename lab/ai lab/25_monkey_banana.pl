% Run:  swipl 05_monkey_banana.pl
% Then try:
%   ?- solve.

% Program 5: Monkey and Banana problem
% state(MonkeyHorizontal, MonkeyVertical, BoxPosition, HasBanana)
% The banana hangs from the ceiling in the middle of the room.

place(atdoor).  place(middle).  place(atwindow).

% move(State1, Action, State2)
move(state(middle, onbox, middle, hasnot), grasp,        state(middle, onbox, middle, has)).
move(state(P, onfloor, P, H),              climb,        state(P, onbox, P, H)).
move(state(P1, onfloor, P1, H),            push(P1, P2), state(P2, onfloor, P2, H)) :- place(P2), P2 \= P1.
move(state(P1, onfloor, B, H),             walk(P1, P2), state(P2, onfloor, B, H))  :- place(P2), P2 \= P1.

% canget(State, Plan): Plan is a list of actions that ends with the banana in hand
canget(state(_, _, _, has), []).
canget(State1, [Act|Rest]) :-
    move(State1, Act, State2),
    canget(State2, Rest).

% iterative deepening: try plans of length 0,1,2,... so the shortest plan is found first
solve :-
    Start = state(atdoor, onfloor, atwindow, hasnot),
    length(Plan, N),
    canget(Start, Plan), !,
    format('Shortest plan found in ~w steps:~n', [N]),
    forall(nth1(I, Plan, A), format('  Step ~w: ~w~n', [I, A])).
