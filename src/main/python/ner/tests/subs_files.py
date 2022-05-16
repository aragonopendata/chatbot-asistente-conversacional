#crea un archivo nuevo con las lineas del primer archivo que no estan en el segundo

text1 = open("../resources/apellidos_poco_frecuentes3.txt", encoding="utf8").readlines()
text2 = open("../resources/paisesycapitales.txt", encoding="utf8").readlines()


set2 = set(text2)

lineas=[]
for line in text1:
   linelower= line.lower()
   if linelower not in set2:
       lineas.append(line)

with open("../resources/apellidos_poco_frecuentes4.txt", 'w', encoding="utf8") as file_out:
    for item in lineas:
        file_out.write(item)

