% -------------------------------
% DEFINICIONES DINÁMICAS
% -------------------------------

:- dynamic calificacion/6.

% -------------------------------
% INSERCIÓN DESDE PYTHON
% -------------------------------

agregar_calificacion(Edad, Estrato, Carrera, Genero, CoctelID, Calificacion) :-
    assertz(calificacion(Edad, Estrato, Carrera, Genero, CoctelID, Calificacion)).

% -------------------------------
% REGLAS DE COINCIDENCIA
% -------------------------------

% Coincidencia exacta
usuario_match_1(Edad, Estrato, Carrera, Genero, Id) :-
    calificacion(Edad, Estrato, Carrera, Genero, Id, _).

% Coincidencia con rango en edad y estrato
usuario_match_2(EdadU, EstratoU, Carrera, Genero, Id) :-
    calificacion(E, Es, Carrera, Genero, Id, _),
    abs(E - EdadU) =< 5,
    abs(Es - EstratoU) =< 2.

% Coincidencia ignorando carrera
usuario_match_3(EdadU, EstratoU, Genero, Id) :-
    calificacion(E, Es, _, Genero, Id, _),
    abs(E - EdadU) =< 5,
    abs(Es - EstratoU) =< 2.

% -------------------------------
% SUMA DE PUNTAJES POR CÓCTEL
% -------------------------------

% Acumula los puntajes de coincidencia
recolectar_puntajes(Edad, Estrato, Carrera, Genero, ListaPuntos) :-
    findall(Id, usuario_match_1(Edad, Estrato, Carrera, Genero, Id), Match1),
    findall(Id, usuario_match_2(Edad, Estrato, Carrera, Genero, Id), Match2),
    findall(Id, usuario_match_3(Edad, Estrato, Genero, Id), Match3),

    contar_puntajes(Match1, 1.0, [], P1),
    contar_puntajes(Match2, 0.5, P1, P2),
    contar_puntajes(Match3, 0.2, P2, ListaPuntos).

% Recorre lista y suma pesos
contar_puntajes([], _, Acc, Acc).
contar_puntajes([Id|Resto], Peso, Acc, Resultado) :-
    actualizar(Id, Peso, Acc, NuevoAcc),
    contar_puntajes(Resto, Peso, NuevoAcc, Resultado).

% Si ya existe el ID, suma el peso
actualizar(Id, Peso, [], [Peso-Id]).
actualizar(Id, Peso, [P0-Id|T], [P1-Id|T]) :- 
    P1 is P0 + Peso.

% Si no existe, lo deja pasar
actualizar(Id, Peso, [P0-Id0|T], [P0-Id0|Resto]) :- 
    Id \= Id0, 
    actualizar(Id, Peso, T, Resto).

% -------------------------------
% INFERENCIA FINAL
% -------------------------------

% Recomendación ordenada
recomendar_cocteles(Edad, Estrato, Carrera, Genero, ListaTop) :-
    recolectar_puntajes(Edad, Estrato, Carrera, Genero, Lista),
    sort(Lista, Ordenada),         
    reverse(Ordenada, Desc),       
    extraer_top(Desc, ListaTop).

% Extrae los 3 mejores
extraer_top([], []).
extraer_top([_-Id1], [Id1]).
extraer_top([_-Id1, _-Id2], [Id1, Id2]).
extraer_top([_-Id1, _-Id2, _-Id3|_], [Id1, Id2, Id3]).
