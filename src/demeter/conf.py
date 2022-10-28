import os

config = {}

if os.getenv('DEBUG', "true").lower() == "true":
    config['DEBUG']=True
    config['PORT']=3000
    config['HOST']='localhost'
    config['MODEL_PATH']='/home/hsotelo/demeter/demeter'
    config['PARAMS_PATH']='/home/hsotelo/demeter/service/vocab'
    config['ACLIMATE_API']='https://webapi.aclimate.org/api/'
    config['CONNECTION_DB']='mongodb://root:s3cr3t@localhost:27017/demeter?authSource=admin'
    config['COUNTRIES']='61e59d829d5d2486e18d2ea8'
    config['ENABLE_REGISTER_MELISA']=True
    config['AGRILAC_KEY']=""
    config['AGRILAC_FILE']=""
    config['AGRILAC_SHEET']=""
else:
    config['DEBUG']=False
    config['PORT']=os.getenv('PORT')
    config['HOST']='0.0.0.0'
    config['MODEL_PATH']=os.getenv('MODEL_PATH')
    config['PARAMS_PATH']=os.getenv('PARAMS_PATH')
    config['ACLIMATE_API']=os.getenv('ACLIMATE_API')
    config['CONNECTION_DB']=os.getenv('CONNECTION_DB')
    config['COUNTRIES']=os.getenv('COUNTRIES')
    config['ENABLE_REGISTER_MELISA']=os.getenv('ENABLE_REGISTER_MELISA')
    config['AGRILAC_KEY']=os.getenv('AGRILAC_KEY')
    config['AGRILAC_FILE']=os.getenv('AGRILAC_FILE')
    config['AGRILAC_SHEET']=os.getenv('AGRILAC_SHEET')
