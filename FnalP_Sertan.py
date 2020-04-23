
import pandas as pd
import numpy as np
import category_encoders
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from pandas import DataFrame
from datetime import datetime
from zipfile import ZipFile

desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',10)

'''
#with ZipFile("./df_2019-2020.zip",'r') as zipo:
    print(zipo.namelist())
    zipo.extractall()
'''


def basic_inf(data):
    print(data.head())
    print("DATA INFORMATION:")
    print(data.info)
    print("SOME STATS:")
    stats = data.describe(include='all')
    print(stats)
    print("DATA TYPES:")
    print(data.dtypes)
    print("NUMBER OF NULL VALUES:")
    print(data.isna().sum())
    print(data.shape)


df = pd.read_csv("./df_2019-2020.csv", delimiter=',')
print("BASIC INFO FOR the ORIGINAL DATA:")
basic_inf(df)
print()


'''
These are the columns I was playing with, feel free to add subtract columns of you wish
'''

my_col2 = ['CMPLNT_FR_DT',      'CMPLNT_FR_TM', 'CRM_ATPT_CPTD_CD', 'ADDR_PCT_CD', 'LAW_CAT_CD',
          'BORO_NM',     'LOC_OF_OCCUR_DESC', 'PREM_TYP_DESC', 'JURISDICTION_CODE',
           'VIC_AGE_GROUP', 'VIC_RACE', 'VIC_SEX']

my_col = ['CMPLNT_FR_DT',      'CMPLNT_FR_TM',   'ADDR_PCT_CD', 'KY_CD',             'PD_CD',
          'CRM_ATPT_CPTD_CD',  'LAW_CAT_CD',     'BORO_NM',     'LOC_OF_OCCUR_DESC', 'PREM_TYP_DESC',
          'JURISDICTION_CODE', 'SUSP_AGE_GROUP', 'SUSP_RACE',   'SUSP_SEX',          'VIC_AGE_GROUP',
          'VIC_RACE',          'VIC_SEX']


df2 = df[my_col].dropna(axis=0, subset=my_col)
print("DF2 INFORMATION:")
basic_inf(df2)



def column_desc(data):

    #col_catog = data.columns[data.dtypes == ('category')]

    col_catog = ['CRM_ATPT_CPTD_CD', 'ADDR_PCT_CD', 'LAW_CAT_CD',
               'BORO_NM', 'LOC_OF_OCCUR_DESC', 'PREM_TYP_DESC', 'JURISDICTION_CODE',
               'VIC_AGE_GROUP', 'VIC_RACE', 'VIC_SEX']

    for cols in col_catog:
        print("COLUMN:", cols)
        print("UNIQUE VALUES:")
        print(data[cols].unique())
        print()
        print("VALUES COUNTS:")
        print(data[cols].value_counts())
        print()


column_desc(df2)
print("====" * 50)


def dropRows(data):
    drops = []
    for i, row in data.iterrows():
        if row["SUSP_AGE_GROUP"] not in ["<18", "18-24", "25-44", "45-64", "65+"]:
            drops.append(i)
        if row["SUSP_SEX"]       not in ["M","F"]:
            drops.append(i)
        if row["VIC_AGE_GROUP"]  not in ["<18", "18-24", "25-44", "45-64", "65+"]:
            drops.append(i)
        if row["VIC_SEX"]        not in ["M","F"]:
            drops.append(i)
    return data.drop(drops).reset_index(drop=True)


df3 = dropRows(df2)


def dateConv(data):
    a = []
    b = []
    for i, row in data.iterrows():
        time_ob = datetime.strptime(row["CMPLNT_FR_TM"], "%H:%M:%S")
        date_ob = datetime.strptime(row["CMPLNT_FR_DT"], "%Y-%m-%d")
        a.append(time_ob.minute * 60 + time_ob.hour * 3600)
        b.append(date_ob.month * 100 + date_ob.day * 1)
    data['incdt_time'] = a
    data['incdt_date'] = b
    return data


df4 = dateConv(df3)
print("DF3 INFORMATION:")
basic_inf(df4)
column_desc(df4)
print("====" * 50)

