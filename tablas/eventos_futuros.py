from variables.datos import intervalo_arribo_pacientes, tiempo_prox_test_pcr


class EventosFuturos:
    def __init__(self):
        self.tpllp = intervalo_arribo_pacientes()
        self.tpt_iter = tiempo_prox_test_pcr()
        self.tpt = next(self.tpt_iter)