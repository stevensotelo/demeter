import pandas as pd
from nlu.enums import Geographic, Cultivars, Forecast, Historical, Error, Commands

class Generator():


    # Method that return an answer for the users
    # (NER[]) answers: List of answers
    @staticmethod
    def print(answers):
        msg = []
        if(len(answers) > 0):
            for a in answers:
                # Commands
                if (isinstance(a.type, Commands)):
                    if(a.type == Commands.HI):
                        msg.append("Hola, ¿cómo puedo ayudarte?")
                    elif(a.type == Commands.BYE):
                        msg.append("Chao :)")
                    elif(a.type == Commands.HELP):
                        msg.append("Puedes preguntarme sobre información histórica de clima, también sobre predicción de clima y producción de cultivos")
                        msg.append("Si quieres saber que localidades hay disponibles podrías preguntar algo como: Municipios disponibles")
                        msg.append("Si quieres saber sobre que cultivos hay disponibles: ¿Qué cultivos hay disponibles?")
                        msg.append("Yo intentaré identificar que información es la que necesitas y te daré una respuesta sobre ese tema")
                    else:
                        msg.append("Con mucho gusto")
                # Geographic answers
                elif (isinstance(a.type, Geographic)):
                    if(a.type == Geographic.STATE):
                        msg.append("Los departamentos disponibles son: " + ', '.join(a.values))
                    elif(a.type == Geographic.MUNICIPALITIES_STATE):
                        msg.append("Los municipios para el departamento " + a.tag + " disponibles son: " + ', '.join(a.values))
                    elif(a.type == Geographic.WS_MUNICIPALITY):
                        msg.append("Las estaciones climáticas para el municipio " + a.tag + " disponibles son: " + ', '.join(a.values))
                    else:
                        msg.append("En el municipio " + a.tag + " están las estaciones: " +  ', '.join(a.values))
                # Cultivars answers
                elif (isinstance(a.type, Cultivars)):
                    if(a.type == Cultivars.CROP_MULTIPLE):
                        msg.append("Los cultivos disponibles son: " + ', '.join(a.values))
                    elif(a.type == Cultivars.CROP_CULTIVAR):
                        msg.append("Las variedades para el cultivo " + a.tag + " disponibles son: " + ', '.join(a.values))
                    else:
                        msg.append("Las variedades similares a " + a.tag + " disponibles son: " + ', '.join(a.values))
                # Historical answers
                elif (isinstance(a.type, Historical)):
                    # Climatology answers
                    if(a.type == Historical.CLIMATOLOGY):
                        # Get ws ids
                        ws_id = a.values.loc[:,"ws_id"].unique()                        
                        for ws in ws_id:
                            # Filter by ws_id
                            cl_ws = a.values.loc[a.values["ws_id"] == ws,:]
                            m = "Para la estación " + cl_ws.iloc[0]["ws_name"] + ", la climatología es: "
                            # Get measures
                            #msg.append(m)                            
                            cl_var = cl_ws.loc[:,"measure"].unique().tolist()
                            # Remove climatology for terciles
                            if "prec_ter_1" in cl_var:
                                cl_var.remove("prec_ter_1")
                            if "prec_ter_2" in cl_var:
                                cl_var.remove("prec_ter_2")
                            for v in cl_var:
                                #m = ""
                                m_name = Generator.get_climate_measure(v) + " (" + Generator.get_climate_unit(v) + ") "
                                m = m + m_name + ": "
                                cl_measure = cl_ws.loc[cl_ws["measure"] == v,:]
                                # List according to measure
                                for me in cl_measure.itertuples(index=True, name='Pandas') :
                                    m = m + Generator.get_month(getattr(me, "month")) + " " + str(int(getattr(me, "value"))) + ", "
                                #msg.append(m[:-2])
                                m = m[:-2] + ". "
                            msg.append(m)
                # Forecast answer
                elif (isinstance(a.type, Forecast)):
                    # Climate answers
                    if(a.type == Forecast.CLIMATE):
                        # Get ws ids
                        ws_id = a.values.loc[:,"ws_id"].unique()
                        for ws in ws_id:
                            # Filter by ws_id
                            cl_ws = a.values.loc[a.values["ws_id"] == ws,:]
                            m = "Para la estación " + cl_ws.iloc[0]["ws_name"] + ", la predicción climática es: "
                            #msg.append(m)
                            for w in cl_ws.itertuples(index=True, name='Pandas') :
                                m = m + "para el trimestre "
                                m = m + Generator.get_month(getattr(w, "month")) + "-" + Generator.get_month(getattr(w, "month") + 1) + "-" + Generator.get_month(getattr(w, "month")+2) + ": " 
                                m = m + "por encima de lo normal = " + str(round(getattr(w, "upper") * 100.0,2)) + "%, " 
                                m = m + "por dentro de lo normal = " + str(round(getattr(w, "normal") * 100.0, 2)) + "%, " 
                                m = m +"por debajo de lo normal = " + str(round(getattr(w, "lower") * 100.0,2)) + "% "
                                #msg.append(m)
                            msg.append(m)
                    # yield answers
                    elif a.type == Forecast.YIELD_PERFORMANCE:
                        # Get ws ids
                        ws_id = a.values.loc[:,"ws_id"].unique()
                        for ws in ws_id:
                            # Filter by ws_id
                            cp_ws = a.values.loc[a.values["ws_id"] == ws,:]
                            crops = cp_ws["cp_name"].unique()
                            for cp in crops:
                                m = "Para la estación " + cp_ws.iloc[0]["ws_name"] + ", encontramos que el cultivo " + cp + " presenta las siguientes variedades con mejor rendimiento potencial: "
                                #msg.append(m)
                                cu_ws = cp_ws.loc[cp_ws["cp_name"] == cp,:]
                                cultivars = cu_ws["cu_name"].unique()
                                for cu in cultivars:
                                    cp_cu_data = cu_ws.loc[cu_ws["cu_name"] == cu,:]
                                    m = m + cu + ": "
                                    for ccd in cp_cu_data.itertuples(index=True, name='Pandas'):
                                        m = m + "sembrando en " + str(getattr(ccd, "start"))[:-10] + ", tipo de suelo " + getattr(ccd, "so_name") + " "
                                        m = m + "puedes obtener en promedio: " + str(round(getattr(ccd, "avg"),2)) + " kg/ha, "
                                        m = m + "variando entre máx. " + str(round(getattr(ccd, "max"),2)) + " kg/ha "
                                        m = m + "y mín. " + str(round(getattr(ccd, "min"),2)) + " kg/ha. "
                                    #msg.append(m)
                                msg.append(m)
                    # yield answers
                    elif a.type == Forecast.YIELD_DATE:
                        # Get ws ids
                        ws_id = a.values.loc[:,"ws_id"].unique()
                        for ws in ws_id:
                            # Filter by ws_id
                            cp_ws = a.values.loc[a.values["ws_id"] == ws,:]
                            crops = cp_ws["cp_name"].unique()
                            for cp in crops:
                                m = "Para la estación " + cp_ws.iloc[0]["ws_name"] + ", encontramos que las mejores fechas de siembra para el cultivo " + cp + " son: "
                                #msg.append(m)
                                for ccd in cp_ws.itertuples(index=True, name='Pandas'):
                                    m = m + "la variedad " + getattr(ccd, "cu_name") + ", en un suelo " +  getattr(ccd, "so_name") + " "
                                    m = m + "y sembrando en " + str(getattr(ccd, "start"))[:-10] + " "
                                    m = m + " puedes obtener en promedio: " + str(round(getattr(ccd, "avg"),2)) + " kg/ha. "
                                    #m = m + " variando con máx. de: " + str(round(getattr(ccd, "max"),2)) + " kg/ha"
                                    #m = m + " y un mín. de: " + str(round(getattr(ccd, "min"),2)) + " kg/ha"
                                msg.append(m)
                # Message error
                elif (isinstance(a.type, Error)):
                    # Missing geographic
                    if(a.type == Error.MISSING_GEOGRAPHIC):
                        msg.append("Lo sentimos, no encontramos una localidad en su solicitud. Por favor intente especificando un municipio, también puedes preguntarme sobre los municipios disponibles")
                    # Locality not found
                    elif(a.type == Error.LOCALITY_NOT_FOUND):
                        msg.append("Lo sentimos, actualmente no tenemos la localidad: " + a.tag + " disponible en la base de datos")
                    # Locality not found
                    elif(a.type == Error.MISSING_ENTITIES):
                        msg.append("Lo sentimos, su consulta no pudo ser procesada. Por favor intenta preguntando de otra manera")
                    # Locality not found
                    elif(a.type == Error.ERROR_ACLIMATE):
                        msg.append("Lo sentimos, su consulta no pudo ser procesada. No se logro conectar con el servicio de Aclimate")
                    elif(a.type == Error.ERROR_ACLIMATE_CLIMATOLOGY):
                        msg.append("Lo sentimos, no hay información de climatología para la localidad de: " + a.tag + " en Aclimate")
                    elif(a.type == Error.ERROR_ACLIMATE_FORECAST_CLIMATE):
                        msg.append("Lo sentimos, no hay información de predicción climática para la localidad de: " + a.tag + " en Aclimate")
                    elif(a.type == Error.ERROR_ACLIMATE_FORECAST_YIELD):
                        msg.append("Lo sentimos, no hay información de pronóstico de cultivo de para la localidad de: " + a.tag + " en Aclimate")
                    elif(a.type == Error.MISSING_CROP_CULTIVAR):
                        msg.append("Lo sentimos, no encontramos un cultivo o un cultivar en su solicitud. Por favor intente especificando un cultivo o cultivar, también puede preguntarme sobre los cultivares disponibles")
        else:
            msg.append('Lo sentimos, su consulta no pudo ser procesada, por favor intente de nuevo')
        return msg
    
    # Method that return the description of measure
    # (string) var: Name of measure
    @staticmethod
    def get_climate_measure(var):
        a = 'precipitación'
        if(var == "sol_rad"):
            a = "radiación solar"
        elif (var == "t_max"):
            a = "temperatura máxima"
        elif (var == "t_min"):
            a = "temperatura mínima"
        return a
    
    #
    @staticmethod
    def get_climate_unit(var):
        a = 'mm'
        if(var == "sol_rad"):
            a = "cal/cm²d"
        elif (var == "t_max"):
            a = "°C"
        elif (var == "t_min"):
            a = "°C"
        return a

    # Method that return the month name
    # (int) id: Id of month
    @staticmethod
    def get_month(id):
        months = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        return months[int(id)-1]