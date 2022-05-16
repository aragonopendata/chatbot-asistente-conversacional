import unittest
from apirest import evaluate,loadmodel
from configuration.config_json import Config

class MyTestCase(unittest.TestCase):
    def test_something(self):
        config_path = "./config_ner.json"
        loadmodel(config_path)
        tests = [("El 20 de diciembre me voy de vacaciones ",
                  [('El', 'B-TIME'), ('20', 'I-TIME'), ('de', 'I-TIME'), ('diciembre', 'I-TIME'), ('me', 'O'),
                   ('voy', 'O'), ('de', 'O'), ('vacaciones', 'O')]),
                 ("Para las 14:00 tengo hora con el dentista",
                  [('Para', 'O'), ('las', 'O'), ('14:00', 'B-TIME'), ('tengo', 'O'),
                   ('hora', 'O'), ('con', 'O'), ('el', 'O'), ('dentista', 'O')]),
                 ("María ha llamado por teléfono",
                  [('María', 'B-PER'), ('ha', 'O'), ('llamado', 'O'), ('por', 'O'), ('teléfono', 'O')]),
                 ("El correo de María mcrodriguez@itainnova.es",
                  [('El', 'O'), ('correo', 'O'), ('de', 'O'), ('María', 'B-PER'), ('mcrodriguez@itainnova.es', 'B-EMAIL')]),
                 ("El aeropuerto está en Madrid",
                  [('El', 'O'), ('aeropuerto', 'B-LOC'), ('está', 'O'), ('en', 'O'), ('Madrid', 'B-LOC')]),
                 ("Yo tengo 30 años", [('Yo', 'O'), ('tengo', 'O'), ('30', 'B-DUR'), ('años', 'I-DUR')]),
                 ("Las botas cuestan 60 euros",
                  [('Las', 'O'), ('botas', 'O'), ('cuestan', 'O'), ('60', 'B-MONEY'), ('euros', 'I-MONEY')]),
                 ("Las botas cuestan $60,05",
                  [('Las', 'O'), ('botas', 'O'), ('cuestan', 'O'), ('$', 'B-MONEY'), ('60,05', 'I-MONEY')]),
                 ("Las botas cuestan 60.005€",
                  [('Las', 'O'), ('botas', 'O'), ('cuestan', 'O'), ('60.005', 'B-MONEY'), ('€', 'I-MONEY')])
                ]
        for text, result in tests:
           response = evaluate(text, True, True, False)
           print(response["nlp"])

           self.assertEqual(response["nlp"], result)


if __name__ == '__main__':
    unittest.main()
