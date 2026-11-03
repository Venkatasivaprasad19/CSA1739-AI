% Run:  swipl 02_bird_can_fly.pl
% Then try:
%   ?- check(sparrow).
%   ?- check(penguin).
%   ?- check(dog).
%   ?- can_fly(B).
%   ?- bird(B), \+ can_fly(B).

% Program 2: Can a particular bird fly?
bird(sparrow).  bird(eagle).  bird(crow).  bird(parrot).
bird(penguin).  bird(ostrich). bird(kiwi).

% exceptions: birds that cannot fly
cannot_fly(penguin).  cannot_fly(ostrich).  cannot_fly(kiwi).

can_fly(B) :- bird(B), \+ cannot_fly(B).

check(B) :- bird(B), can_fly(B), !, format('~w can fly.~n', [B]).
check(B) :- bird(B), !, format('~w cannot fly.~n', [B]).
check(B) :- format('~w is not in the bird database.~n', [B]).
