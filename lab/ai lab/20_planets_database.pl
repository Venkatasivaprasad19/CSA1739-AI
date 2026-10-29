% ============================================================
% Experiment 10 : PLANETS database   (Prolog)
% Fact format : planet(Name, Position, Diameter_km, Moons, Type, Distance_AU).
% Position = order from the Sun, Distance in Astronomical Units (AU).
% (Moon counts are approximate and change as new moons are discovered.)
% ============================================================

% ---------------- Facts --------------------------------------
planet(mercury, 1,   4879,   0, rocky,     0.39).
planet(venus,   2,  12104,   0, rocky,     0.72).
planet(earth,   3,  12756,   1, rocky,     1.00).
planet(mars,    4,   6792,   2, rocky,     1.52).
planet(jupiter, 5, 142984,  95, gas_giant, 5.20).
planet(saturn,  6, 120536, 146, gas_giant, 9.58).
planet(uranus,  7,  51118,  28, ice_giant, 19.20).
planet(neptune, 8,  49528,  16, ice_giant, 30.05).

% ---------------- Rules --------------------------------------

% Planets of a given type
type_of(Name, Type) :- planet(Name, _, _, _, Type, _).

% Inner (rocky) planets and outer planets
inner_planet(Name) :- planet(Name, _, _, _, rocky, _).
outer_planet(Name) :- planet(Name, _, _, _, Type, _), Type \== rocky.

% Planet with more than N moons
has_more_moons(Name, N) :- planet(Name, _, _, Moons, _, _), Moons > N.

% Planets without any moon
no_moon(Name) :- planet(Name, _, _, 0, _, _).

% Larger than another planet
larger(X, Y) :-
    planet(X, _, DX, _, _, _),
    planet(Y, _, DY, _, _, _),
    DX > DY.

% Closer to the Sun than another planet
closer(X, Y) :-
    planet(X, PX, _, _, _, _),
    planet(Y, PY, _, _, _, _),
    PX < PY.

% The biggest planet (largest diameter)
biggest(Name) :-
    planet(Name, _, D, _, _, _),
    \+ ( planet(_, _, D2, _, _, _), D2 > D ).

% The planet next to a given one (its neighbour from the Sun)
next_planet(X, Y) :-
    planet(X, P, _, _, _, _),
    P1 is P + 1,
    planet(Y, P1, _, _, _, _).

% Planets within a given distance (AU) from the Sun
within_au(Name, Limit) :- planet(Name, _, _, _, _, D), D =< Limit.

% Show all planets in a table
list_planets :-
    format("~w~t~10|~w~t~18|~w~t~28|~w~t~35|~w~n",
           ['Planet', 'Order', 'Diameter', 'Moons', 'Type']),
    forall(planet(N, P, D, M, T, _),
           format("~w~t~10|~w~t~18|~w~t~28|~w~t~35|~w~n", [N, P, D, M, T])).

% ---------------- Demo (runs automatically) ------------------
demo :-
    list_planets,
    findall(N, type_of(N, gas_giant), L1),
    format("~nGas giants        : ~w~n", [L1]),
    findall(N, inner_planet(N), L2),
    format("Inner planets      : ~w~n", [L2]),
    findall(N, no_moon(N), L3),
    format("Planets with no moon : ~w~n", [L3]),
    findall(N, has_more_moons(N, 20), L4),
    format("More than 20 moons : ~w~n", [L4]),
    biggest(B), format("Biggest planet     : ~w~n", [B]),
    next_planet(earth, Nx), format("Planet after earth : ~w~n", [Nx]),
    findall(N, within_au(N, 2.0), L5),
    format("Within 2 AU of Sun : ~w~n", [L5]).

:- initialization(demo).

% ---------------- Sample queries ------------------------------
% ?- planet(mars, Order, Dia, Moons, Type, AU).
% ?- type_of(P, ice_giant).
% ?- larger(saturn, earth).
% ?- closer(venus, mars).
% ?- biggest(P).
