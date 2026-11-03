% Run:  swipl 08_medical_diagnosis.pl
% Then try:
%   ?- report(kumar).
%   ?- report(priya).
%   ?- report(david).
%   ?- diagnose(P, malaria).

% Program 8: Medical diagnosis (rule based)
:- dynamic has/2.

symptom_of(flu,        fever).      symptom_of(flu,        body_ache).
symptom_of(flu,        cough).      symptom_of(flu,        headache).
symptom_of(malaria,    fever).      symptom_of(malaria,    chills).
symptom_of(malaria,    sweating).   symptom_of(malaria,    vomiting).
symptom_of(dengue,     fever).      symptom_of(dengue,     joint_pain).
symptom_of(dengue,     rash).       symptom_of(dengue,     headache).
symptom_of(migraine,   headache).   symptom_of(migraine,   nausea).
symptom_of(migraine,   light_sensitivity).

advice(flu,      'Rest, fluids, paracetamol. See a doctor if fever lasts > 3 days.').
advice(malaria,  'Get a blood smear test immediately and start anti-malarial treatment.').
advice(dengue,   'Platelet count test, plenty of fluids, avoid aspirin.').
advice(migraine, 'Rest in a dark room, hydrate, consult a neurologist if frequent.').

% patient records
has(kumar, fever).  has(kumar, chills).  has(kumar, sweating).  has(kumar, vomiting).
has(priya, headache). has(priya, nausea). has(priya, light_sensitivity).
has(david, fever). has(david, joint_pain). has(david, rash). has(david, headache).
has(ravi, cough).

% a patient is diagnosed when ALL symptoms of the disease are present
patient(P)  :- setof(P0, S^has(P0, S), Ps), member(P, Ps).
disease(D)  :- setof(D0, S^symptom_of(D0, S), Ds), member(D, Ds).

diagnose(P, D) :-
    patient(P), disease(D),
    forall(symptom_of(D, S), has(P, S)).

report(P) :- diagnose(P, D), !, advice(D, A),
    format('Patient ~w -> probable disease: ~w~nAdvice: ~w~n', [P, D, A]).
report(P) :- format('Patient ~w -> no disease matched, consult a doctor.~n', [P]).
