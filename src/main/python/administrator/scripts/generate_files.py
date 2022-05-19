"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
"""
Main application to create files from mongodb needed to handle data
for projects, models, intent, entities, stories and interactions
recreate training_data.yml
recreate rules.yml
"""

from trainer import RasaTrainer
from mongo_connector import projects, stories, entities, intents
project_id = projects.read_project_id_from_name("GDA")
model_id = projects.read_model_id_from_name("AOD")
rasa_trainer = RasaTrainer(project_id=project_id, model_id=model_id)
try:
    rasa_trainer.generate()
except:
    pass