'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
"""
Script to train a model, at the moment, the project and model
are hardcoded because we work with only one project.

The project 'GDA' and model 'AOD' is always merged with the
'smalltalk' project
"""
from pprint import pprint

from mongo_connector import projects
from trainer import RasaTrainer


if __name__ == "__main__":
    project_id = projects.read_project_id_from_name("GDA")
    model_id = projects.read_model_id_from_name("AOD")
    rasa_trainer = RasaTrainer(project_id=project_id, model_id=model_id)
    try:
        rasa_trainer.train()
    except ValueError as val:
        print(val)
    except FileNotFoundError as fnf:
        print(fnf)
    except IsADirectoryError as err:
        print(err)
    finally:
        del rasa_trainer
