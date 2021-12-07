# -*- coding: latin-1 -*-
import pandas as pd
import numpy as np

class DBM:
    def __init__(self,inputs,db_inputs):
        self.db_inputs = db_inputs
        self.inputs = inputs

    # Load PPB,NUC and LOC databases
    def load_data(self):
        ext = self.db_inputs['extension']
        self.nucleo = pd.read_excel(self.db_inputs['ruta_nuc']+self.db_inputs['nombre_nucleo']+ext)
        self.ppb = pd.read_excel(self.db_inputs['ruta_ppb']+self.db_inputs['nombre_ppb']+ext)
        self.local = pd.read_excel(self.db_inputs['ruta_loc']+self.db_inputs['nombre_loc']+ext)
    
    #Compara uno a uno 
    def test_simple(self,nuc_agr,nom_nuc,clave_nuc):
        if not self.validator:
            if nuc_agr == nom_nuc:
                self.clave = clave_nuc
    
    def test_eliminateNull(self,element):
        if not self.validator:
            if element in self.inputs['nulos']:
                self.validator = True
                self.clave = '0'

    def test_subset(self,nuc_agr,nom_nuc,clave_nuc):
        if not self.validator:
            nuc_agr = set(nuc_agr)
            nom_nuc = set(nom_nuc)

            if nuc_agr.issubset(nom_nuc) or nom_nuc.issubset(nuc_agr):
                self.clave = clave_nuc
                self.validator = True
    
    def test_removeStuff(self,nuc_agr,nom_nuc,clave_nuc):
        nuc_agr = nuc_agr.split()
        nom_nuc = nom_nuc.split()
        if not self.validator:
            for w in self.inputs['remover']:
                if w in nuc_agr:
                    nuc_agr.remove(w)
            self.test_simple(nuc_agr,nom_nuc,clave_nuc)

        else:
            self.test_subset(nuc_agr,nom_nuc,clave_nuc)
    
    def test_transformNumbers(self,nuc_agr,nom_nuc,clave_nuc):
        pass

    def compare_localidades(self):
        self.test_parenthesis()
    
    def test_parenthesis(self):
        pass

    #Save merged database in specific route
    def save_database(self):
        save_route = self.db_Inputs['ruta_merge']+self.db_Inputs['nombre_ppb']+'.csv'
        self.ppb.to_csv(save_route,encoding='latin-1')
        print('Database has been saved with success at: '+ str(save_route))
    
    def performance(self,test_row):
        print(test_row.count())
    
    def main(self):
        print("machine on")
        self.load_data()
        print("data read")
        #Para cada una de las filas de PPB (base a clasificar)
        #match: NUCLEO_AGRARIO-- Regresa: Clave
        claves = []
        n = len(self.ppb)
        for index, ppb_row in self.ppb.iterrows():
            print("missing"+str(n))
            self.validator = False
            self.clave = 'not classified'
            nuc_agr = str(ppb_row['NUCLEO_AGRARIO'])
            #1. comparar con base Nucleos:
                #a. test_eliminateNull()
            self.test_eliminateNull(nuc_agr)
                #b. Comparar Municipios;
            if not self.validator:
                for index, nuc_row in self.nucleo.iterrows():
                        #b. True: Comparar NUCLEO_AGRARIO con NOM_NUC (prueba 5v); True traer clave
                        nom_nuc = str(nuc_row['NOM_NUC'].encode('latin-1'))
                        clave_nuc = str(nuc_row['CLAVE'].encode('latin-1'))

                        self.test_simple(nuc_agr,nom_nuc,clave_nuc)
                        self.test_removeStuff(nuc_agr,nom_nuc,clave_nuc)
                            #   False: compare_localidades()
                                #   False: Guardar como Error1
                        #b. False-. compare_localidades()
                                #   False: Guardar como Error2
            
            #se terminan los tests y se guarda la clave
            if self.clave == 'not classified':
                print(self.clave)
            else:
                print("classified")
            claves.append(self.clave)
            n = n-1
        self.ppb['clave_'] = claves

                            
        self.performance(self.ppb['clave_'])
        self.save_database()
            