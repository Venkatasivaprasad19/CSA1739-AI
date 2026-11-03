% Run:  swipl 03_family_tree.pl
% Then try:
%   ?- father(raghav, X).
%   ?- grandparent(raghav, G).
%   ?- sibling(rohan, S).
%   ?- uncle(U, rohan).
%   ?- cousin(rohan, divya).
%   ?- ancestor(raghav, D).

% Program 3: Family tree (three generations)
male(raghav).  male(arjun).  male(vikram). male(rohan).
female(lakshmi). female(sita). female(meena). female(sneha). female(divya). female(anaya).

parent(raghav, arjun).   parent(lakshmi, arjun).
parent(raghav, meena).   parent(lakshmi, meena).
parent(raghav, vikram).  parent(lakshmi, vikram).
parent(arjun, rohan).    parent(sita, rohan).
parent(arjun, anaya).    parent(sita, anaya).
parent(vikram, divya).   parent(sneha, divya).

father(F, C)      :- male(F), parent(F, C).
mother(M, C)      :- female(M), parent(M, C).
grandparent(G, C) :- parent(G, P), parent(P, C).
% full siblings share the same father (each child has exactly one father)
sibling(X, Y)     :- father(F, X), father(F, Y), X \= Y.
brother(B, S)     :- male(B), sibling(B, S).
sister(S, X)      :- female(S), sibling(S, X).
uncle(U, N)       :- male(U), parent(P, N), sibling(U, P).
aunt(A, N)        :- female(A), parent(P, N), sibling(A, P).
cousin(X, Y)      :- parent(P1, X), parent(P2, Y), sibling(P1, P2).
ancestor(A, D)    :- parent(A, D).
ancestor(A, D)    :- parent(A, X), ancestor(X, D).
