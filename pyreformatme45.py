import pandas as pd
import numpy as np
import os
from os import listdir
from datetime import datetime

def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

def main():
    
    

    basepath = 'process/'

    filenames = find_csv_filenames(basepath)
    for name in filenames:        
        reformat(name)


def reformat(filename):

    NA_VALUES = [9999, 99999, '9999', '99999', '/', '//', '///', '////', '\\', '.', '#REF!', '#VALUE!', 'STNR', '#N/A', '#', 'N', '/A', '`', '*', 'Z', 'A', 'C', 'AC', '*/', '+', 'CI', '0S', 'y', 'BN ', 'CNS SL RA', 'CLD DECR', 'ALSE', 'cdd', 'L' , 'x', 'E', '0`', '3            tidak ada hujan', 'FALSE']
    NA_VALUES_QFF_QFE = NA_VALUES[:]
    NA_VALUES_QFF_QFE.remove(9999)
    NA_VALUES_QFF_QFE.remove('9999')

    df = pd.read_csv (r'process/'+filename, 
    skipinitialspace = True,
    # sep=';'
    ) #(r'sample/test ingest me45.csv')
    print(df)

    #todo: check if columen exist
    #https://stackoverflow.com/questions/24870306/how-to-check-if-a-column-exists-in-pandas

    ##########
    ##### TdTdTd  
    ##########

    df['TdTdTd'] = df['TdTdTd'][~df['TdTdTd'].isin(NA_VALUES)]
    df['TdTdTd'] = df['TdTdTd'][ df['TdTdTd'].notnull() ].astype(int) / 10    
    df['TdTdTd'] = df['TdTdTd'].fillna(9999).astype(float)    
    
    ##########
    ##### N
    ##########

    def funcN(n):
        if n == '0': result = 0
        elif n == '1': result = 1
        elif n == '2': result = 2
        elif n == '3': result = 3
        elif n == '4': result = 4
        elif n == '5': result = 5
        elif n == '6': result = 6
        elif n == '7': result = 7
        elif n == '8': result = 8
        elif n == '9': result = 9
        elif n == '/': result = '//' 
        elif n == '//': result = '//' 
        else: result = 9999
        return(result)

    df['N'] = df['N'].astype('str').apply(funcN)

    ##########
    ##### dd
    ##########

    def funcdd(n):
        if n == '0': dd = 0 #dari hasil diskusi diisi 29        
        elif n == '1': dd = 1
        elif n == '2': dd = 2
        elif n == '3': dd = 3
        elif n == '4': dd = 4
        elif n == '5': dd = 5
        elif n == '6': dd = 6
        elif n == '7': dd = 7
        elif n == '8': dd = 8
        elif n == '9': dd = 9
        elif n == '10': dd = 10
        elif n == '11': dd = 11
        elif n == '12': dd = 12
        elif n == '13': dd = 13
        elif n == '14': dd = 14
        elif n == '15': dd = 15
        elif n == '16': dd = 16
        elif n == '17': dd = 17
        elif n == '18': dd = 18
        elif n == '19': dd = 19
        elif n == '20': dd = 20
        elif n == '21': dd = 21
        elif n == '22': dd = 22
        elif n == '23': dd = 23
        elif n == '24': dd = 24
        elif n == '25': dd = 25
        elif n == '26': dd = 26
        elif n == '27': dd = 27
        elif n == '28': dd = 28
        elif n == '29': dd = 29
        elif n == '30': dd = 30
        elif n == '31': dd = 31
        elif n == '32': dd = 32
        elif n == '33': dd = 33
        elif n == '34': dd = 34
        elif n == '35': dd = 35
        elif n == '36': dd = 36
        elif n == '99': dd = 99        
        else: dd = 9999
        return(dd)

    df['dd'] = df['dd'].astype('str').apply(funcdd)
    df.loc[df['dd'] != 9999, 'dd'] = pd.to_numeric(df['dd']) * 10      

    
    ##########
    ##### ff
    ##########

    df['ff'] = df['ff'][~df['ff'].isin(NA_VALUES)]
    df['ff'] = df['ff'].fillna(9999).astype(int)

    ##########
    ##### VV
    ##########

    df['VV'] = df['VV'].astype('str').apply(funcVV)

    ##########
    ##### ww
    ##########

    df['ww'] = df['ww'][~df['ww'].isin(NA_VALUES)]
    df['ww'] = df['ww'].fillna(9999).astype(int)
    df['ww'] = df['ww'].astype('str').apply(funcww)


    def funcW1W2(n):
        if n == '0': result = 0
        elif n == '1': result = 1
        elif n == '2': result = 2
        elif n == '3': result = 3
        elif n == '4': result = 4
        elif n == '5': result = 5
        elif n == '6': result = 6
        elif n == '7': result = 7
        elif n == '8': result = 8
        elif n == '9': result = 9        
        else: result = 9999
        return(result)

    ##########
    ##### W1
    ##########

    df['W1'] = df['W1'].astype('str').apply(funcW1W2)

    ##########
    ##### W2
    ##########

    df['W2'] = df['W2'].astype('str').apply(funcW1W2)

    ##########
    ##### QFF
    ##########

    df['QFF'] = df['QFF'][~df['QFF'].isin(NA_VALUES_QFF_QFE)]
    df['QFF'] = df['QFF'][df['QFF'].astype(str).str.len() <= 6] # untuk memfilter yang diproses hanya 6 digit bilangan termasuk .0
    df['QFF'] = df['QFF'][df['QFF'].notnull()].astype(int).astype(str).str.zfill(4) 
    df.loc[df['QFF'].astype(str).str[0] == '0', 'QFF'] = (10000 + pd.to_numeric(df['QFF'])) / 10  
    df.loc[df['QFF'].astype(str).str[0] == '9', 'QFF'] = pd.to_numeric(df['QFF']) / 10      
    df['QFF'] = df['QFF'].fillna(9999).astype(float)  

    #############
    ##### TtTtTt
    #############

    df['TtTtTt'] = df['TtTtTt'][~df['TtTtTt'].isin(NA_VALUES)]
    df['TtTtTt'] = df['TtTtTt'][ df['TtTtTt'].notnull() ].astype(int) / 10 
    df['TtTtTt'] = df['TtTtTt'].fillna(9999).astype(float)

    def funcNh(n):
        if n == '0': result = 0
        elif n == '1': result = 1
        elif n == '2': result = 2
        elif n == '3': result = 3
        elif n == '4': result = 4
        elif n == '5': result = 5
        elif n == '6': result = 6
        elif n == '7': result = 7
        elif n == '8': result = 8
        elif n == '9': result = 9
        elif n == '/': result = '//' 
        elif n == '//': result = '//' 
        else: result = 9999
        return(result)

    ##########
    ##### Nh
    ##########

    df['Nh'] = df['Nh'].astype('str').apply(funcNh)



    def funcCLCMCHNsC(n):
        if n == '0': clcmch = 0
        elif n == '1': clcmch = 1
        elif n == '2': clcmch = 2
        elif n == '3': clcmch = 3
        elif n == '4': clcmch = 4
        elif n == '5': clcmch = 5
        elif n == '6': clcmch = 6
        elif n == '7': clcmch = 7
        elif n == '8': clcmch = 8
        elif n == '9': clcmch = 9
        elif n == '/': clcmch = '//' 
        elif n == '//': clcmch = '//' 
        else: clcmch = 9999
        return(clcmch)

    ###########
    ##### CL
    ###########

    df['CL'] = df['CL'].astype('str').apply(funcCLCMCHNsC)
    

    ###########
    ##### h	
    ###########
    
    def funch(n):
        if n == '0': h = 50
        elif n == '1': h = 100
        elif n == '2': h = 200
        elif n == '3': h = 300
        elif n == '4': h = 600
        elif n == '5': h = 1000
        elif n == '6': h = 1500
        elif n == '7': h = 2000
        elif n == '8': h = 2500
        elif n == '9': h = 2501 #dari hasil diskusi diisi 2501
        # elif n == '/': h = '//' # di bmkgsoft tidak menerima garis miring untuk parameter ini
        # elif n == '//': h = '//' # di bmkgsoft tidak menerima garis miring untuk parameter ini
        else: h = 9999
        return(h)

    df['h'] = df['h'].astype('str').apply(funch)

    ##########
    ##### CM
    ##########

    df['CM'] = df['CM'].astype('str').apply(funcCLCMCHNsC)
    
    ##########
    ##### CH
    ##########

    df['CH'] = df['CH'].astype('str').apply(funcCLCMCHNsC)

    ##########
    ##### Ns_1

    df['Ns_1'] = df['Ns_1'].astype('str').apply(funcCLCMCHNsC)

    # def funcC(n):
    #     if n == '0': c = 0
    #     elif n == '1': c = 1
    #     elif n == '2': c = 2
    #     elif n == '3': c = 3
    #     elif n == '4': c = 4
    #     elif n == '5': c = 5
    #     elif n == '6': c = 6
    #     elif n == '7': c = 7
    #     elif n == '8': c = 8
    #     elif n == '9': c = 9
    #     elif n == '/': c = '//' #todo: nanti dipastikan lagi ke LDM apa ada tanda garis miring
    #     elif n == '//': c = '//' #todo: nanti dipastikan lagi ke LDM apa ada tanda garis miring
    #     else: c = 9999
    #     return(c)

    ##########
    ##### C_1
    ##########

    df['C_1'] = df['C_1'].astype('str').apply(funcCLCMCHNsC) 




    def funcHshs(n):
        if n == '0': hshs = 29 #dari hasil diskusi diisi 29        
        elif n == '1': hshs = 30
        elif n == '2': hshs = 60
        elif n == '3': hshs = 90
        elif n == '4': hshs = 120
        elif n == '5': hshs = 150
        elif n == '6': hshs = 180
        elif n == '7': hshs = 210
        elif n == '8': hshs = 240
        elif n == '9': hshs = 270
        elif n == '10': hshs = 300
        elif n == '11': hshs = 330
        elif n == '12': hshs = 360
        elif n == '13': hshs = 390
        elif n == '14': hshs = 420
        elif n == '15': hshs = 450
        elif n == '16': hshs = 480
        elif n == '17': hshs = 510
        elif n == '18': hshs = 540
        elif n == '19': hshs = 570
        elif n == '20': hshs = 600
        elif n == '21': hshs = 630
        elif n == '22': hshs = 660
        elif n == '23': hshs = 690
        elif n == '24': hshs = 720
        elif n == '25': hshs = 750
        elif n == '26': hshs = 780
        elif n == '27': hshs = 810
        elif n == '28': hshs = 840
        elif n == '29': hshs = 870
        elif n == '30': hshs = 900
        elif n == '31': hshs = 930
        elif n == '32': hshs = 960
        elif n == '33': hshs = 990
        elif n == '34': hshs = 1020
        elif n == '35': hshs = 1050
        elif n == '36': hshs = 1080
        elif n == '37': hshs = 1110
        elif n == '38': hshs = 1140
        elif n == '39': hshs = 1170
        elif n == '40': hshs = 1200
        elif n == '41': hshs = 1230
        elif n == '42': hshs = 1260
        elif n == '43': hshs = 1290
        elif n == '44': hshs = 1320
        elif n == '45': hshs = 1350
        elif n == '46': hshs = 1380
        elif n == '47': hshs = 1410
        elif n == '48': hshs = 1440
        elif n == '49': hshs = 1470
        elif n == '50': hshs = 1500
        elif n == '51': hshs = 9999 #dari hasil diskusi diisi 9999
        elif n == '52': hshs = 9999 #dari hasil diskusi diisi 9999
        elif n == '53': hshs = 9999 #dari hasil diskusi diisi 9999
        elif n == '54': hshs = 9999 #dari hasil diskusi diisi 9999
        elif n == '55': hshs = 9999 #dari hasil diskusi diisi 9999
        elif n == '56': hshs = 1800
        elif n == '57': hshs = 2100
        elif n == '58': hshs = 2400
        elif n == '59': hshs = 2700
        elif n == '60': hshs = 3000
        elif n == '61': hshs = 3300
        elif n == '62': hshs = 3600
        elif n == '63': hshs = 3900
        elif n == '64': hshs = 4200
        elif n == '65': hshs = 4500
        elif n == '66': hshs = 4800
        elif n == '67': hshs = 5100
        elif n == '68': hshs = 5400
        elif n == '69': hshs = 5700
        elif n == '70': hshs = 6000
        elif n == '71': hshs = 6300
        elif n == '72': hshs = 6600
        elif n == '73': hshs = 6900
        elif n == '74': hshs = 7200
        elif n == '75': hshs = 7500
        elif n == '76': hshs = 7800
        elif n == '77': hshs = 8100
        elif n == '78': hshs = 8400
        elif n == '79': hshs = 8700
        elif n == '80': hshs = 9000
        elif n == '81': hshs = 10500
        elif n == '82': hshs = 12000
        elif n == '83': hshs = 13500
        elif n == '84': hshs = 15000
        elif n == '85': hshs = 16500
        elif n == '86': hshs = 18000
        elif n == '87': hshs = 19500
        elif n == '88': hshs = 21000
        elif n == '89': hshs = 21001 #dari hasil diskusi diisi 21001
        elif n == '90': hshs = 9999 #dari hasil diskusi ini adalah pengamatan laut, diisi 9999
        elif n == '91': hshs = 9999 #dari hasil diskusi ini adalah pengamatan laut, diisi 9999
        elif n == '92': hshs = 9999 #dari hasil diskusi ini adalah pengamatan laut, diisi 9999
        elif n == '93': hshs = 9999 #dari hasil diskusi ini adalah pengamatan laut, diisi 9999
        elif n == '94': hshs = 9999 #dari hasil diskusi ini adalah pengamatan laut, diisi 9999
        elif n == '95': hshs = 9999 #dari hasil diskusi ini adalah pengamatan laut, diisi 9999
        elif n == '96': hshs = 9999 #dari hasil diskusi ini adalah pengamatan laut, diisi 9999
        elif n == '97': hshs = 9999 #dari hasil diskusi ini adalah pengamatan laut, diisi 9999
        elif n == '98': hshs = 9999 #dari hasil diskusi ini adalah pengamatan laut, diisi 9999
        elif n == '99': hshs = 9999 #dari hasil diskusi ini adalah pengamatan laut, diisi 9999
        else: hshs = 9999
        return(hshs)

    ##########
    ##### Hshs_1	
    ##########
    df['Hshs_1'] = df['Hshs_1'].astype('str').apply(funcHshs)

    ##########
    ##### Ns_2
    ##########

    df['Ns_2'] = df['Ns_2'].astype('str').apply(funcCLCMCHNsC)

    ##########
    ##### C_2
    ##########

    df['C_2'] = df['C_2'].astype('str').apply(funcCLCMCHNsC)

    ##########
    ##### Hshs_2	
    ##########

    df['Hshs_2'] = df['Hshs_2'].apply(funcHshs)

    ##########
    ##### Ns_3
    ##########

    df['Ns_3'] = df['Ns_3'].astype('str').apply(funcCLCMCHNsC)

    ##########
    ##### C_3
    ##########
    
    df['C_3'] = df['C_3'].astype('str').apply(funcCLCMCHNsC) # df['C_3'].apply(funcC)

    ##########
    ##### Hshs_3	
    ##########

    df['Hshs_3'] = df['Hshs_3'].apply(funcHshs)

    def funce(n):
        if n == '0': result = 0
        elif n == '1': result = 1
        elif n == '2': result = 2
        elif n == '3': result = 3
        elif n == '4': result = 4
        elif n == '5': result = 5
        elif n == '6': result = 6
        elif n == '7': result = 7
        elif n == '8': result = 8
        elif n == '9': result = 9        
        else: result = 9999
        return(result)

    ##########
    ##### e
    ##########

    df['e'] = df['e'].astype('str').apply(funce)

    ##########
    ##### UU
    ##########

    df['UU'] = df['UU'][~df['UU'].isin(NA_VALUES)]
    df['UU'] = df['UU'].fillna(9999).astype(int)

    ##########
    ##### QFE
    ##########

    df['QFE'] = df['QFE'][~df['QFE'].isin(NA_VALUES_QFF_QFE)]
    df['QFE'] = df['QFE'][df['QFE'].astype(str).str.len() <= 6] # untuk memfilter yang diproses hanya 6 digit bilangan termasuk .0
    df['QFE'] = df['QFE'][df['QFE'].notnull()].astype(int).astype(str).str.zfill(4) 
    df.loc[df['QFE'].astype(str).str[0] == '0', 'QFE'] = (10000 + pd.to_numeric(df['QFE'])) / 10  
    df.loc[df['QFE'].astype(str).str[0] == '9', 'QFE'] = pd.to_numeric(df['QFE']) / 10      
    df['QFE'] = df['QFE'].fillna(9999).astype(float)

    ##########
    ##### TwTwTw
    ##########

    df['TwTwTw'] = df['TwTwTw'][~df['TwTwTw'].isin(NA_VALUES)]
    df['TwTwTw'] = df['TwTwTw'][ df['TwTwTw'].notnull() ].astype(int) / 10 
    df['TwTwTw'] = df['TwTwTw'].fillna(9999).astype(float)

    # RRR	
    # panduan hal 24
    df['RRR'] = df['RRR'].astype('str').apply(funcRRR)


    def functR(n):        
        if n == '1': result = 1
        elif n == '2': result = 2
        elif n == '3': result = 3
        elif n == '4': result = 4
        elif n == '5': result = 5
        elif n == '6': result = 6
        elif n == '7': result = 7
        elif n == '8': result = 8
        elif n == '9': result = 9        
        else: result = 9999
        return(result)

    ##########
    ##### tR
    ##########

    df['tR'] = df['tR'].astype('str').apply(functR)


    ##########
    ##### TxTxTx
    ##########
    
    df['TxTxTx'] = df['TxTxTx'][~df['TxTxTx'].isin(NA_VALUES)]    
    df['TxTxTx'] = df['TxTxTx'][ df['TxTxTx'].notnull() ].astype(int) / 10 
    df['TxTxTx'] = df['TxTxTx'].fillna(9999).astype(float)

    ##########
    ##### TnTnTn
    ##########

    df['TnTnTn'] = df['TnTnTn'][~df['TnTnTn'].isin(NA_VALUES)]
    df['TnTnTn'] = df['TnTnTn'][ df['TnTnTn'].notnull() ].astype(int) / 10
    df['TnTnTn'] = df['TnTnTn'].fillna(9999).astype(float)

    # EEE
    df['EEE'] = df['EEE'][~df['EEE'].isin(NA_VALUES)]
    df['EEE'] = df['EEE'][ df['EEE'].notnull() ].astype(int) / 10
    df['EEE'] = df['EEE'].fillna(9999).astype(float)
    
    # F24F24F24F24	-> OK #todo: dicek lagi
    df['F24F24F24F24'] = df['F24F24F24F24'][~df['F24F24F24F24'].isin(NA_VALUES)]
    df['F24F24F24F24'] = df['F24F24F24F24'].fillna(9999).astype(int)

    # SSS	
    df['SSS'] = df['SSS'][~df['SSS'].isin(NA_VALUES)]
    df['SSS'] = df['SSS'][ df['SSS'].notnull() ].astype(int) / 10 
    df['SSS'] = df['SSS'].fillna(9999).astype(float)

    # E	-> OK
    df['E'] = df['E'][~df['E'].isin(NA_VALUES)]
    df['E'] = df['E'].fillna(9999).astype(int)

    def funcDLDMDH(n):
        if n == '0': result = 0
        elif n == '1': result = 1
        elif n == '2': result = 2
        elif n == '3': result = 3
        elif n == '4': result = 4
        elif n == '5': result = 5
        elif n == '6': result = 6
        elif n == '7': result = 7
        elif n == '8': result = 8
        elif n == '9': result = 9                
        else: result = 9999
        return(result)

    ##########
    ##### DL
    ##########

    df['DL'] = df['DL'].astype('str').apply(funcDLDMDH)

    ##########
    ##### DM
    ##########

    df['DM'] = df['DM'].astype('str').apply(funcDLDMDH)

    ##########
    ##### DH
    ##########

    df['DH'] = df['DH'].astype('str').apply(funcDLDMDH)


    # appp	
    # def funcappp(n):
    #     if n == 0: a = 1
    #     elif n == 1: a = 1
    #     elif n == 2: a = 1
    #     elif n == 3: a = 1
    #     elif n == 4: a = 1
    #     elif n == 5: a = -1
    #     elif n == 6: a = -1
    #     elif n == 7: a = -1
    #     elif n == 8: a = -1
    #     else: a = 9999
    #     return(a)
    
    def funcappp(n):
        if n < 5000: a = 1
        elif (n >= 5000) and (n <= 9000): a = -1        
        else: a = 1
        return(a)
    
    #todo: kalau nilai awalannya 0 maka hasilnya tidak sesuai (TAPI SAAT INI DICOBA SUDAH SOLVED)
    #todo: kalau nilainya lebih dari 9000 maka hasilnya tidak sesuai
    df['appp_help'] = df['appp'][~df['appp'].isin(NA_VALUES)]
    df['appp_help'] = df['appp_help'][df['appp_help'].notnull()].astype(str).apply(lambda x: x.zfill(4))      
    df['appp'] = df['appp_help'].str[1:].astype(float) * df['appp_help'].astype(float).apply(funcappp) / 10
    df['appp'] = df['appp'].fillna(9999).astype(float)

    del df['appp_help']    

    # P24P24P24	
    df['P24P24P24'] = df['P24P24P24'].fillna(9999)    
    df['P24P24P24'] = df['P24P24P24'][~df['P24P24P24'].isin(NA_VALUES)].astype(str).apply(lambda x: x.zfill(3))    
    df.loc[df['P24P24P24'].astype(str).str[0] != '5', 'P24P24P24'] = pd.to_numeric(df['P24P24P24']) / 10
    df.loc[df['P24P24P24'].astype(str).str[0] == '5', 'P24P24P24'] = (pd.to_numeric(df['P24P24P24']) - 500 )/ 10 * -1    
    df['P24P24P24'] = df['P24P24P24'].fillna(9999)

    def funciW(n):
        if n == '0': result = 0
        elif n == '1': result = 1        
        elif n == '3': result = 3
        elif n == '4': result = 4        
        else: result = 9999
        return(result)

    ##########
    ##### iW
    ##########

    df['iW'] = df['iW'].astype('str').apply(funciW)

    def funciX(n):        
        if n == '1': result = 1
        elif n == '2': result = 2
        elif n == '3': result = 3
        elif n == '4': result = 4
        elif n == '5': result = 5
        elif n == '6': result = 6
        else: result = 9999
        return(result)

    ##########
    ##### iX
    ##########

    df['iX'] = df['iX'].astype('str').apply(funciX)


    def funciR(n):        
        if n == '0': result = 0
        elif n == '1': result = 1
        elif n == '2': result = 2
        elif n == '3': result = 3
        elif n == '4': result = 4        
        else: result = 9999
        return(result)


    ##########
    ##### iR
    ##########

    df['iR'] = df['iR'].astype('str').apply(funciR)

    def funciE(n):        
        if n == '0': result = 0
        elif n == '1': result = 1        
        else: result = 9999
        return(result)

    ##########
    ##### iE
    ##########

    df['iE'] = df['iE'].astype('str').apply(funciE)




    # Remove column 'C' dan 'D' karena tidak dibutuhkan saat ingest
    # where 1 is the axis number (0 for rows and 1 for columns.)
    df = df.drop('C', 1)
    df = df.drop('D', 1)


    #######
    # datetime object containing current date and time
    now = datetime.now()
    
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y%m%d%H%M")
    # print("date and time =", dt_string)	
    #####


    print(df)
    df.info(verbose=True)
    df.to_csv('output/'+'importME45_'+dt_string+' - '+filename, index=False)




