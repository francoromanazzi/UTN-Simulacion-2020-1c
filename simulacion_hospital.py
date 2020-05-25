import variables.control
import variables.estado
import variables.resultado
import variables.datos
import tablas.eventos_futuros
from config import Config


class SimulacionHospital:
    def __init__(self, config: Config):
        self.config = config
        self.tiempo = 0
        self.eventos_futuros = tablas.eventos_futuros.EventosFuturos()
        #self.resultados


    def _procesar_evento_llegada_paciente(self):
        self.tiempo = self.eventos_futuros.tpllp
        self.eventos_futuros.tpllp = self.tiempo + variables.datos.intervalo_arribo_pacientes()
        self.var_estado.cpe += 1


    def _procesar_evento_test_pcr(self):
        self.tiempo = self.eventos_futuros.tpt
        self.eventos_futuros.tpt = next(self.eventos_futuros.tpt_iter)


    def ejecutar(self, var_control: variables.control.VariablesDeControl):
        self.var_estado = variables.estado.VariablesDeEstado(self.config, var_control)

        while self.tiempo < self.config['tiempo_final']:
            if self.eventos_futuros.tpllp <= self.eventos_futuros.tpt:
                self._procesar_evento_llegada_paciente()
            else:
                self._procesar_evento_test_pcr()
        
        return variables.resultado.ResultadoSimulacion(pct_personas_que_no_pudieron_ser_internadas_por_falta_de_cama=0)