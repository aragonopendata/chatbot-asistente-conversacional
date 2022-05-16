from flask import Flask,request, jsonify
import re
import json
#Configurations
from configuration.config_json import Config
#Datasets
from data.conll import CoNLLDataset
#Models
from model.sequence_tagging.ner_model import NERModel
#import pytest
import jpype
from datetime import datetime, timedelta
from dateutil import parser
from dateutil.tz import tzlocal
from duckling import Duckling, Dim, Language
import sys
from gevent.pywsgi import WSGIServer
import copy


duckling=None
config=None
app = Flask(__name__)
dictionaries=[]

def str2bool(v):
   return v.lower() in ("yes", "true", "t", "1")

@app.route("/ner",  methods=["GET","POST"])
def evaluate_api():
    words = ""
    other = False
    duck=False
    plain=False


    if request.method == "POST":
        request_json = request.get_json()
        words = request_json.get('words')

    else:
        words = request.args['words']
    try:
        other = str2bool(request.args['other'])
    except:
        other = False;
    try:
        duck = str2bool(request.args['duck'])
    except:
        duck = False;

    try:
       plain = str2bool(request.args['plain'])
    except:
       plain = False;

    return jsonify(evaluate(words,other,duck,plain=plain))


def extractNotFoundText(value,start, validEntities):
    toReturn=[]
    validEntities.sort(key=lambda x: x['start'])
    currentStart=start
    currentEnd=start
    for ent in validEntities:
        if currentStart==currentEnd:
            if ent["start"]>currentStart:
                entity={}
                entity["start"]=currentEnd
                entity["end"] =ent["start"]
                entity["entity"] = "other"
                entity["value"] = value[currentEnd-start:ent["start"]-start]
                currentStart = ent["start"]
                toReturn.append(entity)
            currentEnd = ent["end"]
        elif ent["start"]<currentEnd:
            currentEnd = ent["end"]
        else:
            entity = {}
            entity["start"] = currentEnd
            entity["end"] = ent["start"]
            entity["entity"] = "other"
            entity["value"] = value[currentEnd - start:ent["start"] - start]
            currentStart = ent["start"]
            currentEnd = ent["end"]
            toReturn.append(entity)

    if currentEnd-start<len(value): #añadimos el texto del final a una entity other
        entity = {}
        entity["start"] = currentEnd
        entity["entity"] = "other"
        entity["value"] = value[currentEnd - start:]
        entity["end"] = currentEnd + len(entity["value"])
        toReturn.append(entity)

    return toReturn


def buscarRegex(words, pattern, startindex, stopwords,entityname,fullmatch=False):
      results=[]

      if fullmatch:
        match = re.match(pattern, words.strip())
        if match!= None:
            textmatched=match.group()
            currentindex = words.find(textmatched, 0)
            currententity = {}
            currententity["start"] = startindex + currentindex
            currententity["entity"] = entityname
            currententity["value"] = textmatched
            eIndex = currentindex + len(textmatched)
            currententity["end"] = startindex + eIndex
            currententity["confidence"] = 1.0
            lastindex = eIndex
            results.append(currententity)
      else:
        foundlist = re.findall(pattern, words)

        if foundlist is not None and foundlist != []:
          lastindex = 0
          for res in foundlist:
              resStripped=res.strip()
              if resStripped.lower() not in stopwords:
                  currentindex = words.find(resStripped, lastindex)
                  currententity = {}
                  currententity["start"] = startindex + currentindex
                  currententity["entity"] = entityname
                  currententity["value"] = resStripped
                  eIndex = currentindex + len(resStripped)
                  currententity["end"] = startindex + eIndex
                  currententity["confidence"] = 1.0

                  lastindex = eIndex
                  results.append(currententity)

      return results,extractNotFoundText(words,startindex,results)