def funcVV(n):
    if n == '0': vv = 0.09 #dari hasil diskusi diisi 0.09
    elif n == '1': vv = 0.1    
    elif n == '2': vv = 0.2
    elif n == '3': vv = 0.3
    elif n == '4': vv = 0.4
    elif n == '5': vv = 0.5
    elif n == '6': vv = 0.6
    elif n == '7': vv = 0.7
    elif n == '8': vv = 0.8
    elif n == '9': vv = 0.9
    elif n == '10': vv = 1
    elif n == '11': vv = 1.1
    elif n == '12': vv = 1.2
    elif n == '13': vv = 1.3
    elif n == '14': vv = 1.4
    elif n == '15': vv = 1.5
    elif n == '16': vv = 1.6
    elif n == '17': vv = 1.7
    elif n == '18': vv = 1.8
    elif n == '19': vv = 1.9
    elif n == '20': vv = 2
    elif n == '21': vv = 2.1
    elif n == '22': vv = 2.2
    elif n == '23': vv = 2.3
    elif n == '24': vv = 2.4
    elif n == '25': vv = 2.5
    elif n == '26': vv = 2.6
    elif n == '27': vv = 2.7
    elif n == '28': vv = 2.8
    elif n == '29': vv = 2.9
    elif n == '30': vv = 3
    elif n == '31': vv = 3.1
    elif n == '32': vv = 3.2
    elif n == '33': vv = 3.3
    elif n == '34': vv = 3.4
    elif n == '35': vv = 3.5
    elif n == '36': vv = 3.6
    elif n == '37': vv = 3.7
    elif n == '38': vv = 3.8
    elif n == '39': vv = 3.9
    elif n == '40': vv = 4
    elif n == '41': vv = 4.1
    elif n == '42': vv = 4.2
    elif n == '43': vv = 4.3
    elif n == '44': vv = 4.4
    elif n == '45': vv = 4.5
    elif n == '46': vv = 4.6
    elif n == '47': vv = 4.7
    elif n == '48': vv = 4.8
    elif n == '49': vv = 4.9
    elif n == '50': vv = 5
    elif n == '51': vv = 9999 #dari hasil diskusi diisi 9999
    elif n == '52': vv = 9999 #dari hasil diskusi diisi 9999
    elif n == '53': vv = 9999 #dari hasil diskusi diisi 9999
    elif n == '54': vv = 9999 #dari hasil diskusi diisi 9999
    elif n == '55': vv = 9999 #dari hasil diskusi diisi 9999
    elif n == '56': vv = 6
    elif n == '57': vv = 7
    elif n == '58': vv = 8
    elif n == '59': vv = 9
    elif n == '60': vv = 10
    elif n == '61': vv = 11
    elif n == '62': vv = 12
    elif n == '63': vv = 13
    elif n == '64': vv = 14
    elif n == '65': vv = 15
    elif n == '66': vv = 16
    elif n == '67': vv = 17
    elif n == '68': vv = 18
    elif n == '69': vv = 19
    elif n == '70': vv = 20
    elif n == '71': vv = 21
    elif n == '72': vv = 22
    elif n == '73': vv = 23
    elif n == '74': vv = 24
    elif n == '75': vv = 25
    elif n == '76': vv = 26
    elif n == '77': vv = 27
    elif n == '78': vv = 28
    elif n == '79': vv = 29
    elif n == '80': vv = 30
    elif n == '81': vv = 35
    elif n == '82': vv = 40
    elif n == '83': vv = 45
    elif n == '84': vv = 50
    elif n == '85': vv = 55
    elif n == '86': vv = 60
    elif n == '87': vv = 65
    elif n == '88': vv = 70
    elif n == '89': vv = 71 #dari hasil diskusi diisi 71
    elif n == '90': vv = 9999 #dari hasil diskusi pengamatan laut, diisi 9999
    elif n == '91': vv = 9999 #dari hasil diskusi pengamatan laut, diisi 9999
    elif n == '92': vv = 9999 #dari hasil diskusi pengamatan laut, diisi 9999
    elif n == '93': vv = 9999 #dari hasil diskusi pengamatan laut, diisi 9999
    elif n == '94': vv = 9999 #dari hasil diskusi pengamatan laut, diisi 9999
    elif n == '95': vv = 9999 #dari hasil diskusi pengamatan laut, diisi 9999
    elif n == '96': vv = 9999 #dari hasil diskusi pengamatan laut, diisi 9999
    elif n == '97': vv = 9999 #dari hasil diskusi pengamatan laut, diisi 9999
    elif n == '98': vv = 9999 #dari hasil diskusi pengamatan laut, diisi 9999
    elif n == '99': vv = 9999 #dari hasil diskusi pengamatan laut, diisi 9999
    else: vv = 9999
    return(vv)

