import math
#from scipy.special import erfinv
#from sympy.functions.special.error_functions import erfinv, erf
import random
from scipy.stats import fatiguelife, norm


# ------------------------------------- fdps -------------------------------------

def intervalo_arribo_pacientes() -> int:
    return fatiguelife.rvs(2.6377, loc=0.20048, scale=18.233)


def intervalo_fallecimiento() -> int:
    return norm.rvs(loc=45360, scale=8000)


# print(intervalo_fallecimiento())
# print(intervalo_fallecimiento())
# print(intervalo_fallecimiento())
# print(intervalo_fallecimiento())
# print(intervalo_fallecimiento())
# print(intervalo_fallecimiento())
# print(intervalo_fallecimiento())
# print(intervalo_fallecimiento())

# --------- A partir de aca no son fdps pero son "datos" del problema ------------

def tiempo_prox_test_pcr() -> int:
    tiempo_prox_turno = 630 # A las 10:30, y la simulacion habia empezado a las 00:00

    avances_de_tiempo = [210, 210, 1020] # Minutos que hay entre los 3 turnos
    subindice_avances_de_tiempo = 0

    while True:
        yield tiempo_prox_turno
        tiempo_prox_turno += avances_de_tiempo[subindice_avances_de_tiempo]
        subindice_avances_de_tiempo = (subindice_avances_de_tiempo + 1) % 3