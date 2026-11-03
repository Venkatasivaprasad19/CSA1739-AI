% Run:  swipl 06_fruit_colour_backtracking.pl
% Then try:
%   ?- list_all.
%   ?- fruits_of(red).
%   ?- colours_of(mango).
%   ?- fruit_colour(F, green).

% Program 6: Fruit and its colour using backtracking
fruit_colour(apple,       red).
fruit_colour(apple,       green).
fruit_colour(banana,      yellow).
fruit_colour(grapes,      green).
fruit_colour(grapes,      purple).
fruit_colour(orange,      orange).
fruit_colour(mango,       yellow).
fruit_colour(mango,       green).
fruit_colour(strawberry,  red).
fruit_colour(blueberry,   blue).

% backtrack through every fact using fail
list_all :- fruit_colour(F, C),
            format('~w is ~w~n', [F, C]),
            fail.
list_all.

% print every fruit having a given colour
fruits_of(C) :- format('Fruits that are ~w:~n', [C]),
                fruit_colour(F, C), format('  - ~w~n', [F]), fail.
fruits_of(_).

% print every colour of a given fruit
colours_of(F) :- format('Colours of ~w:~n', [F]),
                 fruit_colour(F, C), format('  - ~w~n', [C]), fail.
colours_of(_).
