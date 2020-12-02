'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
import os
filenames = ['prueba.py']


for fname in filenames:
  with open('copying.txt', 'a' ,encoding="utf8") as copying:
    with open(fname, 'a' ,encoding="utf8") as infile:
      infile.write(copying.read())
			
		
