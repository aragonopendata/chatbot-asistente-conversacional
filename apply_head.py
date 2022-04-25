'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
from pathlib import Path
import glob, os


filenames = [path for path in Path('./').rglob('*.py')]

#print (filenames )

#exit(0)

for fname in filenames:
  with open('head.txt', 'r' ,encoding="utf8") as copying:
    with  open(fname , 'r+' ,encoding="utf8" ) as outfile:
      old = outfile.read()
      head = copying.read()
      if( head not in old  ):
        print (f"insert header in {fname}")
        outfile.seek(0)
        outfile.write(head)
        outfile.write(old)

