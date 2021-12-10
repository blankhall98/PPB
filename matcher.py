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
                self.validator = True
                self.clave = clave_nuc
    
    def test_eliminateNull(self,element,nuc_mun):
        if not self.validator:
            for n in self.inputs['nulos']:
                if element.startswith(n) or element==n:
                    self.validator = True
                    self.clave = '0'
                    break
        if not self.validator:
            for n in self.inputs['cabeceras']:
                if element.startswith(n) or element==n:
                    self.validator = True
                    self.clave = nuc_mun
                    break

    def test_subset(self,nuc_agr,nom_nuc,clave_nuc):
        if not self.validator:
            nuc_agr = set(nuc_agr)
            nom_nuc = set(nom_nuc)

            if nuc_agr.issubset(nom_nuc) or nom_nuc.issubset(nuc_agr):
                self.clave = clave_nuc
                self.validator = True
    
    def test_removeStuff(self,nuc_agr,nom_nuc,clave_nuc):
        if not self.validator:
            nuc_agr = nuc_agr.split()
            nom_nuc = nom_nuc.split()

        if not self.validator:
            for w in self.inputs['remover']:
                if w in nuc_agr:
                    nuc_agr.remove(w)
                if w in nom_nuc:
                    nom_nuc.remove(w)

                for i in range(len(nuc_agr)):
                    nuc_agr[i] = nuc_agr[i].replace(',','')

                for i in range(len(nom_nuc)):
                    nom_nuc[i] = nom_nuc[i].replace(',','')

            self.test_simple(nuc_agr,nom_nuc,clave_nuc)

        if not self.validator:
            nuc_agr.sort()
            nom_nuc.sort()
            self.test_simple(nuc_agr,nom_nuc,clave_nuc)
        

        if not self.validator:
            self.test_subset(nuc_agr,nom_nuc,clave_nuc)
    
    def test_transformNumbers(self,nuc_agr,nom_nuc,clave_nuc):
        for k in range(len(nuc_agr)):
            for num in self.inputs['numeros']:
                if nuc_agr[k] in self.inputs['numeros'][num]:
                        nuc_agr[k] = num
        for k in range(len(nom_nuc)):
            for num in self.inputs['numeros']:
                if nom_nuc[k] in self.inputs['numeros'][num]:
                        nom_nuc[k] = num
        self.test_simple(nuc_agr,nom_nuc,clave_nuc)
        self.test_removeStuff(nuc_agr,nom_nuc,clave_nuc)

    def compare_localidades(self):
        self.test_parenthesis()
    
    def test_parenthesis(self):
        pass

    #Save merged database in specific route
    def save_database(self):
        save_route = self.db_inputs['ruta_merge']+self.db_inputs['nombre_ppb']+'.csv'
        self.ppb.to_csv(save_route,encoding='latin-1')
        print('Data was saved')

    def performance(self,test_row):
        print(test_row.describe())

    def normalize(self,s):
        replacements = (
            ("á", "a"),
            ("é", "e"),
            ("í", "i"),
            ("ó", "o"),
            ("ú", "u"),
        )
        for a, b in replacements:
            s = s.replace(a, b).replace(a.upper(), b.upper())
        return s
    
    def main(self):
        print("machine on")
        self.load_data()
        print("data read")
        #Para cada una de las filas de PPB (base a clasificar)
        #match: NUCLEO_AGRARIO-- Regresa: Clave
        claves = []
        self.nuc_mun_unique = self.nucleo['MUNICIPIO'].unique()
        self.nuc_mun_unique = [self.normalize(x) for x in self.nuc_mun_unique]

        for index1, ppb_row in self.ppb.iterrows():
            self.validator = False
            self.clave = 'not classified'
            nuc_agr = self.normalize(str(ppb_row['NUCLEO_AGRARIO']))
            nuc_mun = self.normalize(str(ppb_row['MUNICIPIO']))
            #1. comparar con base Nucleos:
                #a. test_eliminateNull()
            self.test_eliminateNull(nuc_agr,nuc_mun)
                #b. Comparar Municipios;
            if not self.validator:
                if nuc_mun in self.nuc_mun_unique:
                    nucleo_reduced = self.nucleo[self.nucleo['MUNICIPIO']==nuc_mun]
                    nucleo_unique = nucleo_reduced['NOM_NUC'].unique()
                    for nom_nuc in nucleo_unique:
                            #b. True: Comparar NUCLEO_AGRARIO con NOM_NUC (prueba 5v); True traer clave
                            clave_nuc = self.nucleo[self.nucleo['NOM_NUC'] == nom_nuc]['CLAVE'].values[0]
                            self.test_simple(nuc_agr,nom_nuc,clave_nuc)
                            self.test_removeStuff(nuc_agr,nom_nuc,clave_nuc)
                            self.test_transformNumbers(nuc_agr,nom_nuc,clave_nuc)
                            #   False: compare_localidades()
                                #   False: Guardar como Error1
                    if not self.validator:
                        loc_reduced = self.local[self.local['MUN']==nuc_mun]
                        loc1_unique = loc_reduced['LOC1'].unique()
                        for lc in loc1_unique:
                            clave_loc = self.local[self.local['LOC']==lc]['CVEGEO_LOC'].values[0]
                            self.test_simple(nuc_agr,lc,clave_loc)
                            self.test_removeStuff(nuc_agr,lc,clave_loc)
                            self.test_transformNumbers(nuc_agr,lc,clave_loc)

                    if not self.validator:
                        self.clave = "error1"
                else:
                    self.clave = "error2"
            
            #se terminan los tests y se guarda la clave
            claves.append(self.clave)
            print(index1)
        self.ppb['clave_'] = claves

                            
        self.performance(self.ppb['clave_'])
        self.save_database()
            