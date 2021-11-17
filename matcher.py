import unidecode
import pandas as pd
import numpy as np

class DBM:
    def __init__(self,db_inputs,inputs):
        self.db_inputs = db_inputs
        self.inputs = inputs

    def load_data(self):
        ext = self.db_Inputs['extension']
        self.nucleo = pd.read_excel(self.db_Inputs['ruta_nuc']+self.db_Inputs['nombre_nucleo']+ext,encoding='latin-1')
        self.ppb = pd.read_excel(self.db_Inputs['ruta_ppb']+self.db_Inputs['nombre_ppb']+extencoding='latin-1')
        self.local = pd.read_excel(self.db_Inputs['ruta_loc']+self.db_Inputs['nombre_loc']+ext,encoding='latin-1')
    
    def test_simple(self):
        pass
    
    def test_eliminateNull(self):
        pass
    
    def test_removeStuff(self):
        pass
    
    def test_subset(self):
        pass
    
    def test_transformNumbers(self):
        pass

    def compare_localidades(self):
        self.test_parenthesis()
    
    def test_parenthesis(self):
        pass

    def save_database(self):
        save_route = self.db_Inputs['ruta_merge']+self.db_Inputs['nombre_ppb']+'.csv'
        self.ppb.to_csv(save_route,encoding='latin-1')
        print(f'Database {self.ppb_name} has been saved with success at {save_route}')
    
    def performance(self):
        pass
    
    def main(self):
        self.load_data()
        #Para cada una de las filas de PPB (base a clasificar)
        #match: NUCLEO_AGRARIO-- Regresa: Clave
        for index, row in self.iterrows():
            global_validator = False
            #1. comparar con base Nucleos:
                #a. test_eliminateNull()
                #b. Comparar Municipios;
                    #b. True: Comparar NUCLEO_AGRARIO con NOM_NUC (prueba 5v); True traer clave
                        #   False: compare_localidades()
                            #   False: Guardar como Error1
                    #b. False-. compare_localidades()
                            #   False: Guardar como Error2
                            
        self.performance()
        self.save_database()
            