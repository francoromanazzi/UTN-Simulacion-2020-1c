import variables.control
from config import Config


class VariablesDeEstado:
    def __init__(self, config: Config, var_control: variables.control.VariablesDeControl):
        self.cpe = 0 # Cantidad de pacientes esperando resultados de primer test
        self.ccu = 0 # Cantidad de camas en uso
        self.tptc = [config['high_value']] *  var_control.cant_camas # Tiempo de próximo test PCR del paciente en cama(i)
        self.cru = 0 # Cantidad de respiradores en uso
        self.tptr = [config['high_value']] *  var_control.cant_respiradores # Tiempo de próximo test PCR del paciente usando respirador(i)