def evaluate(words,other,duck,plain):
    global model

    respuesta = {}
    entities = []
    entitiesOther=[]
    wordIndex = 0
    startindex = 0
    currententity = {}
    currenttext = ""

    # dividimos el texto en frases separadas por punto
    words_point = words.strip().split("\n")

    # foundlist = buscarEnDiccionario(words, dict_pob, 0)
    phraseindex=0
    print(words)
    for phrase in words_point:
        #print(phraseindex)
        phraseindex = phraseindex+1
        words_raw = re.split('(\W+)', phrase)
        #words_raw = re.split('([a-zA-Z0-9_üñÑÇçÜ\\-ÁÉÍÓÚáéíóúü\\.]+)', phrase)
        # words_raw = words.strip().split(" ")
        #si el numero de palabras es menor de 7 (incluidos espacios y signos de puntuacion) buscamos en los diccionarios
        if len(words_raw) < 7:
            startindex = words.find(phrase, startindex)
            inDict, notInDict = buscarEnDiccionario(phrase, dictionaries, startindex)
            if inDict != []:
                entities.extend(inDict)
            if notInDict != []:
                entities.extend(notInDict)

            startindex=  startindex + len(phrase)
        else:
            try:
                preds,score = model.get_predictions(words_raw,
                                                word2idx=config.word2idx,
                                                char2idx=config.char2idx)
            except Exception:
                print("An exception occurred "+ Exception)
                # {"B-LOC": 0, "O": 1, "B-ORG": 2, "B-PER": 3, "I-PER": 4, "B-MISC": 5, "I-ORG": 6, "I-LOC": 7, "I-MISC": 8}
            for pred in preds:
                t = words_raw[wordIndex]
                wordIndex = wordIndex + 1

                if pred.startswith("I"):
                    currenttext = currenttext + t
                elif pred.startswith("B"):
                    if currententity != {}:
                        currententity["value"] = currenttext
                        startindex = words.find(currenttext, startindex)
                        currententity["start"] = startindex
                        currententity["end"] = startindex + len(currenttext)
                        startindex = currententity["end"]

                        if currententity["entity"] == "other":
                            entitiesOther.append(currententity)
                            # if currenttext.strip() != "," and dictionaries!= None:
                            #     foundlist = buscarEnDiccionario(currenttext, dictionaries, startindex)
                            #     entities.extend(foundlist)
                        else:
                            entities.append(currententity)

                    currententity = {}
                    currenttext = t;
                    currententity["confidence"] = score
                    currententity["start"] = 0
                    if pred == "B-LOC":
                        currententity["entity"] = "location"
                    elif pred == "B-ORG":
                        currententity["entity"] = "organization"
                    elif pred == "B-PER":
                        currententity["entity"] = "person"
                    elif pred == "B-MISC":
                        currententity["entity"] = "misc"
                else:
                    if currententity != {} and currententity["entity"] != "other":
                        currententity["value"] = currenttext
                        startindex = words.find(currenttext, startindex)
                        currententity["start"] = startindex
                        currententity["end"] = startindex + len(currenttext)
                        startindex = currententity["end"]
                        entities.append(currententity)
                        currententity = {}
                        currenttext = ""
                    currententity["confidence"] = score
                    currententity["entity"] = "other"
                    currenttext = currenttext + t

        if currententity != {}:
           #
            #if currenttext.endswith("."):
             #   currenttext = currenttext[0:len(currenttext) - 2]
            #currenttext = currenttext.strip()
            currententity["value"] = currenttext
            startindex = words.find(currenttext, startindex)
            currententity["start"] = startindex
            currententity["end"] = startindex + len(currenttext)

            if currententity["entity"] == "other":
                entitiesOther.append(currententity)
            else:
                entities.append(currententity)

            currenttext = ""
        wordIndex = 0
        currententity = {}
        currenttext = "";


    # Buscamos en diccionarios cuando entity=="other"

    notfoundlist = []
    inDict=[]
    notInDict=[]


    for ot in entitiesOther:
        inDict,notInDict=buscarEnDiccionario(ot["value"], dictionaries, ot["start"])
        if inDict != []:
            entities.extend(inDict)
        if notInDict != []:
            notfoundlist.extend(notInDict)

    #separamos en dos listas para hacer mas postprocesado, si no se busca mas se puede añadir en la misma lista

    #buscamos las entities misc en los diccionarios
    entities=replaceEntitiesWithDictionary(entities,dictionaries,"misc")

    entitiesOther = notfoundlist




    notfoundlist = []

    stopwords=[] # por el momento no lo usamos
    pattern=" ([A-ZÑÇÜÁÉÍÓÚ]+[A-Za-z0-9ÑÇÜÁÉÍÓÚáéíóúüçñ\\-_]*)" #problema al
    for ot in entitiesOther:
        inDict = []
        notInDict = []
        if ot["value"]!=" ":
            inDict,notInDict=buscarRegex(ot["value"], pattern, ot["start"],stopwords,"regex")
            if inDict != []:
                entities.extend(inDict)
            if notInDict != []:
                notfoundlist.extend(notInDict)
        else:
            notfoundlist.append(ot)

    entitiesOther = notfoundlist

    notfoundlist = []
    if duck == True:  # buscamos utilizando la libreria duckling despues de buscar nombres con -

        for ot in entitiesOther:
            found, notfound = buscarDucklingEntities(ot["value"], ot["start"])
            if found != []:
                entities.extend(found)
            if notfound != []:
                notfoundlist.extend(notfound)

        entitiesOther = notfoundlist



    notfoundlist=[]
    #buscamos subdominios
    pattern = "^(\\.([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\\-]*[a-zA-Z0-9])+)+"
    for ot in entitiesOther:
        inDict = []
        notInDict = []
        if ot["value"] != " ":
            inDict, notInDict = buscarRegex(ot["value"], pattern, ot["start"], stopwords, "domain",True)
            if inDict != []:
                entities.extend(inDict)
            if notInDict != []:
                notfoundlist.extend(notInDict)
        else:
            notfoundlist.append(ot)


    if notfoundlist != []:
        entities.extend(notfoundlist);

    if entities!=[]:
        entities.sort(key=lambda x: x['start'])



    ## recorremos la entities para fusionar entities consecutivas del mismo tipo que tengan entre ella las cadenas " de la "," del "," de "," de las "," de los "," "
    ##hacemos varias pasadas hasta que no se habga ninguna fusion

    numFusion = 0;
    while True:
        entitiesProcessed = []
        firstentity = {}
        secondentity = {}
        currenttext = ""
        numFusion = 0;
        if entities != []:
            entities.sort(key=lambda x: x['start'])

        for ent in entities:
            if firstentity!={}:
                if secondentity=={}:
                    # if  firstentity["entity"] == "extra":
                    #     if ent["entity"] != "other":
                    #         ent["entityold"] = ent["entity"]
                    #         ent["entity"] = "location"
                    #
                    #     entitiesProcessed.append(firstentity)
                    #     entitiesProcessed.append(ent)
                    #     firstentity = {}
                    # else:
                    if ent["entity"]=="other" and ent["value"] in [" de la "," del "," de "," de las "," de los "," "]:
                            secondentity=ent
                    elif firstentity["entity"]=="organization" and ent["entity"]=="domain":
                        entitiesProcessed.append(fusionarEntities(firstentity, ent))
                        numFusion += 1
                        firstentity = {}
                    elif firstentity["entity"] == "location" and ent["entity"] != "other" and ent["value"][0]!=" " : # para detectar nombres con guiones
                        entitiesProcessed.append(fusionarEntities(firstentity, ent,None,True))
                        numFusion += 1
                        firstentity = {}
                    else:
                        entitiesProcessed.append(firstentity)
                        entitiesProcessed.append(ent)
                        firstentity={}
                elif firstentity["entity"] == ent["entity"] and secondentity["value"] ==" ":
                    entitiesProcessed.append(fusionarEntities(firstentity, secondentity, ent, True))
                    numFusion += 1
                    firstentity = {}
                    secondentity = {}

                elif (firstentity["entity"] == "location" and secondentity["value"]==" " and ( ("entityold" in firstentity and firstentity["entityold"] == "regex" and ent["entity"]=="location") or ent["entity"]=="regex")):
                    entitiesProcessed.append(fusionarEntities(firstentity, secondentity, ent,False))
                    numFusion += 1
                    firstentity = {}
                    secondentity = {}
                elif firstentity["entity"] == ent["entity"] and firstentity["entity"]!="regex":
                    if firstentity["entity"]=="organization" and firstentity["value"].lower() in ["ayuntamiento","comarca","universidad","diputacion","diputación","gobierno","municipio","ciudad"]:
                        ent["entity"]="location"
                    entitiesProcessed.append(fusionarEntities(firstentity,secondentity,ent,True))
                    numFusion += 1
                    firstentity={}
                    secondentity={}
                elif firstentity["entity"] =="organization" and  ent["entity"]=="location" and secondentity["value"] in [" del "," de ", " de la "]:
                    entitiesProcessed.append(fusionarEntities(firstentity, secondentity, ent,True))
                    numFusion += 1
                    firstentity = {}
                    secondentity = {}
                elif firstentity["entity"] == "person" and ent["entity"] == "misc" and secondentity["value"] in [" de "]:
                    entitiesProcessed.append(fusionarEntities(firstentity, secondentity, ent,True))
                    numFusion += 1
                    firstentity = {}
                    secondentity = {}
                elif firstentity["entity"] == "person" and ent["entity"] == "location" and secondentity["value"] in [" del "," de ", " de la "]:
                    entitiesProcessed.append(fusionarEntities(firstentity, secondentity, ent,True))
                    numFusion += 1
                    firstentity = {}
                    secondentity = {}
                elif firstentity["entity"] == "location" and (ent["entity"] == "misc" or ent["entity"] == "regex") and secondentity["value"] in [" del ", " de ", " de la "]:
                    entitiesProcessed.append(fusionarEntities(firstentity, secondentity, ent, True))
                    numFusion += 1
                    firstentity = {}
                    secondentity = {}
                elif firstentity["entity"] == "person" and ent["entity"] == "organization" and secondentity["value"] in [" del "," de ", " de la "]:
                    entitiesProcessed.append(fusionarEntities(firstentity, secondentity, ent,True))
                    numFusion += 1
                    firstentity = {}
                    secondentity = {}
                else:
                    if firstentity["entity"] == "extra" and secondentity["value"] in [" "," del "," de ", " de la "]:
                        if ent["entity"] != "other" and ent["entity"] != "location" :
                            entitiesProcessed.append(fusionarEntities(firstentity, secondentity, ent, True))
                            numFusion += 1
                            firstentity = {}
                            secondentity = {}
                        else:
                            entitiesProcessed.append(firstentity)
                            entitiesProcessed.append(secondentity)
                            firstentity=ent
                            secondentity = {}
                    elif firstentity["entity"] == "regex" and secondentity["value"] in [" ", " del ", " de ", " de la "]:
                        entitiesProcessed.append(fusionarEntities(firstentity, secondentity, ent, True))
                        numFusion += 1
                        firstentity = {}
                        secondentity = {}
                    else:
                        entitiesProcessed.append(firstentity)
                        entitiesProcessed.append(secondentity)
                        firstentity=ent
                        secondentity = {}

            elif ent["entity"]!="other":
                firstentity=ent
            else:
                entitiesProcessed.append(ent)
                #print(ent["value"])
                #print(duckling.parse(ent["value"],language=Language.SPANISH))

        #añadimos el resto
        if firstentity != {}:
            entitiesProcessed.append(firstentity)
            if secondentity != {}:
                entitiesProcessed.append(secondentity)

        entities = copy.deepcopy(entitiesProcessed)
        if numFusion == 0:
            break

    #eliminamos other si no se ha pedido
    # y buscamos en duckling fechas y dinero

    #entitiesOther=copy.deepcopy(entities)
    entitiesOther=list(filter(lambda x: x['entity'] == "other", entities))
    entities=list( filter(lambda x: x['entity'] != "other", entities) ) # añadimos las entidades encontradas distintas de other
    #filter(lambda x: x['entity'] == "other", entitiesOther)






    respuesta["value"] = words
    nlp = formatAsNLP(entities, entitiesOther)
    if plain:
        entities= extraerSubSentities(copy.deepcopy(entities),0,other)
    if other:
        entities.extend(entitiesOther)

    if entities!=[]:
        entities.sort(key=lambda x: x['start'])

    #ponemos tipo a las entities temporales
    for ent in entities:
        if ent["entity"] == "regex":
            ent["entity"]="misc"
        elif ent["entity"] == "extra":
            ent["entity"] = "location"


    respuesta["entities"] = entities
    respuesta["nlp"] = nlp
    return respuesta  # json.dumps(respuesta, ensure_ascii=False).encode('utf8')



