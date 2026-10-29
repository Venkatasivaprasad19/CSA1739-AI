
sum(0, 0).
% Recursive case : sum(N) = N + sum(N-1)
sum(N, S) :-
    N > 0,
    N1 is N - 1,
    sum(N1, S1),
    S is S1 + N.

% ---- Method 2 : tail recursion with an accumulator -----------
sum_acc(N, S) :- sum_acc(N, 0, S).
sum_acc(0, Acc, Acc).
sum_acc(N, Acc, S) :-
    N > 0,
    Acc1 is Acc + N,
    N1 is N - 1,
    sum_acc(N1, Acc1, S).

% ---- Method 3 : direct formula  N(N+1)/2 ---------------------
sum_formula(N, S) :- S is N * (N + 1) // 2.

% ---- Demo that runs automatically when the file is loaded ----
demo :-
    forall(member(N, [5, 10, 100]),
           ( sum(N, S1),
             sum_acc(N, S2),
             sum_formula(N, S3),
             format("N = ~w : recursion = ~w, accumulator = ~w, formula = ~w~n",
                    [N, S1, S2, S3]) )).

:- initialization(demo).

% ---- Sample queries to type at the  ?-  prompt ---------------
% ?- sum(5, S).            S = 15.
% ?- sum(10, S).           S = 55.
% ?- sum_acc(100, S).      S = 5050.
% ?- sum_formula(20, S).   S = 210.
