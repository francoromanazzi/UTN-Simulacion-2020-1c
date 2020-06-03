import random

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
        self.resultados = variables.resultado.ResultadoSimulacion()


    def _procesar_evento_llegada_paciente(self):
        self.tiempo = self.eventos_futuros.tpllp
        self.eventos_futuros.tpllp = self.tiempo + variables.datos.intervalo_arribo_pacientes()
        self.var_estado.cpe += 1


    def _procesar_evento_fallecimiento(self):

        def liberar_respirador():
            pos_pacientes_respirador = [pos_paciente for pos_paciente, paciente in enumerate(self.var_estado.tptr) if paciente != self.config['high_value']]
            pos_pacientes_que_fallece = random.choice(pos_pacientes_respirador)
            tiempo_prox_test_paciente_que_fallece = self.var_estado.tptr[pos_pacientes_que_fallece]
            self.resultados.sumatoria_minutos_permanencia_respirador -= (tiempo_prox_test_paciente_que_fallece - self.tiempo)
            self.var_estado.tptr[pos_pacientes_que_fallece] = self.config['high_value']
        
        self.tiempo = self.eventos_futuros.tpf      
        self.eventos_futuros.tpf = self.tiempo + variables.datos.intervalo_fallecimiento()
        if self.var_estado.cru > 0:
            self.var_estado.cru -= 1
            self.resultados.cantidad_fallecidos += 1
            liberar_respirador()


    def _procesar_evento_test_pcr(self):
        
        def testear_pacientes_guardia_medica(cant_pacientes: int) -> None:
            for _ in range(cant_pacientes):
                if random.random() <= 0.1:
                    # Dio positivo, entonces se interna
                    if random.random() <= 0.04:
                        # Respirador
                        self.resultados.cantidad_pacientes_positivo_respirador += 1
                        if self.var_estado.cru >= self.var_control.cant_respiradores:
                            # No hay respirador disponible
                            self.resultados.cantidad_pacientes_no_pudieron_internarse_por_falta_respirador += 1
                        else:
                            self.resultados.cantidad_pacientes_que_estuvieron_en_respirador += 1
                            self.var_estado.cru += 1
                            # Busco 1er respirador disponible
                            for i, tiempo in enumerate(self.var_estado.tptr):
                                if tiempo == self.config['high_value']:
                                    #Disponible
                                    self.var_estado.tptr[i] = self.tiempo + 10080 # Programo otro test para dentro de 7 dias
                                    self.resultados.sumatoria_minutos_permanencia_respirador += 10080
                                    break
                    else:
                        # Cama
                        self.resultados.cantidad_pacientes_positivo_cama += 1
                        if self.var_estado.ccu >= self.var_control.cant_camas:
                            # No hay cama disponible
                            self.resultados.cantidad_pacientes_no_pudieron_internarse_por_falta_cama += 1
                        else:
                            self.resultados.cantidad_pacientes_que_estuvieron_en_cama += 1
                            self.var_estado.ccu += 1
                            # Busco 1er cama disponible
                            for i, tiempo in enumerate(self.var_estado.tptc):
                                if tiempo == self.config['high_value']:
                                    #Disponible
                                    self.var_estado.tptc[i] = self.tiempo + 10080 # Programo otro test para dentro de 7 dias
                                    self.resultados.sumatoria_minutos_permanencia_cama += 10080
                                    break

        def testear_pacientes_respirador(cant_max_pacientes: int) -> int:
            cant_tests_respirador_realizados = 0
            for _ in range(cant_max_pacientes):
                for pos_paciente, tiempo_paciente in enumerate(self.var_estado.tptr):
                    if tiempo_paciente <= self.tiempo:
                        # Deberian hacerse el test
                        cant_tests_respirador_realizados += 1
                        if random.random() <= 0.8:
                            # Dio positivo, entonces se queda y se programa otro test para dentro de 7 dias
                            self.var_estado.tptr[pos_paciente] = self.tiempo + 10080 # Otro test en 7 dias
                            self.resultados.sumatoria_minutos_permanencia_respirador += 10080 + (self.tiempo - tiempo_paciente)
                        else:
                            # Dio negativo, se va a su casa
                            self.var_estado.cru -= 1
                            self.var_estado.tptr[pos_paciente] = self.config['high_value']            
            return cant_tests_respirador_realizados

        def testear_pacientes_cama(cant_max_pacientes: int) -> int:
            cant_tests_cama_realizados = 0
            for _ in range(cant_max_pacientes):
                for pos_paciente, tiempo_paciente in enumerate(self.var_estado.tptc):
                    if tiempo_paciente <= self.tiempo:
                        # Deberian hacerse el test
                        cant_tests_cama_realizados += 1
                        if random.random() <= 0.8:
                            # Dio positivo, entonces se queda y se programa otro test para dentro de 7 dias
                            self.var_estado.tptc[pos_paciente] = self.tiempo + 10080 # Otro test en 7 dias
                            self.resultados.sumatoria_minutos_permanencia_cama += 10080 + (self.tiempo - tiempo_paciente)
                        else:
                            # Dio negativo, se va a su casa
                            self.var_estado.ccu -= 1
                            self.var_estado.tptc[pos_paciente] = self.config['high_value']
            return cant_tests_cama_realizados

        self.tiempo = self.eventos_futuros.tpt
        self.eventos_futuros.tpt = next(self.eventos_futuros.tpt_iter)

        self.resultados.cantidad_tests_pcr_realizados += 1

        if self.var_estado.cpe >= 12:
            if self.var_estado.cpe > 12:
                self.resultados.cantidad_veces_que_test_no_alcanzo_para_todas_las_muestras += 1

            # El test solamente tiene pacientes esperando su 1er test
            self.var_estado.cpe -= 12
            cant_pacientes_guardia_medica_para_test = 12
            self.resultados.sumatoria_llenado_muestras += cant_pacientes_guardia_medica_para_test
        else:
            # Hay tanto pacientes nuevos como internados para el test
            cant_pacientes_guardia_medica_para_test = self.var_estado.cpe
            self.var_estado.cpe = 0

            cant_max_pacientes_respirador_para_test = 12 - cant_pacientes_guardia_medica_para_test
            cant_pacientes_respirador_testeados = testear_pacientes_respirador(cant_max_pacientes_respirador_para_test)
            
            cant_max_pacientes_cama_para_test = 12 - cant_pacientes_guardia_medica_para_test - cant_pacientes_respirador_testeados
            cant_pacientes_cama_testeados = testear_pacientes_cama(cant_max_pacientes_cama_para_test)

            self.resultados.sumatoria_llenado_muestras += cant_pacientes_guardia_medica_para_test + cant_pacientes_respirador_testeados + cant_pacientes_cama_testeados

            if any([tiempo_paciente <= self.tiempo for tiempo_paciente in (self.var_estado.tptr + self.var_estado.tptc)]):
                self.resultados.cantidad_veces_que_test_no_alcanzo_para_todas_las_muestras += 1

        testear_pacientes_guardia_medica(cant_pacientes_guardia_medica_para_test)


    def ejecutar(self, var_control: variables.control.VariablesDeControl):
        self.var_estado = variables.estado.VariablesDeEstado(self.config, var_control)
        self.var_control = var_control

        while self.tiempo < self.config['tiempo_final']:
            if self.eventos_futuros.tpllp <= self.eventos_futuros.tpt and self.eventos_futuros.tpllp <= self.eventos_futuros.tpf:
                self._procesar_evento_llegada_paciente()
            elif self.eventos_futuros.tpt <= self.eventos_futuros.tpf:
                self._procesar_evento_test_pcr()
            else:
                self._procesar_evento_fallecimiento()
        
        return self.resultados