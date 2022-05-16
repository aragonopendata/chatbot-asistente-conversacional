import re
from browser.config import Config
from browser.constants import Constants
import browser.road_issues_parser as road_issues_parser
import browser.calendar_parser as calendar_parser
import browser.calendar_parser_ics_urls as calendar_parser_ics_urls
from dateutil.relativedelta import relativedelta
import datetime
import time


class TemplatesCalendar:
    """[summary]
    """

    now = datetime.datetime.now()
    min = 2014
    max = now.year + 1
    years = range(min, max+1)

    @staticmethod
    def getYear() -> str:

        now = datetime.datetime.now()
        return now.year

    @staticmethod
    def getPlaces() -> str:

        """ This function returns list of places.

        Returns
        ---------
            places list
            """
        
        places = ["Aragón", "Huesca", "Zaragoza", "Teruel"]
        return places

    @staticmethod
    def getUrls() -> str:

        """ This function return of list of different calendar urls.
        
        Returns
        ---------
            urls list
            """
        
        urls = calendar_parser_ics_urls.parser(TemplatesCalendar.years)
        return urls

    @staticmethod
    def getNecessaryData(urls, ano):

        """ This function return the main information of the urls of a concrete year.
        Parameter
        ----------
            urls str
            ano int        
        
        Returns
        ---------
            final_results dict
            """        
        
        keys = list(urls[ano].keys())
        final_results = {}
        for key in keys:
            elements = urls[ano][key]
            results = []
            for element in elements:
                descripcion = elements[element]["description"]
                url = elements[element]["url"]
                data = {"description": descripcion, "url": url}
                results.append(data)
            final_results[key] = results
        return final_results

    @staticmethod
    def getFestivoUrl(comunidadoprovincia, ano):

        """ This function return the bank holidays of a concrete year.
        Parameter
        ----------
            comunidadoprovincia str
            ano int        
        
        Returns
        ---------
            element str
            """        
        
        text_to_find = "Festivos"
        urls = TemplatesCalendar.getUrls()
        final_results = TemplatesCalendar.getNecessaryData(urls, ano)
        keys = list(final_results.keys())
        for key in keys:
            if key.upper().find(text_to_find.upper()) > -1:
                for element in final_results[key]:
                    if (
                        element["description"].upper().find(comunidadoprovincia.upper())
                        > -1
                    ):
                        return element["url"]

    @staticmethod
    def getShortFeriasyExposicionesAndSchool(comunidadoprovincia, ano, urls=""):

        """ This function return the list of fairs of a concrete year.
        Parameter
        ----------
            comunidadoprovincia str
            ano int
            url str   
        
        Returns
        ---------
            urls_returns list
            """        
        
        texts_to_find = ["Festivos", "ferias"]
        urls_returns = []
        if urls == "":
            urls = TemplatesCalendar.getUrls()
        final_results = TemplatesCalendar.getNecessaryData(urls, ano)
        keys = list(final_results.keys())
        for text_to_find in texts_to_find:
            for key in keys:
                lista = final_results[key]
                for element in lista:
                    if element["description"].upper().find(text_to_find.upper()) > -1:
                        if text_to_find.upper() == "FERIAS":
                            urls_returns.append(element["url"])
                            break
                        else:
                            if (
                                element["description"]
                                .upper()
                                .find(comunidadoprovincia.upper())
                                > -1
                            ):
                                urls_returns.append(element["url"])
                                break
        return urls_returns

    @staticmethod
    def getFeriasyExposicionesAndSchoolCalendarUrlTipo(
        comunidadoprovincia, ano, tipo, urls=""
    ):

        """ This function return the list of fairs of a concrete year and of a concrete type.
        Parameter
        ----------
            comunidadoprovincia str
            ano int
            tipo str
            url str   
        
        Returns
        ---------
            urls_returns list
            """    

        places = TemplatesCalendar.getPlaces()
        texts_to_find = ["Festivos", "ferias"]
        urls_returns = []
        if urls == "":
            urls = TemplatesCalendar.getUrls()
        final_results = TemplatesCalendar.getNecessaryData(urls, ano)
        keys = list(final_results.keys())
        tipo = TemplatesCalendar.getReplaceTildes(tipo)
        if tipo.upper() == "ARAGON" or tipo.upper() == "":
            for text_to_find in texts_to_find:
                for key in keys:
                    lista = final_results[key]
                    for element in lista:
                        if (
                            element["description"].upper().find(text_to_find.upper())
                            > -1
                        ):
                            urls_returns.append(element["url"])
        else:
            for text_to_find in texts_to_find:
                for key in keys:
                    lista = final_results[key]
                    for element in lista:
                        if (
                            element["description"].upper().find(text_to_find.upper())
                            > -1
                        ):
                            if text_to_find.upper() == "FERIAS":
                                urls_returns.append(element["url"])
                                break
                            else:
                                if (
                                    element["description"]
                                    .upper()
                                    .find(comunidadoprovincia.upper())
                                    > -1
                                ):
                                    urls_returns.append(element["url"])
                                    break
        return urls_returns

    @staticmethod
    def getHolidayDay(data_evento, url) -> str:

        """ This function return the list of fairs names from a concrete date.
        Parameter
        ----------
            data_evento str
            url str   
        
        Returns
        ---------
            information list
            """        
        
        [eventos_aragon, eventos_aragon_dict] = calendar_parser.parser(url)
        tipoEvento = TemplatesCalendar.getUrlTag(url)
        information = []
        for evento in eventos_aragon:
            if evento["fecha_inicio"].find(data_evento) > -1:
                information.append(
                    {
                        "calendario_name": evento["calendario_name"],
                        "calendar_type": tipoEvento,
                        "nombre": evento["nombre"],
                        "descripcion": evento["descripcion"],
                        "fecha_inicio": evento["fecha_inicio"],
                        "fecha_fin": evento["fecha_fin"],
                        "localizacion": evento["localizacion"],
                    }
                )
        return information

    @staticmethod
    def getDateHolidayFromName(name_evento, url) -> str:

        """ This function return the list of dates of fairs from a concrete name.
        Parameter
        ----------
            name_evento str
            url str   
        
        Returns
        ---------
            information list
            """        
        
        [eventos_aragon, eventos_aragon_dict] = calendar_parser.parser(url)
        tipoEvento = TemplatesCalendar.getUrlTag(url)
        information = []
        for evento in eventos_aragon:
            try:
                if (
                    evento["nombre"].upper().find(name_evento.upper()) > -1
                    or evento["descripcion"].upper().find(name_evento.upper()) > -1
                ):
                    information.append(
                        {
                            "calendario_name": evento["calendario_name"],
                            "name_evento": name_evento,
                            "calendar_type": tipoEvento,
                            "nombre": evento["nombre"],
                            "descripcion": evento["descripcion"],
                            "fecha_inicio": evento["fecha_inicio"],
                            "fecha_fin": evento["fecha_fin"],
                            "localizacion": evento["localizacion"],
                        }
                    )
            except:
                if evento["nombre"].upper().find(name_evento.upper()) > -1:                    
                    information.append(
                        {
                            "calendario_name": evento["calendario_name"],
                            "name_evento": name_evento,
                            "calendar_type": tipoEvento,
                            "nombre": evento["nombre"],
                            "descripcion": evento["descripcion"],
                            "fecha_inicio": evento["fecha_inicio"],
                            "fecha_fin": evento["fecha_fin"],
                            "localizacion": evento["localizacion"],
                        }
                    )
        return information

    @staticmethod
    def getDateHolidayWhere(name_evento, url) -> str:

        """ This function return the list of places from a concrete name.
        Parameter
        ----------
            name_evento str
            url str   
        
        Returns
        ---------
            information list
            """         
        
        [eventos_aragon, eventos_aragon_dict] = calendar_parser.parser(url)
        tipoEvento = TemplatesCalendar.getUrlTag(url)
        information = []
        for evento in eventos_aragon:
            nombre = TemplatesCalendar.getReplaceTildes(evento["nombre"].upper())
            descripcion = TemplatesCalendar.getReplaceTildes(evento["descripcion"].upper())
            try:
                if (
                    nombre.upper().find(name_evento.upper()) > -1
                    or descripcion.upper().find(name_evento.upper()) > -1
                ):
                    information.append(
                        {
                            "calendario_name": evento["calendario_name"],
                            "name_evento": name_evento,
                            "calendar_type": tipoEvento,
                            "nombre": evento["nombre"],
                            "descripcion": evento["descripcion"],
                            "fecha_inicio": evento["fecha_inicio"],
                            "fecha_fin": evento["fecha_fin"],
                            "localizacion": evento["localizacion"],
                        }
                    )
            except:
                if nombre.upper().find(name_evento.upper()) > -1:
                    information.append(
                        {
                            "calendario_name": evento["calendario_name"],
                            "name_evento": name_evento,
                            "calendar_type": tipoEvento,
                            "nombre": evento["nombre"],
                            "descripcion": evento["descripcion"],
                            "fecha_inicio": evento["fecha_inicio"],
                            "fecha_fin": evento["fecha_fin"],
                            "localizacion": evento["localizacion"],
                        }
                    )
        return information

    @staticmethod
    def getHolidaysDayLocation(fecha, url) -> str:

        """ This function return the list of bank holiday of location from a concrete date.
        Parameter
        ----------
            fecha str
            url str   
        
        Returns
        ---------
            information list
            """                
        
        [eventos_aragon, eventos_aragon_dict] = calendar_parser.parser(url)
        tipoEvento = TemplatesCalendar.getUrlTag(url)
        information = []
        for evento in eventos_aragon:
            if evento["fecha_inicio"].find(fecha) > -1:
                information.append(
                    {
                        "calendario_name": evento["calendario_name"],
                        "calendar_type": tipoEvento,
                        "nombre": evento["nombre"],
                        "descripcion": evento["descripcion"],
                        "fecha_inicio": evento["fecha_inicio"],
                        "fecha_fin": evento["fecha_fin"],
                        "localizacion": evento["localizacion"],
                    }
                )
        return information

    @staticmethod
    def getHolidaysDayLocationYearPlace(location, url, tipo, place) -> str:

        """ This function return the list of bank holiday from a location.
        Parameter
        ----------
            location str
            url str
            tipo str
            place str  
        
        Returns
        ---------
            information list
            """        
        
        place = TemplatesCalendar.getReplaceTildes(place)
        [eventos_aragon, eventos_aragon_dict] = calendar_parser.parser(url)
        tipoEvento = TemplatesCalendar.getUrlTag(url)
        information = []
        for evento in eventos_aragon:
            if tipo.upper() == "ARAGON":
                information.append(
                    {
                        "calendario_name": evento["calendario_name"],
                        "calendar_type": tipoEvento,
                        "nombre": evento["nombre"],
                        "descripcion": evento["descripcion"],
                        "fecha_inicio": evento["fecha_inicio"],
                        "fecha_fin": evento["fecha_fin"],
                        "localizacion": evento["localizacion"],
                    }
                )
            else:
                if tipo.upper() == "PROVINCIA":
                    if place.upper() == location.upper():
                        information.append(
                            {
                                "calendario_name": evento["calendario_name"],
                                "calendar_type": tipoEvento,
                                "nombre": evento["nombre"],
                                "descripcion": evento["descripcion"],
                                "fecha_inicio": evento["fecha_inicio"],
                                "fecha_fin": evento["fecha_fin"],
                                "localizacion": evento["localizacion"],
                            }
                        )
                else:
                    if evento["localizacion"].upper().find(location.upper()) > -1:
                        information.append(
                            {
                                "calendario_name": evento["calendario_name"],
                                "calendar_type": tipoEvento,
                                "nombre": evento["nombre"],
                                "descripcion": evento["descripcion"],
                                "fecha_inicio": evento["fecha_inicio"],
                                "fecha_fin": evento["fecha_fin"],
                                "localizacion": evento["localizacion"],
                            }
                        )
        return information

    @staticmethod
    def getHolidaysMonths(location, month, tipo, url, place) -> str:

        """ This function return the list of bank holiday of a concrete month and location.
        Parameter
        ----------
            location str
            month str
            tipo str            
            url str
            place str  
        
        Returns
        ---------
            information list
            """        
        
        place = TemplatesCalendar.getReplaceTildes(place)
        [eventos_aragon, eventos_aragon_dict] = calendar_parser.parser(url)
        tipoEvento = TemplatesCalendar.getUrlTag(url)
        information = []
        for evento in eventos_aragon:
            fecha_inicio = evento["fecha_inicio"]
            fecha_inicio_time_obj = datetime.datetime.strptime(fecha_inicio, "%d-%m-%Y")
            if fecha_inicio_time_obj.month == int(month):
                if tipo.upper() == "ARAGON":
                    information.append(
                        {
                            "calendario_name": evento["calendario_name"],
                            "calendar_type": tipoEvento,
                            "nombre": evento["nombre"],
                            "descripcion": evento["descripcion"],
                            "fecha_inicio": evento["fecha_inicio"],
                            "fecha_fin": evento["fecha_fin"],
                            "localizacion": evento["localizacion"],
                        }
                    )
                else:
                    if tipo.upper() == "PROVINCIA":
                        if place.upper() == location.upper():
                            information.append(
                                {
                                    "calendario_name": evento["calendario_name"],
                                    "calendar_type": tipoEvento,
                                    "nombre": evento["nombre"],
                                    "descripcion": evento["descripcion"],
                                    "fecha_inicio": evento["fecha_inicio"],
                                    "fecha_fin": evento["fecha_fin"],
                                    "localizacion": evento["localizacion"],
                                }
                            )
                    else:
                        if evento["localizacion"].upper().find(location.upper()) > -1:
                            information.append(
                                {
                                    "calendario_name": evento["calendario_name"],
                                    "calendar_type": tipoEvento,
                                    "nombre": evento["nombre"],
                                    "descripcion": evento["descripcion"],
                                    "fecha_inicio": evento["fecha_inicio"],
                                    "fecha_fin": evento["fecha_fin"],
                                    "localizacion": evento["localizacion"],
                                }
                            )
        return information

    @staticmethod
    def getHolidaysDayLocationYear(location, tipo, url, place) -> str:

        """ This function return the list of bank holiday of a concrete location.
        Parameter
        ----------
            location str
            tipo str            
            url str
            place str  
        
        Returns
        ---------
            information list
            """        
        
        place = TemplatesCalendar.getReplaceTildes(place)
        [eventos_aragon, eventos_aragon_dict] = calendar_parser.parser(url)
        tipoEvento = TemplatesCalendar.getUrlTag(url)
        information = []
        for evento in eventos_aragon:
            if tipo.upper() == "ARAGON":
                information.append(
                    {
                        "calendario_name": evento["calendario_name"],
                        "calendar_type": tipoEvento,
                        "nombre": evento["nombre"],
                        "descripcion": evento["descripcion"],
                        "fecha_inicio": evento["fecha_inicio"],
                        "fecha_fin": evento["fecha_fin"],
                        "localizacion": evento["localizacion"],
                    }
                )
            else:
                if tipo.upper() == "PROVINCIA":
                    if place.upper() == location.upper():
                        information.append(
                            {
                                "calendario_name": evento["calendario_name"],
                                "calendar_type": tipoEvento,
                                "nombre": evento["nombre"],
                                "descripcion": evento["descripcion"],
                                "fecha_inicio": evento["fecha_inicio"],
                                "fecha_fin": evento["fecha_fin"],
                                "localizacion": evento["localizacion"],
                            }
                        )
                else:
                    if evento["localizacion"].upper().find(location.upper()) > -1:
                        information.append(
                            {
                                "calendario_name": evento["calendario_name"],
                                "calendar_type": tipoEvento,
                                "nombre": evento["nombre"],
                                "descripcion": evento["descripcion"],
                                "fecha_inicio": evento["fecha_inicio"],
                                "fecha_fin": evento["fecha_fin"],
                                "localizacion": evento["localizacion"],
                            }
                        )
        return information

    @staticmethod
    def getHolidaysRange(location, datefrom, dateTo, tipo, url, place) -> str:

        """ This function return the list of bank holiday of a concrete range of dates and of a concrete location.
        Parameter
        ----------
            location str
            datefrom str
            dateTo str
            tipo str            
            url str
            place str  
        
        Returns
        ---------
            information list
            """        
        
        place = TemplatesCalendar.getReplaceTildes(place)
        [eventos_aragon, eventos_aragon_dict] = calendar_parser.parser(url)
        tipoEvento = TemplatesCalendar.getUrlTag(url)
        information = []
        datefrom_time = datetime.datetime.strptime(datefrom, "%d-%m-%Y")
        dateTo_time = datetime.datetime.strptime(dateTo, "%d-%m-%Y")
        for evento in eventos_aragon:
            fecha_inicio = evento["fecha_inicio"]
            fecha_inicio_time_obj = datetime.datetime.strptime(fecha_inicio, "%d-%m-%Y")
            fecha_fin = evento["fecha_fin"]
            fecha_fin_time_obj = datetime.datetime.strptime(fecha_fin, "%d-%m-%Y")
            tipo = TemplatesCalendar.getReplaceTildes(tipo)
            if (
                fecha_inicio_time_obj >= datefrom_time
                and dateTo_time >= fecha_fin_time_obj
            ):
                if tipo.upper() == "ARAGON":
                    information.append(
                        {
                            "calendario_name": evento["calendario_name"],
                            "calendar_type": tipoEvento,
                            "nombre": evento["nombre"],
                            "descripcion": evento["descripcion"],
                            "fecha_inicio": evento["fecha_inicio"],
                            "fecha_fin": evento["fecha_fin"],
                            "localizacion": evento["localizacion"],
                        }
                    )
                else:
                    if tipo.upper() == "PROVINCIA":
                        if place.upper() == location.upper():
                            information.append(
                                {
                                    "calendario_name": evento["calendario_name"],
                                    "calendar_type": tipoEvento,
                                    "nombre": evento["nombre"],
                                    "descripcion": evento["descripcion"],
                                    "fecha_inicio": evento["fecha_inicio"],
                                    "fecha_fin": evento["fecha_fin"],
                                    "localizacion": evento["localizacion"],
                                }
                            )
                    else:
                        if evento["localizacion"].upper().find(location.upper()) > -1:
                            information.append(
                                {
                                    "calendario_name": evento["calendario_name"],
                                    "calendar_type": tipoEvento,
                                    "nombre": evento["nombre"],
                                    "descripcion": evento["descripcion"],
                                    "fecha_inicio": evento["fecha_inicio"],
                                    "fecha_fin": evento["fecha_fin"],
                                    "localizacion": evento["localizacion"],
                                }
                            )
        return information

    @staticmethod
    def getUrlTag(url):

        """ This function returns the type of caledar.
        Parameter
        ----------
            url str
        
        Returns
        ---------
            str
            """        
        
        if url.upper().find("FESTIVO") > -1:
            return "Festivos"
        else:
            if url.upper().find("FERIAS") > -1:
                return "Eventos"
            else:
                if url.upper().find("ESCOLAR"):
                    return "Fechas de Calendario Escolar"

    @staticmethod
    def getReplaceTildes(tipo):

        """ This function replaces some string characters to get the final string format.
        Parameter
        ----------
            tipo str            
        
        Returns
        ---------
            tipo str
            """        
        
        return (
            tipo.replace("á", "a")
            .replace("ó", "o")
            .replace("í", "i")
            .replace("é", "e")
            .replace("ú", "u")
            .replace("Á", "A")
            .replace("Ó", "O")
            .replace("Í", "I")
            .replace("É", "E")
            .replace("Ú", "U")
        )

    @staticmethod
    def getTypeCalendar(calendario):

        """ This function gets the location area.
        Parameter
        ----------
            cadendario str            
        
        Returns
        ---------
            calendario_name str
            """        
        
        calendario_name = ""
        if calendario.find("ar-") > -1:
            calendario_name = "Aragon"
        else:
            if calendario.find("hu-") > -1:
                calendario_name = "Huesca"
            else:
                if calendario.find("za-") > -1:
                    calendario_name = "Zaragoza"
                else:
                    if calendario.find("te-") > -1:
                        calendario_name = "Teruel"
                    else:
                        calendario_name = "Aragón"

        return calendario_name

    @staticmethod
    def getTodayDay():

        """ This function gets the correct date fromat."""
        
        return time.strftime("%d-%m-%Y")

    @staticmethod
    def getStringDataInDateFormat(date_time_str):

        """ This function gets the correct date fromat."""
        
        date_time_obj = datetime.datetime.strptime(date_time_str, "%d-%m-%Y")
        return date_time_obj

    @staticmethod
    def isHigherFechaInicioToToday(fecha_inicio):

        """ This function verifies if fecha_inicio is just passed.
        Parameter
        ----------
            fecha_inicio str            
        
        Returns
        ---------
            boolean
            """        
        
        fecha_hoy = TemplatesCalendar.getTodayDay()
        fecha_hoy = TemplatesCalendar.getStringDataInDateFormat(fecha_hoy)
        fecha_inicio_date_obj = TemplatesCalendar.getStringDataInDateFormat(
            fecha_inicio
        )
        if fecha_inicio_date_obj >= fecha_hoy:
            return True
        else:
            return False