def grpRow(data):
    premis_group = []
    for i, row in data.iterrows():
        if row["PREM_TYP_DESC"] in ['RESIDENCE-HOUSE', 'MAILBOX OUTSIDE']:
            premis_group.append(1)

        elif row["PREM_TYP_DESC"] in ['RESIDENCE - PUBLIC HOUSING']:
            premis_group.append(2)

        elif row["PREM_TYP_DESC"] == ('STREET'):
            premis_group.append(3)

        elif row["PREM_TYP_DESC"] in ['MOSQUE','OTHER HOUSE OF WORSHIP','CHURCH', 'SYNAGOGUE']:
            premis_group.append(4)

        elif row["PREM_TYP_DESC"] in ['PARKING LOT/GARAGE (PUBLIC)', 'PARKING LOT/GARAGE (PRIVATE)', 'HIGHWAY/PARKWAY',
                                      'TUNNEL', 'BRIDGE','OPEN AREAS (OPEN LOTS)', 'CONSTRUCTION SITE',
                                      'STORAGE FACILITY', 'ABANDONED BUILDING', 'CEMETERY', 'HOMELESS SHELTER']:
            premis_group.append(5)

        elif row["PREM_TYP_DESC"] in ['BUS STOP','BUS (OTHER)', 'BUS (NYC TRANSIT)', 'FERRY/FERRY TERMINAL',
                                      'BUS TERMINAL','TRANSIT FACILITY (OTHER)','TAXI (LIVERY LICENSED)',
                                      'TAXI (YELLOW LICENSED)', 'AIRPORT TERMINAL','TRAMWAY',
                                      'TAXI/LIVERY (UNLICENSED)']:
            premis_group.append(6)

        elif row["PREM_TYP_DESC"] in ['HOSPITAL', 'DOCTOR/DENTIST OFFICE']:
            premis_group.append(7)

        elif row["PREM_TYP_DESC"] in ['ATM','BANK']:
            premis_group.append(8)

        elif row["PREM_TYP_DESC"] in ['RESTAURANT/DINER','BAR/NIGHT CLUB', 'HOTEL/MOTEL','MARINA/PIER',
                                      'SOCIAL CLUB/POLICY']:
            premis_group.append(9)

        elif row["PREM_TYP_DESC"] in ['PUBLIC BUILDING', 'GAS STATION']:
            premis_group.append(10)

        elif row["PREM_TYP_DESC"] in ['PRIVATE/PAROCHIAL SCHOOL', 'PUBLIC SCHOOL','DAYCARE FACILITY',
                                      'PARK/PLAYGROUND']:
            premis_group.append(11)

        elif row["PREM_TYP_DESC"] in ['RESIDENCE - APT. HOUSE']:
            premis_group.append(12)

        else:
            premis_group.append(30)

    data['premis_var'] = premis_group
    return data


df5 = grpRow(df4)
print("DF5 INFORMATION:")
print(df5.head())


def encoder(data):

    B_encoder = category_encoders.BinaryEncoder(cols=['premis_var'])
    data = B_encoder.fit_transform(data)

    '''
    L_encoder = LabelEncoder()
    data['BORO'] = L_encoder.fit_transform(data['BORO_NM'])
    data['VIC_AGE'] = L_encoder.fit_transform(data['VIC_AGE_GROUP'])
    data['LOC_DESC'] = L_encoder.fit_transform(data['LOC_OF_OCCUR_DESC'])
    data['VICM_RAC'] = L_encoder.fit_transform(data['VIC_RACE'])
    data['VICM_SEX'] = L_encoder.fit_transform(data['VIC_SEX'])
    '''

    OH_encoder = OneHotEncoder()
    hc1 = DataFrame(OH_encoder.fit_transform(data['BORO_NM'].values.reshape(-1,1)).toarray(),
                    columns = ['BORO1', 'BORO2','BORO3', 'BORO4', 'BORO5'])
    hc2 = DataFrame(OH_encoder.fit_transform(data['VIC_AGE_GROUP'].values.reshape(-1, 1)).toarray(),
                    columns=['VIC_AGE1', 'VIC_AGE2', 'VIC_AGE3', 'VIC_AGE4', 'VIC_AGE5'])
    hc3 = DataFrame(OH_encoder.fit_transform(data['LOC_OF_OCCUR_DESC'].values.reshape(-1, 1)).toarray(),
                    columns=['LOC_DESC1', 'LOC_DESC2', 'LOC_DESC3', 'LOC_DESC4'])
    hc4 = DataFrame(OH_encoder.fit_transform(data['VIC_RACE'].values.reshape(-1, 1)).toarray(),
                    columns=['VIC_RACE1', 'VIC_RACE2', 'VIC_RACE3', 'VIC_RACE4', 'VIC_RACE5',
                             'VIC_RACE6', 'VIC_RACE7'])
    hc5 = DataFrame(OH_encoder.fit_transform(data['VIC_SEX'].values.reshape(-1, 1)).toarray(),
                    columns=['VICM_SEX1', 'VICM_SEX2'])
    hc6 = DataFrame(OH_encoder.fit_transform(data['SUSP_RACE'].values.reshape(-1, 1)).toarray(),
                    columns=['SUSP_RACE1', 'SUSP_RACE2', 'SUSP_RACE3', 'SUSP_RACE4', 'SUSP_RACE5',
                             'SUSP_RACE6', 'SUSP_RACE7'])
    hc7 = DataFrame(OH_encoder.fit_transform(data['VIC_SEX'].values.reshape(-1, 1)).toarray(),
                    columns=['SUSP_SEX1', 'SUSP_SEX2'])
    data = pd.concat([data,hc1,hc2,hc3,hc4,hc5,hc6,hc7], axis=1)
    return data


df6 = encoder(df5)
print("DF6 INFORMATION:")
print(df6.head())

