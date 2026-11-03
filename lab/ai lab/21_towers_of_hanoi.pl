% Run:  swipl 01_towers_of_hanoi.pl
% Then try:
%   ?- hanoi(3).
%   ?- min_moves(5, C).

% Program 1: Towers of Hanoi
% move(N, From, To, Via): move N discs from From to To using Via
move(0, _, _, _) :- !.
move(N, From, To, Via) :-
    M is N - 1,
    move(M, From, Via, To),
    format('Move disc ~w from ~w to ~w~n', [N, From, To]),
    move(M, Via, To, From).

hanoi(N) :- format('--- Solving Towers of Hanoi for ~w discs ---~n', [N]),
            move(N, left, right, centre).

% minimum number of moves = 2^N - 1
min_moves(N, Count) :- Count is 2**N - 1.
