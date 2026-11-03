% Run:  swipl 07_best_first_search.pl
% Then try:
%   ?- best_first(salem, chennai, Path).
%   ?- best_first(erode, chennai, P).

% Program 7: Best First Search (greedy, uses heuristic h(Node))
% Road map between towns, goal = chennai
edge(salem,     erode,      60).   edge(salem,   dharmapuri, 65).
edge(erode,     coimbatore, 90).   edge(erode,   trichy,     140).
edge(dharmapuri,vellore,   170).   edge(vellore, chennai,    140).
edge(trichy,    villupuram,160).   edge(villupuram, chennai, 160).
edge(coimbatore,palakkad,   55).
neighbour(X, Y) :- edge(X, Y, _) ; edge(Y, X, _).

% heuristic: straight-line distance to chennai (km, approximate)
h(chennai, 0).     h(vellore, 130).   h(villupuram, 150). h(dharmapuri, 270).
h(trichy, 290).    h(erode, 340).     h(salem, 300).      h(coimbatore, 430). h(palakkad, 480).

best_first(Start, Goal, Path) :-
    h(Start, H0),
    bfs([H0-[Start]], Goal, RevPath),
    reverse(RevPath, Path).

bfs([_-[Goal|T]|_], Goal, [Goal|T]) :- !.
bfs([_-[Node|T]|Frontier], Goal, Path) :-
    findall(H-[Next,Node|T],
            ( neighbour(Node, Next), \+ memberchk(Next, [Node|T]), h(Next, H) ),
            Children),
    append(Frontier, Children, Open),
    keysort(Open, Sorted),                 % lowest heuristic first
    format('Expanding ~w, open list: ~w~n', [Node, Sorted]),
    bfs(Sorted, Goal, Path).
