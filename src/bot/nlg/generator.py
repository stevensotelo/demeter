import pandas as pd
from nlu.enums import Geographic, Cultivars, Forecast, Historical

class Generator():


    # Method that return an answer for the users
    # (NER[]) answers: List of answers
    @staticmethod
    def print(answers):
        msg = []
        if(len(answers) > 0):
            for a in answers:
                # Geographic answers
                if (isinstance(a.type, Geographic)):
                    if(a.type == Geographic.STATE):
                        msg.append("Los departamentos disponibles son: " + ','.join(a.values))
                    elif(a.type == Geographic.MUNICIPALITIES_STATE):
                        msg.append("Los municipios para el departamento " + a.tag + " disponibles son: " + ','.join(a.values))
                    elif(a.type == Geographic.WS_MUNICIPALITY):
                        msg.append("Las estaciones climáticas para el municipio " + a.tag + " disponibles son: " + ','.join(a.values))
                    else:
                        msg.append("En el municipio " + a.tag + " están las estaciones: " +  + ','.join(a.values))
                # Cultivars answers
                elif (isinstance(a.type, Cultivars)):
                    if(a.type == Cultivars.CROP_MULTIPLE):
                        msg.append("Los cultivos disponibles son: " + ','.join(a.values))
                    elif(a.type == Cultivars.CROP_CULTIVAR):
                        msg.append("Las variedades para el cultivo " + a.tag + " disponibles son: " + ','.join(a.values))
                    else:
                        msg.append("Las variedades para el cultivo " + a.tag + " disponibles son: " + ','.join(a.values))
                # Historical answers
                elif (isinstance(a.type, Historical)):
                    # Climatology answers
                    if(a.type == Historical.CLIMATOLOGY):
                        # Get ws ids
                        ws_id = a.values[:,"ws_id"].unique()
                        for ws in ws_id:
                            # Filter by ws_id
                            cl_ws = a.values[a.value["ws_id"] == ws,:]
                            m = "Para la estación " + cl_ws["ws_name"][0] + ", la climatología es: "
                            # Get measures
                            cl_var = cl_ws.loc[:,"measure"].unique()
                            for v in cl_var:
                                m_name = Generator.get_climate_measure(v)
                                m = m + m_name + ": "
                                cl_measure = cl_ws.loc[cl_ws["measure"] == v,:]
                                # List according to measure
                                for me in cl_measure.itertuples(index=True, name='Pandas') :
                                    m = m + Generator.get_month(getattr(me, "month")) + " " + str(getattr(me, "value")) + " "
                            msg.append(m)
                # Forecast answer
                elif (isinstance(a.type, Forecast)):
                    # Climate answers
                    if(a.type == Forecast.FORECAST_CLIMATE):
                        # Get ws ids
                        ws_id = a.values[:,"ws_id"].unique()
                        for ws in ws_id:
                            # Filter by ws_id
                            cl_ws = a.values[a.value["ws_id"] == ws,:]
                            m = "Para la estación " + cl_ws["ws_name"][0] + ", la predicción climática es: "
                            for w in cl_ws.itertuples(index=True, name='Pandas') :
                                m = m + Generator.get_month(getattr(me, "month")) + ": " 
                                m = m + "Por encima de lo normal = " + str(getattr(me, "upper") * 100.0) + "% " 
                                m = m + "Por dentro de lo normal = " + str(getattr(me, "normal") * 100.0) + "% " 
                                m = m +"Por debajo de lo normal = " + str(getattr(me, "lower") * 100.0) + "% "
                            msg.append(m)
                # Message error
                elif (isinstance(a.type, Error)):
                    # Missing geographic
                    if(a.type == Error.MISSING_GEOGRAPHIC):
                        msg.append("No encontramos una localidad en su solicitud. Por favor intente especificando un municipio, también puede preguntarme sobre los municipios disponibles.")
                    # Locality not found
                    elif(a.type == Error.LOCALITY_NOT_FOUND):
                        msg.append("Actualmente no tenemos la localidad: " + a.tag + " disponible en la base de datos")
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

    # Method that return the month name
    # (int) id: Id of month
    @staticmethod
    def get_month(id):
        months = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        return months[id-1]