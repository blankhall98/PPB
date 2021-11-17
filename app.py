import pandas as pd
import numpy as np

from inputs import Inputs, db_Inputs
from matcher import DBM

m = DBM(Inputs,db_Inputs)
m.match_databases()
PPB = m.ppb
print(PPB['CLAVE_NA'].value_counts())
m.save_database()