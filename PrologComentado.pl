% --------------------------
% motor.pl – Sistema Experto de Cócteles
% --------------------------

:- dynamic calificacion/6.

Comentario : Aqui se insertan los hechos de calificaciones de cócteles.

% Hecho: calificacion(Edad, Estrato, Carrera, Genero, IdCoctel, Calificacion).
agregar_calificacion(Edad, Estrato, Carrera, Genero, IdCoctel, Calificacion) :-
    assertz(calificacion(Edad, Estrato, Carrera, Genero, IdCoctel, Calificacion)).

% --------------------------------
% Coincidencias según nivel
% --------------------------------


% Coincidencia 1: exacta
usuario_match1(Edad, Estrato, Carrera, Genero, Id, Cal) :-
    calificacion(Edad, Estrato, Carrera, Genero, Id, Cal).

% Coincidencia 2: misma carrera y género, edad ±5, estrato ±2
usuario_match2(EdadU, EstratoU, Carrera, Genero, Id, Cal) :-
    calificacion(Edad, Estrato, Carrera, Genero, Id, Cal),
    abs(Edad - EdadU) =< 5,
    abs(Estrato - EstratoU) =< 2.

% Coincidencia 3: solo género, edad ±5, estrato ±2. Por ejemplo si ingreso 19 años y estrato 3, me puede recomendar un cóctel de alguien de 14 a 24 años y estrato 1 a 5.
% Esto es útil para encontrar cócteles de personas que no tienen la misma carrera.
usuario_match3(EdadU, EstratoU, _, Genero, Id, Cal) :-
    calificacion(Edad, Estrato, _, Genero, Id, Cal),
    abs(Edad - EdadU) =< 5,
    abs(Estrato - EstratoU) =< 2.

% --------------------------------
% Ponderación por calificación
% --------------------------------

Son pesos que se asignan a cada calificación segun el match. Por ejemplo, si la calificación es 5 en el match 1, el peso es 1, si es 4, el peso es 0.5, y así sucesivamente.

peso_match1(5, 1).
peso_match1(4, 0.5).
peso_match1(3, 0).
peso_match1(2, -0.5).
peso_match1(1, -1).

peso_match2(5, 0.5).
peso_match2(4, 0.2).
peso_match2(3, 0).
peso_match2(2, -0.2).
peso_match2(1, -0.5).

peso_match3(5, 0.2).
peso_match3(4, 0.1).
peso_match3(3, 0).
peso_match3(2, -0.1).
peso_match3(1, -0.2).

% --------------------------------
% Sumar pesos por cóctel
% --------------------------------

% Match 1
sumar_pesos_match1(Edad, Estrato, Carrera, Genero, Id, PesoTotal) :-
    findall(P, (usuario_match1(Edad, Estrato, Carrera, Genero, Id, Cal), peso_match1(Cal, P)), Pesos),
    sumlist(Pesos, PesoTotal).

% Match 2
sumar_pesos_match2(Edad, Estrato, Carrera, Genero, Id, PesoTotal) :-
    findall(P, (usuario_match2(Edad, Estrato, Carrera, Genero, Id, Cal), peso_match2(Cal, P)), Pesos),
    sumlist(Pesos, PesoTotal).

% Match 3
sumar_pesos_match3(Edad, Estrato, Carrera, Genero, Id, PesoTotal) :-
    findall(P, (usuario_match3(Edad, Estrato, Carrera, Genero, Id, Cal), peso_match3(Cal, P)), Pesos),
    sumlist(Pesos, PesoTotal).

% --------------------------------
% Acumulación total por cóctel
% --------------------------------

puntaje_total(Edad, Estrato, Carrera, Genero, Id, Puntaje) :-
    sumar_pesos_match1(Edad, Estrato, Carrera, Genero, Id, P1),
    sumar_pesos_match2(Edad, Estrato, Carrera, Genero, Id, P2),
    sumar_pesos_match3(Edad, Estrato, Carrera, Genero, Id, P3),
    Puntaje is P1 + P2 + P3.

% Obtener todos los IDs únicos con algún match
coctel_posible(Id) :-
    calificacion(_, _, _, _, Id, _).

% Recolectar puntajes
recolectar_puntajes(Edad, Estrato, Carrera, Genero, Lista) :-
    setof(Puntaje-Id, (coctel_posible(Id), puntaje_total(Edad, Estrato, Carrera, Genero, Id, Puntaje)), ListaOrdenada),
    reverse(ListaOrdenada, ListaDesc),
    extraer_top(ListaDesc, Lista).

% Extraer top 3
extraer_top([], []).
extraer_top([_-Id1], [Id1]).
extraer_top([_-Id1, _-Id2], [Id1, Id2]).
extraer_top([_-Id1, _-Id2, _-Id3|_], [Id1, Id2, Id3]).

% --------------------------------
% Regla principal
% --------------------------------

recomendar_cocteles(Edad, Estrato, Carrera, Genero, ListaTop) :-
    recolectar_puntajes(Edad, Estrato, Carrera, Genero, ListaTop).
