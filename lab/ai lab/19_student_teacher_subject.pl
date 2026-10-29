% ============================================================
% Experiment 9 : STUDENT - TEACHER - SUBJECT - CODE database   (CO1)
% Facts : student(Name).               teacher(Name).
%         subject(Code, SubjectName).
%         teaches(Teacher, Code).      studies(Student, Code).
% ============================================================

% ---------------- Facts --------------------------------------
student(arun).
student(meena).
student(rahul).
student(priya).
student(siva).

teacher(ramesh).
teacher(lakshmi).
teacher(suresh).

subject(csa17, artificial_intelligence).
subject(csa43, internet_programming).
subject(csa21, database_management).
subject(csa30, cryptography).

teaches(ramesh,  csa17).
teaches(lakshmi, csa43).
teaches(suresh,  csa21).
teaches(ramesh,  csa30).

studies(arun,  csa17).
studies(arun,  csa43).
studies(meena, csa17).
studies(meena, csa21).
studies(rahul, csa43).
studies(priya, csa30).
studies(priya, csa17).
studies(siva,  csa43).
studies(siva,  csa30).

% ---------------- Rules --------------------------------------

% Name of the subject taught by a teacher
teacher_subject(Teacher, SubjectName) :-
    teaches(Teacher, Code),
    subject(Code, SubjectName).

% Which teacher teaches a student?
student_teacher(Student, Teacher) :-
    studies(Student, Code),
    teaches(Teacher, Code).

% Student with the subject name and its teacher
student_subject_teacher(Student, SubjectName, Teacher) :-
    studies(Student, Code),
    subject(Code, SubjectName),
    teaches(Teacher, Code).

% Students of a teacher
students_of(Teacher, Student) :-
    teaches(Teacher, Code),
    studies(Student, Code).

% Two students who study the same subject (classmates)
classmates(S1, S2) :-
    studies(S1, Code),
    studies(S2, Code),
    S1 @< S2.

% Teachers who teach more than one subject
teaches_many(Teacher) :-
    teaches(Teacher, C1),
    teaches(Teacher, C2),
    C1 @< C2.

% Number of students in a subject
count_students(Code, N) :-
    findall(S, studies(S, Code), L),
    length(L, N).

% ---------------- Demo (runs automatically) ------------------
demo :-
    writeln("--- Student, subject and teacher ---"),
    forall(student_subject_teacher(St, Sub, T),
           format("~w~t~8|  studies ~w~t~35|  taught by ~w~n", [St, Sub, T])),
    findall(S, students_of(ramesh, S), L1), sort(L1, U1),
    format("~nStudents of ramesh : ~w~n", [U1]),
    findall(T, student_teacher(arun, T), L2), sort(L2, U2),
    format("Teachers of arun    : ~w~n", [U2]),
    findall(T, teaches_many(T), L3), sort(L3, U3),
    format("Teachers with more than one subject : ~w~n", [U3]),
    count_students(csa17, N),
    format("Number of students in csa17 : ~w~n", [N]),
    findall(A-B, classmates(A, B), L4),
    format("Classmates : ~w~n", [L4]).

:- initialization(demo).

% ---------------- Sample queries ------------------------------
% ?- teacher_subject(ramesh, S).
% ?- student_teacher(meena, T).
% ?- subject(Code, cryptography).
% ?- students_of(lakshmi, S).
% ?- classmates(arun, X).
