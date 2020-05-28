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
        #self.resultados


    def _procesar_evento_llegada_paciente(self):
        self.tiempo = self.eventos_futuros.tpllp
        self.eventos_futuros.tpllp = self.tiempo + variables.datos.intervalo_arribo_pacientes()
        self.var_estado.cpe += 1


    def _procesar_evento_fallecimiento(self):

        def liberar_respirador():
            pacientes_respirador = [paciente for paciente in self.var_estado.tptr if paciente != self.config['high_value']]
            self.var_estado.tptr[random.choice(pacientes_respirador)] = self.config['high_value']
        
        self.tiempo = self.eventos_futuros.tpf      
        self.eventos_futuros.tpf = self.tiempo + variables.datos.intervalo_fallecimiento()
        if self.var_estado.cru > 0:
            self.var_estado.cru -= 1
            liberar_respirador()


    def _procesar_evento_test_pcr(self):
        

        def obtener_pacientes_respirador_a_testear(cant_max_pacientes: int) -> [int]:
            pacientes_seleccionados = []

            for i, tiempo in enumerate(self.var_estado.tptr):
                if len(pacientes_seleccionados) >= cant_max_pacientes: # No puedo seguir tomando pacientes, llegue al maximo
                    break

                if tiempo <= self.tiempo:
                    # Deberian hacerse el test
                    pacientes_seleccionados.append(i)

            return pacientes_seleccionados


        def testear_pacientes_respirador(pacientes: [int]) -> None:
            for i in pacientes:
                if random.random() <= 0.6:
                    # Dio positivo
                    self.var_estado.tptr[i] = self.tiempo + 10080 # Otro test en 7 dias
                else:
                    # Dio negativo, se va a su casa
                    self.var_estado.cru -= 1
                    self.var_estado.tptr[i] = self.config['high_value']


        def obtener_pacientes_cama_a_testear(cant_max_pacientes: int) -> [int]:
            pacientes_seleccionados = []

            for i, tiempo in enumerate(self.var_estado.tptc):
                if len(pacientes_seleccionados) >= cant_max_pacientes: # No puedo seguir tomando pacientes, llegue al maximo
                    break

                if tiempo <= self.tiempo:
                    # Deberian hacerse el test
                    pacientes_seleccionados.append(i)

            return pacientes_seleccionados


        def testear_pacientes_cama(pacientes: [int]) -> None:
            for i in pacientes:
                if random.random() <= 0.6:
                    # Dio positivo, entonces se queda y se programa otro test para dentro de 7 dias
                    self.var_estado.tptc[i] = self.tiempo + 10080 # Otro test en 7 dias
                else:
                    # Dio negativo, se va a su casa
                    self.var_estado.ccu -= 1
                    self.var_estado.tptc[i] = self.config['high_value']


        def testear_pacientes_guardia_medica(cant_pacientes: int) -> None:
            for _ in range(cant_pacientes):
                if random.random() <= 0.1:
                    # Dio positivo, entonces se interna
                    if random.random() <= 0.02:
                        # Respirador
                        if self.var_estado.cru >= self.var_control.cant_respiradores:
                            # No hay respirador disponible
                            # TODO: resultados
                            pass
                        else:
                            self.var_estado.cru += 1
                            # Busco 1er respirador disponible
                            for i, tiempo in enumerate(self.var_estado.tptr):
                                if tiempo == self.config['high_value']:
                                    #Disponible
                                    self.var_estado.tptr[i] = self.tiempo + 10080 # Programo otro test para dentro de 7 dias
                                    break
                    else:
                        # Cama
                        if self.var_estado.ccu >= self.var_control.cant_camas:
                            # No hay cama disponible
                            # TODO: resultados
                            pass
                        else:
                            self.var_estado.ccu += 1
                            # Busco 1er cama disponible
                            for i, tiempo in enumerate(self.var_estado.tptc):
                                if tiempo == self.config['high_value']:
                                    #Disponible
                                    self.var_estado.tptc[i] = self.tiempo + 10080 # Programo otro test para dentro de 7 dias
                                    break


        self.tiempo = self.eventos_futuros.tpt
        self.eventos_futuros.tpt = next(self.eventos_futuros.tpt_iter)

        if self.var_estado.cpe >= 12:
            # El test solamente tiene pacientes esperando su 1er test
            self.var_estado.cpe -= 12
            cant_pacientes_guardia_medica_para_test = 12
        else:
            # Hay tanto pacientes nuevos como internados para el test
            cant_pacientes_guardia_medica_para_test = self.var_estado.cpe
            self.var_estado.cpe = 0

            cant_max_pacientes_respirador_para_test = 12 - cant_pacientes_guardia_medica_para_test
            pacientes_respirador_a_testear = obtener_pacientes_respirador_a_testear(cant_max_pacientes_respirador_para_test)
            testear_pacientes_respirador(pacientes_respirador_a_testear)
            
            cant_max_pacientes_cama_para_test = 12 - cant_pacientes_guardia_medica_para_test - len(pacientes_respirador_a_testear)
            pacientes_cama_a_testear = obtener_pacientes_cama_a_testear(cant_max_pacientes_cama_para_test)
            testear_pacientes_cama(pacientes_cama_a_testear)

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
        
        return variables.resultado.ResultadoSimulacion(pct_personas_que_no_pudieron_ser_internadas_por_falta_de_cama=0)