def formatAsNLP(entities, entitiesOther):
    translatedict = {'organization': 'ORG', 'person': 'PER', 'location': 'LOC', 'other': 'O', 'time': 'TIME',
                     'duration': 'DUR', 'email': 'EMAIL', 'amount-of-money': 'MONEY', 'misc': 'MISC',"regex":"MISC","number":"NUMBER","domain":"MISC"}
    entitiesnlp = copy.deepcopy(entities)
    entitiesnlp.extend(entitiesOther)
    nlpoutput = []
    start=-1
    end = -1
    if entitiesnlp != []:
        entitiesnlp.sort(key=lambda x: x['start'])
        for ent in entitiesnlp:
            entity = ent["entity"]
            if entity=="regex": #cambiamos regex por misc
                entity = "misc"
                ent["entity"] = "misc"
                ent["regex"] = True
            currentStart=ent["start"]
            currentEnd = ent["end"]
            if (currentStart<=start or currentStart<end): #descartamos la entity porque ya hemos metido una esto se debe a duckling
                continue
            start=currentStart
            end = currentEnd
            value =ent["value"]
            value=value.strip()
            if entity == "email":
                nlpoutput.append((value, "B-" + translatedict[entity]))
            elif entity == "amount-of-money":
                words = re.split('([\\s\\$€])',value)
                iterwords = iter(words)
                prev = next(iterwords)
                while prev.strip() == "":
                    prev = next(iterwords)
                    if prev==None:
                        break

                if  prev!=None:
                    nlpoutput.append((prev.strip(), "B-" + translatedict[entity]))
                    for w in iterwords:
                        if w.strip() != "":
                           nlpoutput.append((w.strip(), "I-" + translatedict[entity]))
            elif value!="":
                words = re.split('\\s+',value)
                iterwords = iter(words)
                prev = next(iterwords)
                while prev.strip() == "":
                    prev = next(iterwords)
                    if prev==None:
                        break

                if  prev!=None:

                    if entity=="other" or entity=="extra":
                        #Si es del tipo E. se deja tal cual
                        charDot = re.match("^[a-zA-Z]\\.",prev.strip())
                        if charDot is not None:
                            nlpoutput.append((prev.strip(), translatedict["other"]))
                        else:
                            otherWords = re.split('([\\s\\.\\,%&?¿!])',prev.strip())
                            for ow in otherWords:
                                if ow.strip() != "":
                                    nlpoutput.append((ow.strip(), translatedict["other"]))
                    else:
                        nlpoutput.append((prev.strip(), "B-" + translatedict[entity]))

                    for w in iterwords:
                        if w.strip() != "":
                            if entity == "other" or entity=="extra":
                                if charDot is not None:
                                    nlpoutput.append((w.strip(), translatedict["other"]))
                                else:
                                    otherWords=re.split('([\\s\\.\\,;:%&?¿!])',w)
                                    for ow in otherWords:
                                        if ow.strip() != "":
                                           nlpoutput.append((ow.strip(), translatedict["other"]))
                            else:
                                nlpoutput.append((w.strip(), "I-" + translatedict[entity]))
    return nlpoutput



