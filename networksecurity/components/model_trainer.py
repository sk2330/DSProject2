import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.main_utils.utils import save_object, load_object
from networksecurity.utils.main_utils.utils import load_numpy_array_data, evaluate_models
from networksecurity.utils.ml_utils.metrics.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier




class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig, data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def train_model(self, X_train, y_train,X_test,y_test):

        models = {
            'LogisticRegression': LogisticRegression(verbose=1),
            'RandomForestClassifier': RandomForestClassifier(verbose=1),
            'AdaBoostClassifier': AdaBoostClassifier(),
            'GradientBoostingClassifier': GradientBoostingClassifier(verbose=1),
            'DecisionTreeClassifier': DecisionTreeClassifier(),
            'KNeighborsClassifier': KNeighborsClassifier()
        }

        ### performing hyperparameter tuning
        params={
            "Decision Tree":{
                'criterion':['gini','entropy','log_loss'],
                # 'max_depth':[3,5,7,9,11],
                # 'min_samples_split':[2,5,10],
                # 'min_samples_leaf':[1,2,3,4,5],
                # 'max_features':['auto','sqrt','log2']
            },
            "Random Forest" : {
                'criterion':['gini','entropy','log_loss'],
                # 'max_depth':[3,5,7,9,11],
                # 'min_samples_split':[2,5,10],
                # 'min_samples_leaf':[1,2,3,4,5],
                # 'max_features':['auto','sqrt','log2'],
                # 'n_estimators': [8,16,32,64,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss','exponential'],
                'learning_rate':[.1,.01,.05,.001],
                # 'n_estimators': [8,16,32,64,128,256]
                'subsample': [0.6,0.7,0.75,0.8,0.85]
            },
            "AdaBoost":{
                'learning_rate':[.1,.01,0.5,.001],
                 'n_estimators': [8,16,32,64,128,256]
            },
            "KNN":{
                'n_neighbors': [1,2,3,4,5,6,7,8,9,10]
            },
            "Logistic Regression":{
                # 'C': [0.1,0.001],
                # 'penalty': ['l1','l2']
            }
        }
    
        model_report:dict=evaluate_models(x_train=X_train,y_train=y_train,x_test=X_test,y_test=y_test,
                                        models=models,param=params)
        
        ##getting the best model from model_report dictionary
        best_model_score = max(sorted(model_report.values()))

        ### Getting best model name
        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]
        
        best_model= models[best_model_name]
        y_train_pred = best_model.predict(X_train)

        classification_train_metrics=get_classification_score(y_true=y_train,y_pred=y_train_pred)
        
        ###for test data

        y_test_pred = best_model.predict(X_test)
        classification_test_metrics = get_classification_score(y_true=y_test, y_pred=y_test_pred)

        preprocessor=load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path, exist_ok=True)
        network_model=NetworkModel(preprocessor=preprocessor,model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path, obj=network_model)

        ##Model Trainer Artifact
        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact=classification_train_metrics,
            test_metric_artifact=classification_test_metrics
        )
        logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
        return model_trainer_artifact


            
    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logging.info("Loading transformed train and test dataset")
            transformed_train_file_path = self.data_transformation_artifact.transformed_train_file_path
            transformed_test_file_path = self.data_transformation_artifact.transformed_test_file_path
            

            ###Loading transformed train and test array
            logging.info("Loading train and test array")
            train_arr = load_numpy_array_data(transformed_train_file_path)
            test_arr = load_numpy_array_data(transformed_test_file_path)

            logging.info("Splitting input and target feature from both train and test arr.")
            x_train, y_train, x_test, y_test = train_arr[:, :-1], train_arr[:, -1], test_arr[:, :-1], test_arr[:, -1]
            
            model_trainer_artifact =self.train_model(x_train,y_train)
            return model_trainer_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        