def funcww(n):
    if n == '0': ww = 0
    elif n == '1': ww = 1    
    elif n == '2': ww = 2
    elif n == '3': ww = 3
    elif n == '4': ww = 4
    elif n == '5': ww = 5
    elif n == '6': ww = 6
    elif n == '7': ww = 7
    elif n == '8': ww = 8
    elif n == '9': ww = 9
    elif n == '10': ww = 10
    elif n == '11': ww = 11
    elif n == '12': ww = 12
    elif n == '13': ww = 13
    elif n == '14': ww = 14
    elif n == '15': ww = 15
    elif n == '16': ww = 16
    elif n == '17': ww = 17
    elif n == '18': ww = 18
    elif n == '19': ww = 19
    elif n == '20': ww = 20
    elif n == '21': ww = 21
    elif n == '22': ww = 22
    elif n == '23': ww = 23
    elif n == '24': ww = 24
    elif n == '25': ww = 25
    elif n == '26': ww = 26
    elif n == '27': ww = 27
    elif n == '28': ww = 28
    elif n == '29': ww = 29
    elif n == '30': ww = 30
    elif n == '31': ww = 31
    elif n == '32': ww = 32
    elif n == '33': ww = 33
    elif n == '34': ww = 34
    elif n == '35': ww = 35
    elif n == '36': ww = 36
    elif n == '37': ww = 37
    elif n == '38': ww = 38
    elif n == '39': ww = 39
    elif n == '40': ww = 40
    elif n == '41': ww = 41
    elif n == '42': ww = 42
    elif n == '43': ww = 43
    elif n == '44': ww = 44
    elif n == '45': ww = 45
    elif n == '46': ww = 46
    elif n == '47': ww = 47
    elif n == '48': ww = 48
    elif n == '49': ww = 49
    elif n == '50': ww = 50
    elif n == '51': ww = 51
    elif n == '52': ww = 52
    elif n == '53': ww = 53
    elif n == '54': ww = 54
    elif n == '55': ww = 55
    elif n == '56': ww = 56
    elif n == '57': ww = 57
    elif n == '58': ww = 58
    elif n == '59': ww = 59
    elif n == '60': ww = 60
    elif n == '61': ww = 61
    elif n == '62': ww = 62
    elif n == '63': ww = 63
    elif n == '64': ww = 64
    elif n == '65': ww = 65
    elif n == '66': ww = 66
    elif n == '67': ww = 67
    elif n == '68': ww = 68
    elif n == '69': ww = 69
    elif n == '70': ww = 70
    elif n == '71': ww = 71
    elif n == '72': ww = 72
    elif n == '73': ww = 73
    elif n == '74': ww = 74
    elif n == '75': ww = 75
    elif n == '76': ww = 76
    elif n == '77': ww = 77
    elif n == '78': ww = 78
    elif n == '79': ww = 79
    elif n == '80': ww = 80
    elif n == '81': ww = 81
    elif n == '82': ww = 82
    elif n == '83': ww = 83
    elif n == '84': ww = 84
    elif n == '85': ww = 85
    elif n == '86': ww = 86
    elif n == '87': ww = 87
    elif n == '88': ww = 88
    elif n == '89': ww = 89
    elif n == '90': ww = 90
    elif n == '91': ww = 91
    elif n == '92': ww = 92
    elif n == '93': ww = 93
    elif n == '94': ww = 94
    elif n == '95': ww = 95
    elif n == '96': ww = 96
    elif n == '97': ww = 97
    elif n == '98': ww = 98
    elif n == '99': ww = 99
    else: ww = 9999
    return(ww)

