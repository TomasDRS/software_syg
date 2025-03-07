
listas = [(1, 'IMS', 'Prueba 20/02', '', '2025-02-19', '10:59:39', 'Tomás', '2025/02/21', '12:00', 'Ingeniería', '1', 'En progreso'), 
        (2, 'IMS', 'Prueba 20/02', '', '2025-02-19', '10:59:39', 'Tomás', '2025/03/01', '12:00', 'Ingeniería', '2', 'En progreso'), 
        (6, 'IMS', 'Prueba 20/02', '', '2025-02-19', '10:59:39', 'Tomás', '2025/03/01', '12:00', 'Ingeniería', '3', 'En progreso'), 
        (8, 'IMS', 'Prueba 20/02', '', '2025-02-19', '10:59:39', 'Tomás', '2025/03/01', '12:00', 'Ingeniería', '3', 'En progreso'), 
        (9, 'IMS', 'Prueba 20/02', '', '2025-02-19', '10:59:39', 'Tomás', '2025/03/01', '12:00', 'Ingeniería', '1', 'En progreso'), 
        (3, 'IMS', 'Prueba 20/02', '', '2025-02-19', '10:59:39', 'Tomás', '2025/02/20', '12:00', 'Ingeniería', '1', 'En progreso'), 
        (4, 'IMS', 'Prueba 20/02', '', '2025-02-19', '10:59:39', 'Tomás', '2025/05/05', '12:00', 'Ingeniería', '1', 'En progreso'), 
        (5, 'IMS', 'Prueba 20/02', '', '2025-02-19', '10:59:39', 'Tomás', '2025/03/15', '12:00', 'Ingeniería', '1', 'En progreso')]
listas.sort(key=lambda x: (x[7], x[10]))
for lista in listas:
    print(lista)