def fusionarEntities(firstentity,secondentity,thirdentity=None,nested=False):
    new_entity = copy.deepcopy(firstentity)

    if nested:
        if "entities" not in new_entity:
            new_entity["entities"] = []
        new_entity["entities"].append(copy.deepcopy(firstentity))
        new_entity["entities"].append(copy.deepcopy(secondentity))
        if thirdentity is not None:
            new_entity["entities"].append(copy.deepcopy(thirdentity))

    new_entity["value"] += secondentity["value"]
    if thirdentity is not None:
        new_entity["value"] += thirdentity["value"]
    try:
        new_entity["confidence"] = (firstentity["confidence"] + thirdentity["confidence"]) / 2
    except Exception:
        new_entity["confidence"] = firstentity["confidence"]

    new_entity["end"] = new_entity["start"] + len(new_entity["value"])
    new_entity["fusion"] = True
    return  new_entity



def extraerSubSentities(entities,depth=0,other=False):
    toreturn= []
    for ent in entities:
        if (ent["entity"]=="other" and other==False):
            continue
        new_entity = copy.deepcopy(ent)
        new_entity["depth"]=depth
        if ("entities" in new_entity):
            toreturn.extend(extraerSubSentities(new_entity["entities"],depth+1,other))
            del new_entity["entities"]
        toreturn.append(new_entity)

    return  toreturn;


