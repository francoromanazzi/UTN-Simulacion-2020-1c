import json

from simulacion_hospital import SimulacionHospital
import variables.control
from config import Config


def main():
    with open('config.json') as json_data_file:
        config: Config = json.load(json_data_file)

    simulacion = SimulacionHospital(config)
    resultados = simulacion.ejecutar(variables.control.VariablesDeControl(cant_camas=60, cant_respiradores=30))
    print(resultados)


if __name__ == '__main__':
    main()