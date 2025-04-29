import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
#import dill
import pickle
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys) 
    
###Function for writing inside the drift report(data_validation.py)

def write_yaml_file(file_path:str,content:object, replace:bool=False) ->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) 

#### Function to save transformed data into .npy file
def save_numpy_array_data(file_path:str, array:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys) 

##Save any models or pickle files
def save_object(file_path:str, obj:object)->None:
    try:
        logging.info("Entered the save_object method of utils file")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method of utils file")
    except Exception as e:
        raise NetworkSecurityException(e, sys)

### to read the pcikle files saved using saved_object function we create load_object
def load_object(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, 'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

### To load the nnumpy arrays
def load_numpy_array_data(file_path:str)->np.array:
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

###Evaluate the models function

def evaluate_models(X_train,y_train,X_test,y_test,models):
    try:
        report = {}
        for i in range(len(models)):
            model = list(models.values())[i]
            param=param[list(models.keys())[i]]

            gs=GridSearchCV(model,param,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            #Train and test data accuracy
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_score = accuracy_score(y_train,y_train_pred)
            test_model_score = accuracy_score(y_test,y_test_pred)

            report[list(models.keys())[i]] = test_model_score
        return report
    
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    

    