def replaceEntitiesWithDictionary(entities,dictionarylist,entitytype):
    a, b = 'áéíóú', 'aeiou'
    trans = str.maketrans(a, b)
    toreturn = []
    for ent in entities:
        if (ent["entity"] == entitytype):
            for name, dictionary, minusculas in dictionarylist:
                textclean = ent["value"]
                if minusculas == "True":
                    textclean = textclean.lower()
                if textclean in dictionary:
                    ent["entity"]=name
                    ent["dictionary"] = name
                    break

        toreturn.append(ent)

    return (toreturn)



    #devuelve dos lista una con lo encontrado y otra con lo no encontrado
def buscarEnDiccionario(words,dictionarylist,startindex):
    a, b = 'áéíóú', 'aeiou'
    trans = str.maketrans(a, b)


    words_space =re.split("(\\W+)",words)    #words.strip().split(" ")
    wordcount=len(words_space)
    sIndex=0
    eIndex=0
    wordindex=0
    num=wordcount
    foundlist=[]
    otherlist=[]
    results = []
    #buscamos los ngramas de longitud=num hasta longitud=1 desde es principio al final del texto
    while wordindex<wordcount:
        found=False
        while num>0 and found==False:
            currentword="".join(words_space[wordindex:wordindex+num]).strip()
            for name,dictionary,minusculas in dictionarylist:
                textclean=currentword.translate(trans) # quitamos las tildes
                if minusculas == "False":
                    if textclean in dictionary:
                        found = True
                        wordindex = wordindex + num
                        foundlist.append((name, currentword))
                        break
                elif minusculas=="True" :
                    textclean = textclean.lower() # pasamos a minusculas sin tildes
                    if textclean in dictionary:
                        found=True
                        wordindex=wordindex+num
                        foundlist.append((name,currentword))
                        break

            num=num-1
        if found==False:
           wordindex=wordindex+1
        num=wordcount-wordindex
    # a partir de los resultados construimos los objetos con la posicion

    if foundlist!=[]:
        lastindex=0
        for tipo,res in foundlist:
            currentindex=words.find(res, lastindex)
            currententity = {}
            currententity["start"] = startindex + currentindex
            currententity["entity"] = tipo
            currententity["value"] = res
            eIndex=currentindex+ len(res)
            currententity["end"] = startindex+eIndex
            currententity["dictionary"] = tipo
            currententity["confidence"] = 1.0

            if (currentindex!=lastindex) : # hay texto no detectado antes
                preventity = {}
                preventity["start"] = startindex + lastindex
                preventity["value"] = words[lastindex:currentindex]
                preventity["end"] = startindex + currentindex
                preventity["entity"] = "other"
                #if other:
                otherlist.append(preventity)
            lastindex=eIndex
            results.append(currententity)
        if eIndex<len(words): # quedan palabra no detectadas al final de la frase
            lastentity = {}
            lastentity["start"] = startindex + eIndex
            lastentity["value"] = words[eIndex:]
            lastentity["end"] = startindex + len(words)
            lastentity["entity"] = "other"
            #if other:
            otherlist.append(lastentity)
    else:
         currententity = {}
         currententity["start"] = startindex
         currententity["entity"] = "other"
         currententity["value"] = words
         currententity["end"] = startindex + len(words)
         otherlist.append(currententity)

    return results,otherlist

