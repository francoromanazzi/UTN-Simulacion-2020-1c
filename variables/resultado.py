class ResultadoSimulacion:
    def __init__(self):
        self.sumatoria_llenado_muestras = 0
        self.cantidad_tests_pcr_realizados = 0
        self.cantidad_veces_que_test_no_alcanzo_para_todas_las_muestras = 0

        self.cantidad_pacientes_positivo_cama = 0
        self.cantidad_pacientes_no_pudieron_internarse_por_falta_cama = 0
        self.cantidad_pacientes_positivo_respirador = 0
        self.cantidad_pacientes_no_pudieron_internarse_por_falta_respirador = 0

        self.sumatoria_minutos_permanencia_cama = 0
        self.cantidad_pacientes_que_estuvieron_en_cama = 0
        self.sumatoria_minutos_permanencia_respirador = 0
        self.cantidad_pacientes_que_estuvieron_en_respirador = 0

        self.cantidad_fallecidos = 0


    def mostrar(self):
        print(f'Promedio de llenado de muestras de tests PCR: {self.sumatoria_llenado_muestras / self.cantidad_tests_pcr_realizados}')
        print(f'Porcentaje de veces que un test PCR no alcanzó para analizar todas las muestras: {(self.cantidad_veces_que_test_no_alcanzo_para_todas_las_muestras * 100) / self.cantidad_tests_pcr_realizados}')
        print(f'Porcentaje de personas que no se pudo internar por falta de cama: {(self.cantidad_pacientes_no_pudieron_internarse_por_falta_cama * 100) / self.cantidad_pacientes_positivo_cama}')
        print(f'Porcentaje de personas que no se pudo internar por falta de respirador: {(self.cantidad_pacientes_no_pudieron_internarse_por_falta_respirador * 100) / self.cantidad_pacientes_positivo_respirador}')
        print(f'Cantidad fallecidos: {self.cantidad_fallecidos}') #TODO: sacar
        print(f'Promedio de permanencia en una cama de una persona: {(self.sumatoria_minutos_permanencia_cama / self.cantidad_pacientes_que_estuvieron_en_cama) / 60} horas')
        print(f'Promedio de tiempo de uso de un respirador de una persona: {(self.sumatoria_minutos_permanencia_respirador / self.cantidad_pacientes_que_estuvieron_en_respirador) / 60} horas')
