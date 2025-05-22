% Hecho dinámico
:- dynamic calificacion/6.

% Inserción de hechos desde Python
agregar_calificacion(Edad, Estrato, Carrera, Genero, IdCoctel, Calificacion) :-
    assertz(calificacion(Edad, Estrato, Carrera, Genero, IdCoctel, Calificacion)).

% Coincidencia exacta
usuario_match(Edad, Estrato, Carrera, Genero, Id, Cal) :-
    calificacion(Edad, Estrato, Carrera, Genero, Id, Cal).

% Relaja estrato y edad
usuario_match(Edad, Estrato, Carrera, Genero, Id, Cal) :-
    calificacion(E, Es, Carrera, Genero, Id, Cal),
    abs(E - Edad) =< 5,
    abs(Es - Estrato) =< 2.

% Relaja carrera
usuario_match(Edad, Estrato, _, Genero, Id, Cal) :-
    calificacion(E, Es, _, Genero, Id, Cal),
    abs(E - Edad) =< 5,
    abs(Es - Estrato) =< 2.

% Relaja género
usuario_match(Edad, Estrato, _, _, Id, Cal) :-
    calificacion(E, Es, _, _, Id, Cal),
    abs(E - Edad) =< 5,
    abs(Es - Estrato) =< 2.

% Promedio por cóctel
promedio_coctel_robusto(Edad, Estrato, Carrera, Genero, Id, Promedio) :-
    findall(Cal, usuario_match(Edad, Estrato, Carrera, Genero, Id, Cal), Calificaciones),
    Calificaciones \= [],
    sumlist(Calificaciones, Total),
    length(Calificaciones, N),
    Promedio is Total / N.

% Promedio general (si no hay nada)
promedio_general(Id, Promedio) :-
    findall(Cal, calificacion(_, _, _, _, Id, Cal), Calificaciones),
    Calificaciones \= [],
    sumlist(Calificaciones, Total),
    length(Calificaciones, N),
    Promedio is Total / N.

% Recolectar lista de cócteles con sus promedios (robusto)
recolectar_robusto(Edad, Estrato, Carrera, Genero, Lista) :-
    setof(Prom-Id, (promedio_coctel_robusto(Edad, Estrato, Carrera, Genero, Id, Prom), number(Id)), ListaNoOrdenada),
    reverse(ListaNoOrdenada, ListaOrdenada),
    extraer_top(ListaOrdenada, Lista), !.
recolectar_robusto(_, _, _, _, Lista) :-
    setof(Prom-Id, (promedio_general(Id, Prom), number(Id)), ListaNoOrdenada),
    reverse(ListaNoOrdenada, ListaOrdenada),
    extraer_top(ListaOrdenada, Lista), !.
recolectar_robusto(_, _, _, _, Lista) :-
    findall(Id, (calificacion(_, _, _, _, Id, _), number(Id)), TodosIds),
    random_permutation(TodosIds, Aleatorios),
    extraer_top_ids(Aleatorios, Lista), !.
recolectar_robusto(_, _, _, _, []).

% Tomar los mejores 3 de una lista ordenada Prom-Id
extraer_top([], []).
extraer_top([_-Id1], [Id1]).
extraer_top([_-Id1, _-Id2], [Id1, Id2]).
extraer_top([_-Id1, _-Id2, _-Id3|_], [Id1, Id2, Id3]).

% Tomar los primeros 3 de una lista simple de IDs
extraer_top_ids([], []).
extraer_top_ids([Id1], [Id1]).
extraer_top_ids([Id1, Id2], [Id1, Id2]).
extraer_top_ids([Id1, Id2, Id3|_], [Id1, Id2, Id3]).

% Inferencia principal
recomendar_cocteles(Edad, Estrato, Carrera, Genero, ListaTop) :-
    recolectar_robusto(Edad, Estrato, Carrera, Genero, ListaTop).