def buscarDucklingEntities(value,start ):
    entitiesProcessed=[]
    validEntities = []
    otherEntities=[]
    try:
        ducklingentities = duckling.parse(value, language=Language.SPANISH,
                                          dim_filter=["time", "duration", "email", "amount-of-money",
                                                      "number"])  # https://duckling.wit.ai/

        for du in ducklingentities:
            if "latent" in du:
                continue
            if du["body"] in ["un", "una", "uno"]:
                continue
            duEntity = {}
            duEntity["entity"] = du["dim"]
            duEntity["value"] = du["body"]
            duEntity["duckValue"] = copy.deepcopy(du["value"])
            duEntity["start"] = start + du["start"]
            duEntity["end"] = start + du["end"]
            duEntity["confidence"]=0.9
            validEntities.append(duEntity)  # TODO verificar que es valido

    except:
        print("Error inesperado:", sys.exc_info()[0])

    #eliminamos las entities que puedan solaparse
    validEntities.sort(key=lambda x: x['start'])
    startTemp = -1
    endTemp = -1
    entitiesToReturn=[]
    for ent in validEntities:
        currentStart = ent["start"]
        currentEnd = ent["end"]
        if ( currentStart <= startTemp or currentStart < endTemp):  # descartamos la entity  que se solapa no tenemos en cienta la longitud
            continue
        startTemp = currentStart
        endTemp = currentEnd
        entitiesToReturn.append(ent)

    # recorremos la entities para ver que texto no se ha encontrado
    otherEntities=extractNotFoundText(value,start, entitiesToReturn)

    return entitiesToReturn,otherEntities


