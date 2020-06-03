import json

from simulacion_hospital import SimulacionHospital
import variables.control
from config import Config


def main():
    with open('config.json') as json_data_file:
        config: Config = json.load(json_data_file)

    simulacion = SimulacionHospital(config)
    camas, respiradores = 80, 7
    print(camas, respiradores)
    resultados = simulacion.ejecutar(variables.control.VariablesDeControl(cant_camas=camas, cant_respiradores=respiradores))
    resultados.mostrar()


if __name__ == '__main__':
    main()