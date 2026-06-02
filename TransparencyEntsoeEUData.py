import pandas as pd
import numpy as np
import requests
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from entsoe import EntsoePandasClient
from datetime import datetime, timezone

def getTransparencyEntsoeEUData():
    # B01 = Biomass; B02 = Fossil Brown coal/Lignite; B03 = Fossil Coal-derived gas; B04 = Fossil Gas; B05 = Fossil Hard coal; B06 = Fossil Oil; B07 = Fossil Oil shale; B08 = Fossil Peat; 
    # B09 = Geothermal; B10 = Hydro Pumped Storage; B11 = Hydro Run-of-river and poundage; B12 = Hydro Water Reservoir; B13 = Marine; B14 = Nuclear; B15 = Other renewable; B16 = Solar; 
    # B17 = Waste; B18 = Wind Offshore; B19 = Wind Onshore; B20 = Other; B25 = Energy storage
        
    country_code = 'PL'
    client = EntsoePandasClient(api_key='3d91fe70-07f4-4f69-851b-18c1b12c9005')
    start = pd.Timestamp('2026-05-01 00:00:00', tz='Europe/Warsaw')
    end = pd.Timestamp('2026-06-01 00:00:00', tz='Europe/Warsaw')
    generationPerType = client.query_generation(country_code, start=start, end=end, psr_type=None, resolution='60min')
    generationPerType.info()    
    
    colors = ['#A83C85', "#833F0F", "#642509", "#304F77", "#252525", '#A9A9A9', '#87CEEB', '#87CEEB', '#4682B4', '#1E90FF', '#D3D3D3', "#7DA37D", '#FFD700', '#4169E1']
    plt.figure(figsize=(20, 10))
    plt.stackplot(generationPerType.index, generationPerType.values.T, labels=generationPerType.columns, colors=colors, alpha=0.8)
    #plt.title('MW źródeł energii', fontsize=14)
    plt.xlabel(f'Data  {start.tz_localize(None)} - {end.tz_localize(None)}', fontsize=12)
    plt.ylabel('PL: Generowana moc MW', fontsize=12)
    plt.legend(loc='upper center', ncol=4, framealpha=0.3, fontsize=8)
    #plt.tight_layout()
    plt.show()

    generationPerTypeNoCSources = generationPerType.iloc[:, [6,7,8,9,11,12,13]]
    generationPerTypeCSources = generationPerType.iloc[:, [0,1,2,3,4,5,10]]
    valuesNoCSources = np.sum(generationPerTypeNoCSources.values, axis=1)
    valuesCSources = np.sum(generationPerTypeCSources.values, axis=1)    
    generationValuesCNoCSources = {
            'valuesNoCSources': valuesNoCSources,
            'valuesCSources': valuesCSources
        }
    generationValuesCNoCSourcesDf = pd.DataFrame(generationValuesCNoCSources)
    generationPercValuesCNoCSourcesDf = generationValuesCNoCSourcesDf.div(generationValuesCNoCSourcesDf.sum(axis=1), axis=0) * 100
    plt.figure(figsize=(20, 10))
    plt.stackplot(generationPerType.index, generationPercValuesCNoCSourcesDf.T, labels=['Energia_el ze żródeł bez spalania pierwiastka C', 'Energia_el ze żródeł spalania pierwiastka C'],
                    colors=["#048F0B", "#A3A3A3"], 
                    alpha=0.8)
    plt.xlabel(f'Data  {start.tz_localize(None)} - {end.tz_localize(None)}', fontsize=12)
    plt.ylabel('PL: %_udziału źródeł energii', fontsize=12)
    plt.legend(loc='upper center', ncol=4, framealpha=0.3, fontsize=10)
    plt.show()

    # mniejszy zakres
    start = pd.Timestamp('2026-05-29 00:00:00', tz='Europe/Warsaw')
    end = pd.Timestamp('2026-05-29 23:45:00', tz='Europe/Warsaw')
    generationPerType = client.query_generation(country_code, start=start, end=end, psr_type=None)
    plt.figure(figsize=(20, 10))
    plt.stackplot(generationPerType.index, generationPerType.values.T, labels=generationPerType.columns, colors=colors, alpha=0.8)
    plt.xlabel(f'Data  {start.tz_localize(None)} - {end.tz_localize(None)}', fontsize=12)
    plt.ylabel('PL: Generowana moc MW', fontsize=12)
    plt.legend(loc='upper center', ncol=4, framealpha=0.3, fontsize=8)
    plt.show()
    
    generationPerTypeValuesDf = pd.DataFrame(generationPerType.values)
    generationPerTypePercDf = generationPerTypeValuesDf.div(generationPerTypeValuesDf.sum(axis=1), axis=0) * 100
    plt.figure(figsize=(20, 10))
    plt.stackplot(generationPerType.index, generationPerTypePercDf.T, labels=generationPerType.columns, colors=colors, alpha=0.8)
    plt.xlabel(f'Data  {start.tz_localize(None)} - {end.tz_localize(None)}', fontsize=12)
    plt.ylabel('PL: %_udziału źródeł energii', fontsize=12)
    plt.legend(loc='upper center', ncol=4, framealpha=0.3, fontsize=8)
    plt.show()
    
    generationPerTypeNoCSources = generationPerType.iloc[:, [6,7,8,9,11,12,13]]
    generationPerTypeCSources = generationPerType.iloc[:, [0,1,2,3,4,5,10]]
    valuesNoCSources = np.sum(generationPerTypeNoCSources.values, axis=1)
    valuesCSources = np.sum(generationPerTypeCSources.values, axis=1)    
    generationValuesCNoCSources = {
            'valuesNoCSources': valuesNoCSources,
            'valuesCSources': valuesCSources
        }
    generationValuesCNoCSourcesDf = pd.DataFrame(generationValuesCNoCSources)
    generationPercValuesCNoCSourcesDf = generationValuesCNoCSourcesDf.div(generationValuesCNoCSourcesDf.sum(axis=1), axis=0) * 100
    plt.figure(figsize=(20, 10))
    plt.stackplot(generationPerType.index, generationPercValuesCNoCSourcesDf.T, labels=['Energia_el ze żródeł bez spalania pierwiastka C', 'Energia_el ze żródeł spalania pierwiastka C'],
                    colors=["#048F0B", "#A3A3A3"], 
                    alpha=0.8)
    plt.xlabel(f'Data  {start.tz_localize(None)} - {end.tz_localize(None)}', fontsize=12)
    plt.ylabel('PL: %_udziału źródeł energii', fontsize=12)
    plt.legend(loc='upper center', ncol=4, framealpha=0.3, fontsize=10)
    plt.show()
    return