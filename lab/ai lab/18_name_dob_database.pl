% ============================================================
% Experiment 8 : Prolog database with NAME and DATE OF BIRTH   (CO5)
% Fact format : dob(Name, Day, Month, Year).
% ============================================================

% ---------------- Facts (the database) -----------------------
dob(arun,    15,  8, 2003).
dob(meena,    2,  1, 2004).
dob(rahul,   23,  8, 2002).
dob(priya,   10, 12, 2003).
dob(kumar,    5,  3, 2004).
dob(divya,   30,  1, 2003).
dob(siva,    18,  6, 2004).

current_year(2026).

% ---------------- Rules --------------------------------------

% Who was born in a given year?
born_in_year(Name, Year) :- dob(Name, _, _, Year).

% Who was born in a given month?
born_in_month(Name, Month) :- dob(Name, _, Month, _).

% Date of birth printed as day-month-year
show_dob(Name) :-
    dob(Name, D, M, Y),
    format("~w was born on ~d-~d-~d~n", [Name, D, M, Y]).

% Approximate age = current year - birth year
age(Name, Age) :-
    dob(Name, _, _, Y),
    current_year(Now),
    Age is Now - Y.

% X is older than Y  (compare year, then month, then day)
older(X, Y) :-
    dob(X, D1, M1, Y1),
    dob(Y, D2, M2, Y2),
    X \== Y,
    ( Y1 < Y2
    ; Y1 =:= Y2, M1 < M2
    ; Y1 =:= Y2, M1 =:= M2, D1 < D2 ).

% Two different people with the same birth month
same_month(X, Y) :-
    dob(X, _, M, _),
    dob(Y, _, M, _),
    X @< Y.

% Count the people in the database
count_people(N) :- findall(X, dob(X, _, _, _), L), length(L, N).

% Show the full database
list_all :-
    forall(dob(N, D, M, Y),
           format("~w~t~10|  ~d-~d-~d~n", [N, D, M, Y])).

% ---------------- Demo (runs automatically) ------------------
demo :-
    writeln("--- Database ---"), list_all,
    count_people(C), format("~nTotal people : ~w~n", [C]),
    findall(N, born_in_year(N, 2003), L1),
    format("Born in 2003 : ~w~n", [L1]),
    findall(N, born_in_month(N, 8), L2),
    format("Born in August : ~w~n", [L2]),
    age(arun, A), format("Age of arun : ~w~n", [A]),
    findall(X, older(X, arun), L3),
    format("Older than arun : ~w~n", [L3]),
    findall(X-Y, same_month(X, Y), L4),
    format("Same birth month : ~w~n", [L4]).

:- initialization(demo).

% ---------------- Sample queries ------------------------------
% ?- dob(arun, D, M, Y).
% ?- born_in_year(Who, 2004).        (press ; to see more answers)
% ?- age(meena, A).
% ?- older(rahul, priya).
% ?- show_dob(arun).