def funcRRR(n):
    if n == '0': rrr = 9999 #dari hasil diskusi diisi 9999
    elif n == '1': rrr = 1
    elif n == '2': rrr = 2
    elif n == '3': rrr = 3
    elif n == '4': rrr = 4
    elif n == '5': rrr = 5
    elif n == '6': rrr = 6
    elif n == '7': rrr = 7
    elif n == '8': rrr = 8
    elif n == '9': rrr = 9
    elif n == '10': rrr = 10
    elif n == '11': rrr = 11
    elif n == '12': rrr = 12
    elif n == '13': rrr = 13
    elif n == '14': rrr = 14
    elif n == '15': rrr = 15
    elif n == '16': rrr = 16
    elif n == '17': rrr = 17
    elif n == '18': rrr = 18
    elif n == '19': rrr = 19
    elif n == '20': rrr = 20
    elif n == '21': rrr = 21
    elif n == '22': rrr = 22
    elif n == '23': rrr = 23
    elif n == '24': rrr = 24
    elif n == '25': rrr = 25
    elif n == '26': rrr = 26
    elif n == '27': rrr = 27
    elif n == '28': rrr = 28
    elif n == '29': rrr = 29
    elif n == '30': rrr = 30
    elif n == '31': rrr = 31
    elif n == '32': rrr = 32
    elif n == '33': rrr = 33
    elif n == '34': rrr = 34
    elif n == '35': rrr = 35
    elif n == '36': rrr = 36
    elif n == '37': rrr = 37
    elif n == '38': rrr = 38
    elif n == '39': rrr = 39
    elif n == '40': rrr = 40
    elif n == '41': rrr = 41
    elif n == '42': rrr = 42
    elif n == '43': rrr = 43
    elif n == '44': rrr = 44
    elif n == '45': rrr = 45
    elif n == '46': rrr = 46
    elif n == '47': rrr = 47
    elif n == '48': rrr = 48
    elif n == '49': rrr = 49
    elif n == '50': rrr = 50
    elif n == '51': rrr = 51
    elif n == '52': rrr = 52
    elif n == '53': rrr = 53
    elif n == '54': rrr = 54
    elif n == '55': rrr = 55
    elif n == '56': rrr = 56
    elif n == '57': rrr = 57
    elif n == '58': rrr = 58
    elif n == '59': rrr = 59
    elif n == '60': rrr = 60
    elif n == '61': rrr = 61
    elif n == '62': rrr = 62
    elif n == '63': rrr = 63
    elif n == '64': rrr = 64
    elif n == '65': rrr = 65
    elif n == '66': rrr = 66
    elif n == '67': rrr = 67
    elif n == '68': rrr = 68
    elif n == '69': rrr = 69
    elif n == '70': rrr = 70
    elif n == '71': rrr = 71
    elif n == '72': rrr = 72
    elif n == '73': rrr = 73
    elif n == '74': rrr = 74
    elif n == '75': rrr = 75
    elif n == '76': rrr = 76
    elif n == '77': rrr = 77
    elif n == '78': rrr = 78
    elif n == '79': rrr = 79
    elif n == '80': rrr = 80
    elif n == '81': rrr = 81
    elif n == '82': rrr = 82
    elif n == '83': rrr = 83
    elif n == '84': rrr = 84
    elif n == '85': rrr = 85
    elif n == '86': rrr = 86
    elif n == '87': rrr = 87
    elif n == '88': rrr = 88
    elif n == '89': rrr = 89
    elif n == '90': rrr = 90
    elif n == '91': rrr = 91
    elif n == '92': rrr = 92
    elif n == '93': rrr = 93
    elif n == '94': rrr = 94
    elif n == '95': rrr = 95
    elif n == '96': rrr = 96
    elif n == '97': rrr = 97
    elif n == '98': rrr = 98
    elif n == '99': rrr = 99
    elif n == '100': rrr = 100
    elif n == '101': rrr = 101
    elif n == '102': rrr = 102
    elif n == '103': rrr = 103
    elif n == '104': rrr = 104
    elif n == '105': rrr = 105
    elif n == '106': rrr = 106
    elif n == '107': rrr = 107
    elif n == '108': rrr = 108
    elif n == '109': rrr = 109
    elif n == '110': rrr = 110
    elif n == '111': rrr = 111
    elif n == '112': rrr = 112
    elif n == '113': rrr = 113
    elif n == '114': rrr = 114
    elif n == '115': rrr = 115
    elif n == '116': rrr = 116
    elif n == '117': rrr = 117
    elif n == '118': rrr = 118
    elif n == '119': rrr = 119
    elif n == '120': rrr = 120
    elif n == '121': rrr = 121
    elif n == '122': rrr = 122
    elif n == '123': rrr = 123
    elif n == '124': rrr = 124
    elif n == '125': rrr = 125
    elif n == '126': rrr = 126
    elif n == '127': rrr = 127
    elif n == '128': rrr = 128
    elif n == '129': rrr = 129
    elif n == '130': rrr = 130
    elif n == '131': rrr = 131
    elif n == '132': rrr = 132
    elif n == '133': rrr = 133
    elif n == '134': rrr = 134
    elif n == '135': rrr = 135
    elif n == '136': rrr = 136
    elif n == '137': rrr = 137
    elif n == '138': rrr = 138
    elif n == '139': rrr = 139
    elif n == '140': rrr = 140
    elif n == '141': rrr = 141
    elif n == '142': rrr = 142
    elif n == '143': rrr = 143
    elif n == '144': rrr = 144
    elif n == '145': rrr = 145
    elif n == '146': rrr = 146
    elif n == '147': rrr = 147
    elif n == '148': rrr = 148
    elif n == '149': rrr = 149
    elif n == '150': rrr = 150
    elif n == '151': rrr = 151
    elif n == '152': rrr = 152
    elif n == '153': rrr = 153
    elif n == '154': rrr = 154
    elif n == '155': rrr = 155
    elif n == '156': rrr = 156
    elif n == '157': rrr = 157
    elif n == '158': rrr = 158
    elif n == '159': rrr = 159
    elif n == '160': rrr = 160
    elif n == '161': rrr = 161
    elif n == '162': rrr = 162
    elif n == '163': rrr = 163
    elif n == '164': rrr = 164
    elif n == '165': rrr = 165
    elif n == '166': rrr = 166
    elif n == '167': rrr = 167
    elif n == '168': rrr = 168
    elif n == '169': rrr = 169
    elif n == '170': rrr = 170
    elif n == '171': rrr = 171
    elif n == '172': rrr = 172
    elif n == '173': rrr = 173
    elif n == '174': rrr = 174
    elif n == '175': rrr = 175
    elif n == '176': rrr = 176
    elif n == '177': rrr = 177
    elif n == '178': rrr = 178
    elif n == '179': rrr = 179
    elif n == '180': rrr = 180
    elif n == '181': rrr = 181
    elif n == '182': rrr = 182
    elif n == '183': rrr = 183
    elif n == '184': rrr = 184
    elif n == '185': rrr = 185
    elif n == '186': rrr = 186
    elif n == '187': rrr = 187
    elif n == '188': rrr = 188
    elif n == '189': rrr = 189
    elif n == '190': rrr = 190
    elif n == '191': rrr = 191
    elif n == '192': rrr = 192
    elif n == '193': rrr = 193
    elif n == '194': rrr = 194
    elif n == '195': rrr = 195
    elif n == '196': rrr = 196
    elif n == '197': rrr = 197
    elif n == '198': rrr = 198
    elif n == '199': rrr = 199
    elif n == '200': rrr = 200
    elif n == '201': rrr = 201
    elif n == '202': rrr = 202
    elif n == '203': rrr = 203
    elif n == '204': rrr = 204
    elif n == '205': rrr = 205
    elif n == '206': rrr = 206
    elif n == '207': rrr = 207
    elif n == '208': rrr = 208
    elif n == '209': rrr = 209
    elif n == '210': rrr = 210
    elif n == '211': rrr = 211
    elif n == '212': rrr = 212
    elif n == '213': rrr = 213
    elif n == '214': rrr = 214
    elif n == '215': rrr = 215
    elif n == '216': rrr = 216
    elif n == '217': rrr = 217
    elif n == '218': rrr = 218
    elif n == '219': rrr = 219
    elif n == '220': rrr = 220
    elif n == '221': rrr = 221
    elif n == '222': rrr = 222
    elif n == '223': rrr = 223
    elif n == '224': rrr = 224
    elif n == '225': rrr = 225
    elif n == '226': rrr = 226
    elif n == '227': rrr = 227
    elif n == '228': rrr = 228
    elif n == '229': rrr = 229
    elif n == '230': rrr = 230
    elif n == '231': rrr = 231
    elif n == '232': rrr = 232
    elif n == '233': rrr = 233
    elif n == '234': rrr = 234
    elif n == '235': rrr = 235
    elif n == '236': rrr = 236
    elif n == '237': rrr = 237
    elif n == '238': rrr = 238
    elif n == '239': rrr = 239
    elif n == '240': rrr = 240
    elif n == '241': rrr = 241
    elif n == '242': rrr = 242
    elif n == '243': rrr = 243
    elif n == '244': rrr = 244
    elif n == '245': rrr = 245
    elif n == '246': rrr = 246
    elif n == '247': rrr = 247
    elif n == '248': rrr = 248
    elif n == '249': rrr = 249
    elif n == '250': rrr = 250
    elif n == '251': rrr = 251
    elif n == '252': rrr = 252
    elif n == '253': rrr = 253
    elif n == '254': rrr = 254
    elif n == '255': rrr = 255
    elif n == '256': rrr = 256
    elif n == '257': rrr = 257
    elif n == '258': rrr = 258
    elif n == '259': rrr = 259
    elif n == '260': rrr = 260
    elif n == '261': rrr = 261
    elif n == '262': rrr = 262
    elif n == '263': rrr = 263
    elif n == '264': rrr = 264
    elif n == '265': rrr = 265
    elif n == '266': rrr = 266
    elif n == '267': rrr = 267
    elif n == '268': rrr = 268
    elif n == '269': rrr = 269
    elif n == '270': rrr = 270
    elif n == '271': rrr = 271
    elif n == '272': rrr = 272
    elif n == '273': rrr = 273
    elif n == '274': rrr = 274
    elif n == '275': rrr = 275
    elif n == '276': rrr = 276
    elif n == '277': rrr = 277
    elif n == '278': rrr = 278
    elif n == '279': rrr = 279
    elif n == '280': rrr = 280
    elif n == '281': rrr = 281
    elif n == '282': rrr = 282
    elif n == '283': rrr = 283
    elif n == '284': rrr = 284
    elif n == '285': rrr = 285
    elif n == '286': rrr = 286
    elif n == '287': rrr = 287
    elif n == '288': rrr = 288
    elif n == '289': rrr = 289
    elif n == '290': rrr = 290
    elif n == '291': rrr = 291
    elif n == '292': rrr = 292
    elif n == '293': rrr = 293
    elif n == '294': rrr = 294
    elif n == '295': rrr = 295
    elif n == '296': rrr = 296
    elif n == '297': rrr = 297
    elif n == '298': rrr = 298
    elif n == '299': rrr = 299
    elif n == '300': rrr = 300
    elif n == '301': rrr = 301
    elif n == '302': rrr = 302
    elif n == '303': rrr = 303
    elif n == '304': rrr = 304
    elif n == '305': rrr = 305
    elif n == '306': rrr = 306
    elif n == '307': rrr = 307
    elif n == '308': rrr = 308
    elif n == '309': rrr = 309
    elif n == '310': rrr = 310
    elif n == '311': rrr = 311
    elif n == '312': rrr = 312
    elif n == '313': rrr = 313
    elif n == '314': rrr = 314
    elif n == '315': rrr = 315
    elif n == '316': rrr = 316
    elif n == '317': rrr = 317
    elif n == '318': rrr = 318
    elif n == '319': rrr = 319
    elif n == '320': rrr = 320
    elif n == '321': rrr = 321
    elif n == '322': rrr = 322
    elif n == '323': rrr = 323
    elif n == '324': rrr = 324
    elif n == '325': rrr = 325
    elif n == '326': rrr = 326
    elif n == '327': rrr = 327
    elif n == '328': rrr = 328
    elif n == '329': rrr = 329
    elif n == '330': rrr = 330
    elif n == '331': rrr = 331
    elif n == '332': rrr = 332
    elif n == '333': rrr = 333
    elif n == '334': rrr = 334
    elif n == '335': rrr = 335
    elif n == '336': rrr = 336
    elif n == '337': rrr = 337
    elif n == '338': rrr = 338
    elif n == '339': rrr = 339
    elif n == '340': rrr = 340
    elif n == '341': rrr = 341
    elif n == '342': rrr = 342
    elif n == '343': rrr = 343
    elif n == '344': rrr = 344
    elif n == '345': rrr = 345
    elif n == '346': rrr = 346
    elif n == '347': rrr = 347
    elif n == '348': rrr = 348
    elif n == '349': rrr = 349
    elif n == '350': rrr = 350
    elif n == '351': rrr = 351
    elif n == '352': rrr = 352
    elif n == '353': rrr = 353
    elif n == '354': rrr = 354
    elif n == '355': rrr = 355
    elif n == '356': rrr = 356
    elif n == '357': rrr = 357
    elif n == '358': rrr = 358
    elif n == '359': rrr = 359
    elif n == '360': rrr = 360
    elif n == '361': rrr = 361
    elif n == '362': rrr = 362
    elif n == '363': rrr = 363
    elif n == '364': rrr = 364
    elif n == '365': rrr = 365
    elif n == '366': rrr = 366
    elif n == '367': rrr = 367
    elif n == '368': rrr = 368
    elif n == '369': rrr = 369
    elif n == '370': rrr = 370
    elif n == '371': rrr = 371
    elif n == '372': rrr = 372
    elif n == '373': rrr = 373
    elif n == '374': rrr = 374
    elif n == '375': rrr = 375
    elif n == '376': rrr = 376
    elif n == '377': rrr = 377
    elif n == '378': rrr = 378
    elif n == '379': rrr = 379
    elif n == '380': rrr = 380
    elif n == '381': rrr = 381
    elif n == '382': rrr = 382
    elif n == '383': rrr = 383
    elif n == '384': rrr = 384
    elif n == '385': rrr = 385
    elif n == '386': rrr = 386
    elif n == '387': rrr = 387
    elif n == '388': rrr = 388
    elif n == '389': rrr = 389
    elif n == '390': rrr = 390
    elif n == '391': rrr = 391
    elif n == '392': rrr = 392
    elif n == '393': rrr = 393
    elif n == '394': rrr = 394
    elif n == '395': rrr = 395
    elif n == '396': rrr = 396
    elif n == '397': rrr = 397
    elif n == '398': rrr = 398
    elif n == '399': rrr = 399
    elif n == '400': rrr = 400
    elif n == '401': rrr = 401
    elif n == '402': rrr = 402
    elif n == '403': rrr = 403
    elif n == '404': rrr = 404
    elif n == '405': rrr = 405
    elif n == '406': rrr = 406
    elif n == '407': rrr = 407
    elif n == '408': rrr = 408
    elif n == '409': rrr = 409
    elif n == '410': rrr = 410
    elif n == '411': rrr = 411
    elif n == '412': rrr = 412
    elif n == '413': rrr = 413
    elif n == '414': rrr = 414
    elif n == '415': rrr = 415
    elif n == '416': rrr = 416
    elif n == '417': rrr = 417
    elif n == '418': rrr = 418
    elif n == '419': rrr = 419
    elif n == '420': rrr = 420
    elif n == '421': rrr = 421
    elif n == '422': rrr = 422
    elif n == '423': rrr = 423
    elif n == '424': rrr = 424
    elif n == '425': rrr = 425
    elif n == '426': rrr = 426
    elif n == '427': rrr = 427
    elif n == '428': rrr = 428
    elif n == '429': rrr = 429
    elif n == '430': rrr = 430
    elif n == '431': rrr = 431
    elif n == '432': rrr = 432
    elif n == '433': rrr = 433
    elif n == '434': rrr = 434
    elif n == '435': rrr = 435
    elif n == '436': rrr = 436
    elif n == '437': rrr = 437
    elif n == '438': rrr = 438
    elif n == '439': rrr = 439
    elif n == '440': rrr = 440
    elif n == '441': rrr = 441
    elif n == '442': rrr = 442
    elif n == '443': rrr = 443
    elif n == '444': rrr = 444
    elif n == '445': rrr = 445
    elif n == '446': rrr = 446
    elif n == '447': rrr = 447
    elif n == '448': rrr = 448
    elif n == '449': rrr = 449
    elif n == '450': rrr = 450
    elif n == '451': rrr = 451
    elif n == '452': rrr = 452
    elif n == '453': rrr = 453
    elif n == '454': rrr = 454
    elif n == '455': rrr = 455
    elif n == '456': rrr = 456
    elif n == '457': rrr = 457
    elif n == '458': rrr = 458
    elif n == '459': rrr = 459
    elif n == '460': rrr = 460
    elif n == '461': rrr = 461
    elif n == '462': rrr = 462
    elif n == '463': rrr = 463
    elif n == '464': rrr = 464
    elif n == '465': rrr = 465
    elif n == '466': rrr = 466
    elif n == '467': rrr = 467
    elif n == '468': rrr = 468
    elif n == '469': rrr = 469
    elif n == '470': rrr = 470
    elif n == '471': rrr = 471
    elif n == '472': rrr = 472
    elif n == '473': rrr = 473
    elif n == '474': rrr = 474
    elif n == '475': rrr = 475
    elif n == '476': rrr = 476
    elif n == '477': rrr = 477
    elif n == '478': rrr = 478
    elif n == '479': rrr = 479
    elif n == '480': rrr = 480
    elif n == '481': rrr = 481
    elif n == '482': rrr = 482
    elif n == '483': rrr = 483
    elif n == '484': rrr = 484
    elif n == '485': rrr = 485
    elif n == '486': rrr = 486
    elif n == '487': rrr = 487
    elif n == '488': rrr = 488
    elif n == '489': rrr = 489
    elif n == '490': rrr = 490
    elif n == '491': rrr = 491
    elif n == '492': rrr = 492
    elif n == '493': rrr = 493
    elif n == '494': rrr = 494
    elif n == '495': rrr = 495
    elif n == '496': rrr = 496
    elif n == '497': rrr = 497
    elif n == '498': rrr = 498
    elif n == '499': rrr = 499
    elif n == '500': rrr = 500
    elif n == '501': rrr = 501
    elif n == '502': rrr = 502
    elif n == '503': rrr = 503
    elif n == '504': rrr = 504
    elif n == '505': rrr = 505
    elif n == '506': rrr = 506
    elif n == '507': rrr = 507
    elif n == '508': rrr = 508
    elif n == '509': rrr = 509
    elif n == '510': rrr = 510
    elif n == '511': rrr = 511
    elif n == '512': rrr = 512
    elif n == '513': rrr = 513
    elif n == '514': rrr = 514
    elif n == '515': rrr = 515
    elif n == '516': rrr = 516
    elif n == '517': rrr = 517
    elif n == '518': rrr = 518
    elif n == '519': rrr = 519
    elif n == '520': rrr = 520
    elif n == '521': rrr = 521
    elif n == '522': rrr = 522
    elif n == '523': rrr = 523
    elif n == '524': rrr = 524
    elif n == '525': rrr = 525
    elif n == '526': rrr = 526
    elif n == '527': rrr = 527
    elif n == '528': rrr = 528
    elif n == '529': rrr = 529
    elif n == '530': rrr = 530
    elif n == '531': rrr = 531
    elif n == '532': rrr = 532
    elif n == '533': rrr = 533
    elif n == '534': rrr = 534
    elif n == '535': rrr = 535
    elif n == '536': rrr = 536
    elif n == '537': rrr = 537
    elif n == '538': rrr = 538
    elif n == '539': rrr = 539
    elif n == '540': rrr = 540
    elif n == '541': rrr = 541
    elif n == '542': rrr = 542
    elif n == '543': rrr = 543
    elif n == '544': rrr = 544
    elif n == '545': rrr = 545
    elif n == '546': rrr = 546
    elif n == '547': rrr = 547
    elif n == '548': rrr = 548
    elif n == '549': rrr = 549
    elif n == '550': rrr = 550
    elif n == '551': rrr = 551
    elif n == '552': rrr = 552
    elif n == '553': rrr = 553
    elif n == '554': rrr = 554
    elif n == '555': rrr = 555
    elif n == '556': rrr = 556
    elif n == '557': rrr = 557
    elif n == '558': rrr = 558
    elif n == '559': rrr = 559
    elif n == '560': rrr = 560
    elif n == '561': rrr = 561
    elif n == '562': rrr = 562
    elif n == '563': rrr = 563
    elif n == '564': rrr = 564
    elif n == '565': rrr = 565
    elif n == '566': rrr = 566
    elif n == '567': rrr = 567
    elif n == '568': rrr = 568
    elif n == '569': rrr = 569
    elif n == '570': rrr = 570
    elif n == '571': rrr = 571
    elif n == '572': rrr = 572
    elif n == '573': rrr = 573
    elif n == '574': rrr = 574
    elif n == '575': rrr = 575
    elif n == '576': rrr = 576
    elif n == '577': rrr = 577
    elif n == '578': rrr = 578
    elif n == '579': rrr = 579
    elif n == '580': rrr = 580
    elif n == '581': rrr = 581
    elif n == '582': rrr = 582
    elif n == '583': rrr = 583
    elif n == '584': rrr = 584
    elif n == '585': rrr = 585
    elif n == '586': rrr = 586
    elif n == '587': rrr = 587
    elif n == '588': rrr = 588
    elif n == '589': rrr = 589
    elif n == '590': rrr = 590
    elif n == '591': rrr = 591
    elif n == '592': rrr = 592
    elif n == '593': rrr = 593
    elif n == '594': rrr = 594
    elif n == '595': rrr = 595
    elif n == '596': rrr = 596
    elif n == '597': rrr = 597
    elif n == '598': rrr = 598
    elif n == '599': rrr = 599
    elif n == '600': rrr = 600
    elif n == '601': rrr = 601
    elif n == '602': rrr = 602
    elif n == '603': rrr = 603
    elif n == '604': rrr = 604
    elif n == '605': rrr = 605
    elif n == '606': rrr = 606
    elif n == '607': rrr = 607
    elif n == '608': rrr = 608
    elif n == '609': rrr = 609
    elif n == '610': rrr = 610
    elif n == '611': rrr = 611
    elif n == '612': rrr = 612
    elif n == '613': rrr = 613
    elif n == '614': rrr = 614
    elif n == '615': rrr = 615
    elif n == '616': rrr = 616
    elif n == '617': rrr = 617
    elif n == '618': rrr = 618
    elif n == '619': rrr = 619
    elif n == '620': rrr = 620
    elif n == '621': rrr = 621
    elif n == '622': rrr = 622
    elif n == '623': rrr = 623
    elif n == '624': rrr = 624
    elif n == '625': rrr = 625
    elif n == '626': rrr = 626
    elif n == '627': rrr = 627
    elif n == '628': rrr = 628
    elif n == '629': rrr = 629
    elif n == '630': rrr = 630
    elif n == '631': rrr = 631
    elif n == '632': rrr = 632
    elif n == '633': rrr = 633
    elif n == '634': rrr = 634
    elif n == '635': rrr = 635
    elif n == '636': rrr = 636
    elif n == '637': rrr = 637
    elif n == '638': rrr = 638
    elif n == '639': rrr = 639
    elif n == '640': rrr = 640
    elif n == '641': rrr = 641
    elif n == '642': rrr = 642
    elif n == '643': rrr = 643
    elif n == '644': rrr = 644
    elif n == '645': rrr = 645
    elif n == '646': rrr = 646
    elif n == '647': rrr = 647
    elif n == '648': rrr = 648
    elif n == '649': rrr = 649
    elif n == '650': rrr = 650
    elif n == '651': rrr = 651
    elif n == '652': rrr = 652
    elif n == '653': rrr = 653
    elif n == '654': rrr = 654
    elif n == '655': rrr = 655
    elif n == '656': rrr = 656
    elif n == '657': rrr = 657
    elif n == '658': rrr = 658
    elif n == '659': rrr = 659
    elif n == '660': rrr = 660
    elif n == '661': rrr = 661
    elif n == '662': rrr = 662
    elif n == '663': rrr = 663
    elif n == '664': rrr = 664
    elif n == '665': rrr = 665
    elif n == '666': rrr = 666
    elif n == '667': rrr = 667
    elif n == '668': rrr = 668
    elif n == '669': rrr = 669
    elif n == '670': rrr = 670
    elif n == '671': rrr = 671
    elif n == '672': rrr = 672
    elif n == '673': rrr = 673
    elif n == '674': rrr = 674
    elif n == '675': rrr = 675
    elif n == '676': rrr = 676
    elif n == '677': rrr = 677
    elif n == '678': rrr = 678
    elif n == '679': rrr = 679
    elif n == '680': rrr = 680
    elif n == '681': rrr = 681
    elif n == '682': rrr = 682
    elif n == '683': rrr = 683
    elif n == '684': rrr = 684
    elif n == '685': rrr = 685
    elif n == '686': rrr = 686
    elif n == '687': rrr = 687
    elif n == '688': rrr = 688
    elif n == '689': rrr = 689
    elif n == '690': rrr = 690
    elif n == '691': rrr = 691
    elif n == '692': rrr = 692
    elif n == '693': rrr = 693
    elif n == '694': rrr = 694
    elif n == '695': rrr = 695
    elif n == '696': rrr = 696
    elif n == '697': rrr = 697
    elif n == '698': rrr = 698
    elif n == '699': rrr = 699
    elif n == '700': rrr = 700
    elif n == '701': rrr = 701
    elif n == '702': rrr = 702
    elif n == '703': rrr = 703
    elif n == '704': rrr = 704
    elif n == '705': rrr = 705
    elif n == '706': rrr = 706
    elif n == '707': rrr = 707
    elif n == '708': rrr = 708
    elif n == '709': rrr = 709
    elif n == '710': rrr = 710
    elif n == '711': rrr = 711
    elif n == '712': rrr = 712
    elif n == '713': rrr = 713
    elif n == '714': rrr = 714
    elif n == '715': rrr = 715
    elif n == '716': rrr = 716
    elif n == '717': rrr = 717
    elif n == '718': rrr = 718
    elif n == '719': rrr = 719
    elif n == '720': rrr = 720
    elif n == '721': rrr = 721
    elif n == '722': rrr = 722
    elif n == '723': rrr = 723
    elif n == '724': rrr = 724
    elif n == '725': rrr = 725
    elif n == '726': rrr = 726
    elif n == '727': rrr = 727
    elif n == '728': rrr = 728
    elif n == '729': rrr = 729
    elif n == '730': rrr = 730
    elif n == '731': rrr = 731
    elif n == '732': rrr = 732
    elif n == '733': rrr = 733
    elif n == '734': rrr = 734
    elif n == '735': rrr = 735
    elif n == '736': rrr = 736
    elif n == '737': rrr = 737
    elif n == '738': rrr = 738
    elif n == '739': rrr = 739
    elif n == '740': rrr = 740
    elif n == '741': rrr = 741
    elif n == '742': rrr = 742
    elif n == '743': rrr = 743
    elif n == '744': rrr = 744
    elif n == '745': rrr = 745
    elif n == '746': rrr = 746
    elif n == '747': rrr = 747
    elif n == '748': rrr = 748
    elif n == '749': rrr = 749
    elif n == '750': rrr = 750
    elif n == '751': rrr = 751
    elif n == '752': rrr = 752
    elif n == '753': rrr = 753
    elif n == '754': rrr = 754
    elif n == '755': rrr = 755
    elif n == '756': rrr = 756
    elif n == '757': rrr = 757
    elif n == '758': rrr = 758
    elif n == '759': rrr = 759
    elif n == '760': rrr = 760
    elif n == '761': rrr = 761
    elif n == '762': rrr = 762
    elif n == '763': rrr = 763
    elif n == '764': rrr = 764
    elif n == '765': rrr = 765
    elif n == '766': rrr = 766
    elif n == '767': rrr = 767
    elif n == '768': rrr = 768
    elif n == '769': rrr = 769
    elif n == '770': rrr = 770
    elif n == '771': rrr = 771
    elif n == '772': rrr = 772
    elif n == '773': rrr = 773
    elif n == '774': rrr = 774
    elif n == '775': rrr = 775
    elif n == '776': rrr = 776
    elif n == '777': rrr = 777
    elif n == '778': rrr = 778
    elif n == '779': rrr = 779
    elif n == '780': rrr = 780
    elif n == '781': rrr = 781
    elif n == '782': rrr = 782
    elif n == '783': rrr = 783
    elif n == '784': rrr = 784
    elif n == '785': rrr = 785
    elif n == '786': rrr = 786
    elif n == '787': rrr = 787
    elif n == '788': rrr = 788
    elif n == '789': rrr = 789
    elif n == '790': rrr = 790
    elif n == '791': rrr = 791
    elif n == '792': rrr = 792
    elif n == '793': rrr = 793
    elif n == '794': rrr = 794
    elif n == '795': rrr = 795
    elif n == '796': rrr = 796
    elif n == '797': rrr = 797
    elif n == '798': rrr = 798
    elif n == '799': rrr = 799
    elif n == '800': rrr = 800
    elif n == '801': rrr = 801
    elif n == '802': rrr = 802
    elif n == '803': rrr = 803
    elif n == '804': rrr = 804
    elif n == '805': rrr = 805
    elif n == '806': rrr = 806
    elif n == '807': rrr = 807
    elif n == '808': rrr = 808
    elif n == '809': rrr = 809
    elif n == '810': rrr = 810
    elif n == '811': rrr = 811
    elif n == '812': rrr = 812
    elif n == '813': rrr = 813
    elif n == '814': rrr = 814
    elif n == '815': rrr = 815
    elif n == '816': rrr = 816
    elif n == '817': rrr = 817
    elif n == '818': rrr = 818
    elif n == '819': rrr = 819
    elif n == '820': rrr = 820
    elif n == '821': rrr = 821
    elif n == '822': rrr = 822
    elif n == '823': rrr = 823
    elif n == '824': rrr = 824
    elif n == '825': rrr = 825
    elif n == '826': rrr = 826
    elif n == '827': rrr = 827
    elif n == '828': rrr = 828
    elif n == '829': rrr = 829
    elif n == '830': rrr = 830
    elif n == '831': rrr = 831
    elif n == '832': rrr = 832
    elif n == '833': rrr = 833
    elif n == '834': rrr = 834
    elif n == '835': rrr = 835
    elif n == '836': rrr = 836
    elif n == '837': rrr = 837
    elif n == '838': rrr = 838
    elif n == '839': rrr = 839
    elif n == '840': rrr = 840
    elif n == '841': rrr = 841
    elif n == '842': rrr = 842
    elif n == '843': rrr = 843
    elif n == '844': rrr = 844
    elif n == '845': rrr = 845
    elif n == '846': rrr = 846
    elif n == '847': rrr = 847
    elif n == '848': rrr = 848
    elif n == '849': rrr = 849
    elif n == '850': rrr = 850
    elif n == '851': rrr = 851
    elif n == '852': rrr = 852
    elif n == '853': rrr = 853
    elif n == '854': rrr = 854
    elif n == '855': rrr = 855
    elif n == '856': rrr = 856
    elif n == '857': rrr = 857
    elif n == '858': rrr = 858
    elif n == '859': rrr = 859
    elif n == '860': rrr = 860
    elif n == '861': rrr = 861
    elif n == '862': rrr = 862
    elif n == '863': rrr = 863
    elif n == '864': rrr = 864
    elif n == '865': rrr = 865
    elif n == '866': rrr = 866
    elif n == '867': rrr = 867
    elif n == '868': rrr = 868
    elif n == '869': rrr = 869
    elif n == '870': rrr = 870
    elif n == '871': rrr = 871
    elif n == '872': rrr = 872
    elif n == '873': rrr = 873
    elif n == '874': rrr = 874
    elif n == '875': rrr = 875
    elif n == '876': rrr = 876
    elif n == '877': rrr = 877
    elif n == '878': rrr = 878
    elif n == '879': rrr = 879
    elif n == '880': rrr = 880
    elif n == '881': rrr = 881
    elif n == '882': rrr = 882
    elif n == '883': rrr = 883
    elif n == '884': rrr = 884
    elif n == '885': rrr = 885
    elif n == '886': rrr = 886
    elif n == '887': rrr = 887
    elif n == '888': rrr = 888
    elif n == '889': rrr = 889
    elif n == '890': rrr = 890
    elif n == '891': rrr = 891
    elif n == '892': rrr = 892
    elif n == '893': rrr = 893
    elif n == '894': rrr = 894
    elif n == '895': rrr = 895
    elif n == '896': rrr = 896
    elif n == '897': rrr = 897
    elif n == '898': rrr = 898
    elif n == '899': rrr = 899
    elif n == '900': rrr = 900
    elif n == '901': rrr = 901
    elif n == '902': rrr = 902
    elif n == '903': rrr = 903
    elif n == '904': rrr = 904
    elif n == '905': rrr = 905
    elif n == '906': rrr = 906
    elif n == '907': rrr = 907
    elif n == '908': rrr = 908
    elif n == '909': rrr = 909
    elif n == '910': rrr = 910
    elif n == '911': rrr = 911
    elif n == '912': rrr = 912
    elif n == '913': rrr = 913
    elif n == '914': rrr = 914
    elif n == '915': rrr = 915
    elif n == '916': rrr = 916
    elif n == '917': rrr = 917
    elif n == '918': rrr = 918
    elif n == '919': rrr = 919
    elif n == '920': rrr = 920
    elif n == '921': rrr = 921
    elif n == '922': rrr = 922
    elif n == '923': rrr = 923
    elif n == '924': rrr = 924
    elif n == '925': rrr = 925
    elif n == '926': rrr = 926
    elif n == '927': rrr = 927
    elif n == '928': rrr = 928
    elif n == '929': rrr = 929
    elif n == '930': rrr = 930
    elif n == '931': rrr = 931
    elif n == '932': rrr = 932
    elif n == '933': rrr = 933
    elif n == '934': rrr = 934
    elif n == '935': rrr = 935
    elif n == '936': rrr = 936
    elif n == '937': rrr = 937
    elif n == '938': rrr = 938
    elif n == '939': rrr = 939
    elif n == '940': rrr = 940
    elif n == '941': rrr = 941
    elif n == '942': rrr = 942
    elif n == '943': rrr = 943
    elif n == '944': rrr = 944
    elif n == '945': rrr = 945
    elif n == '946': rrr = 946
    elif n == '947': rrr = 947
    elif n == '948': rrr = 948
    elif n == '949': rrr = 949
    elif n == '950': rrr = 950
    elif n == '951': rrr = 951
    elif n == '952': rrr = 952
    elif n == '953': rrr = 953
    elif n == '954': rrr = 954
    elif n == '955': rrr = 955
    elif n == '956': rrr = 956
    elif n == '957': rrr = 957
    elif n == '958': rrr = 958
    elif n == '959': rrr = 959
    elif n == '960': rrr = 960
    elif n == '961': rrr = 961
    elif n == '962': rrr = 962
    elif n == '963': rrr = 963
    elif n == '964': rrr = 964
    elif n == '965': rrr = 965
    elif n == '966': rrr = 966
    elif n == '967': rrr = 967
    elif n == '968': rrr = 968
    elif n == '969': rrr = 969
    elif n == '970': rrr = 970
    elif n == '971': rrr = 971
    elif n == '972': rrr = 972
    elif n == '973': rrr = 973
    elif n == '974': rrr = 974
    elif n == '975': rrr = 975
    elif n == '976': rrr = 976
    elif n == '977': rrr = 977
    elif n == '978': rrr = 978
    elif n == '979': rrr = 979
    elif n == '980': rrr = 980
    elif n == '981': rrr = 981
    elif n == '982': rrr = 982
    elif n == '983': rrr = 983
    elif n == '984': rrr = 984
    elif n == '985': rrr = 985
    elif n == '986': rrr = 986
    elif n == '987': rrr = 987
    elif n == '988': rrr = 988
    elif n == '989': rrr = 989 #dari hasil diskusi diisi 999
    elif n == '990': rrr = 8888 #dari hasil diskusi diisi 8888
    elif n == '991': rrr = 0.1
    elif n == '992': rrr = 0.2
    elif n == '993': rrr = 0.3
    elif n == '994': rrr = 0.4
    elif n == '995': rrr = 0.5
    elif n == '996': rrr = 0.6
    elif n == '997': rrr = 0.7
    elif n == '998': rrr = 0.8
    elif n == '999': rrr = 0.9 
    else: rrr = 9999
    return(rrr)


    # NoSta	
    # Station	
    # YY	
    # MM	
    # DD	
    # HH	
    # TdTdTd	
    # N	
    # dd	
    # ff	
    # VV	
    # ww	
    # W1	
    # W2	
    # QFF	
    # TtTtTt	
    # Nh	
    # CL	
    # h	
    # CM	
    # CH	
    # Ns_1 
    # C_1	
    # Hshs_1	
    # Ns_2	
    # C_2	
    # Hshs_2	
    # Ns_3	
    # C_3	
    # Hshs_3	
    # e	
    # UU	
    # QFE	
    # TwTwTw	
    # RRR	
    # tR	
    # TxTxTx	
    # TnTnTn	
    # EEE	
    # F24F24F24F24	
    # SSS	
    # E	
    # DL	
    # DM	
    # DH	
    # appp	
    # P24P24P24	
    # iW	
    # iX	
    # iR	
    # iE

if __name__ == '__main__':
    main()