def loadmodel(config_path="./config_ner.json"):

    global config

    config = Config(config_path)

    if config.dictionaries!=None:
         dictionariesConfig = config.dictionaries
         for dict in dictionariesConfig:
            f = open(dict[1], encoding="utf8")
            dictionary={}
            for line in f:
                dictionary[line.rstrip()] = True
            dictionaries.append((dict[0],dictionary,dict[2]))
    # creamos en un diccionario especial cuyas entidades usaremos mas adelante para saber si lo que viene despues de ella es location
    dictionaryExtra = {}
    for l in ["hotel","camping","albergue" ,"refugio","refugio de montaña","apartamento","casa rural","cafeteria","bar","restaurante","pizzeria","sidreria","tasca","pub","asador","taberna","casino","agencia de viajes","obra","museo","comarca","provincia","poblacion","municipio","localidad","ciudad","pueblo","villa","tierra"] : # añadir mas o cargar de fichero
        dictionaryExtra[l.rstrip()] = True
    dictionaries.append(("extra", dictionaryExtra, "False"))


    # build model
    global model
    model = NERModel(config)
    model.build()
    model.restore_session(config.dir_model)
    global duckling
    duckling = Duckling()
    duckling.load([Language.SPANISH])

    return config



if __name__ == "__main__":

    config_path = "./config_ner.json"
    config = loadmodel(config_path)


    #app.run(port=config.port)
    server = WSGIServer(("0.0.0.0", config.port), app)
    try:
        print(f"Serving on port {config.port}...")
        server.serve_forever()
    except Exception as e:
        print(e)
        exit(0)
