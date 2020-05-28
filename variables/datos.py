def intervalo_arribo_pacientes() -> int:
    return 150 # TODO: hacer fdp


def intervalo_fallecimiento() -> int:
    return 2000 # TODO: hacer fdp


def tiempo_prox_test_pcr() -> int:
    tiempo_prox_turno = 630 # A las 10:30, y la simulacion habia empezado a las 00:00

    avances_de_tiempo = [210, 210, 1020] # Minutos que hay entre los 3 turnos
    subindice_avances_de_tiempo = 0

    while True:
        yield tiempo_prox_turno
        tiempo_prox_turno += avances_de_tiempo[subindice_avances_de_tiempo]
        subindice_avances_de_tiempo = (subindice_avances_de_tiempo + 1) % 3