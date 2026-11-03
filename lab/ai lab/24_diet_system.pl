% Run:  swipl 04_diet_system.pl
% Then try:
%   ?- suggest(diabetes).
%   ?- suggest(anaemia).
%   ?- suggest(asthma).
%   ?- avoid(D, salt).

% Program 4: Diet suggestion system based on disease
diet(diabetes,      'Low sugar, high fibre: oats, leafy greens, lentils. Avoid sweets and white rice.').
diet(hypertension,  'Low salt (DASH style): fruits, vegetables, banana, low-fat curd. Avoid pickles and chips.').
diet(anaemia,       'Iron rich: spinach, beetroot, dates, jaggery, pomegranate. Add vitamin C.').
diet(obesity,       'Low calorie: salads, sprouts, buttermilk, grilled foods. Avoid fried snacks.').
diet(typhoid,       'Soft and easy to digest: rice kanji, boiled potato, banana, ORS. Avoid spicy food.').
diet(gastritis,     'Bland food: curd rice, idli, banana, coconut water. Avoid tea, coffee and spice.').

avoid(diabetes, sugar).   avoid(hypertension, salt).
avoid(obesity, fried_food). avoid(gastritis, spicy_food).

suggest(Disease) :- diet(Disease, Plan), !,
    format('Disease : ~w~nDiet    : ~w~n', [Disease, Plan]).
suggest(Disease) :- format('No diet plan stored for ~w. Consult a doctor.~n', [Disease]).
