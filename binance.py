import numpy as np
import matplotlib.pyplot as plt
import os
import csv
import pandas as pd 
import datetime
#features estarán ordenados por: mercancia, ventas, capital, gastos
features = {'mercancia':['arr_date','item', 'ssid', 'group', 'weight', 'cost','shipping_cost', 'price'],  
             'ventas':['sell_date','item', 'ssid', 'group', 'weight', 'total_cost', 'final_price', 'channel', 'buyer','days_sell', 'profit'],
             'capital':['date','wallet', 'bancolombia', 'eprep', 'nequi', 'daviplata', 'btc', 'box', 'income','about'],
             'gastos':['date','global_group','group', 'details', 'amount', 'account']}

#global group puede ser: 1. obligación 2. gusto 3. ajuste_{cuenta}
#group puede ser: 1. mercado 2. rapitienda 3. varios 4. admon 5. recibos 6. eps 7. eps_comp 8. eps_prep
#                 9. comida 10. otro 11. (wallet, bancolombia, ...) 12. tc



# mercancia = open('data/mercancia.csv', 'w')
# ventas    = open('data/ventas.csv', 'w')
# capital   = open('data/capital.csv', 'w')
# gastos    = open('data/gastos.csv', 'w')

files = ['mercancia', 'ventas', 'capital', 'gastos']

class Month():
    def __init__(self,month):
        self.month = month
        self.path = month+'/'

    def maker(self):
        #este atributo crea la carpeta y archivos para el mes si aún no existe
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        for i in range(0,len(files)):
            name = files[i] #la mercancía se agrega de manera manual, ya que se traslada de mes a mes
            if not os.path.exists(self.path+name+'_'+self.month+'.csv'):
                os.mknod(self.path+name+'_'+self.month+'.csv') #crea el archivo
                df = pd.DataFrame(data=None, columns=features[name])
                # df.set_index(features[name][0], inplace=True)
                df.to_csv(self.path+name+'_'+self.month+'.csv', index=False)

    def add(self, name, value):
        ##me doy cuenta que esta aunque puede usarse en cualquier lista, de manera práctica solo será útil para gastos y mercancía
        ##name es la lista a donde se va a agregar, ,mercancia, gastos, etc
        ##value sería una lista con los datos de cada uno
        tmp_df = pd.DataFrame(data=[value], columns=features[name])
        # if (name == 'mercancia') or (name == 'ventas'):
        #     tmp_df = tmp_df.astype({'ssid': int})
        # tmp_df.set_index(features[name][0], inplace=True)
        tmp_df.to_csv(self.path+name+'_'+self.month+'.csv', mode='a', header=False, index=False)

    def venta(self, ssid, venta_list):
        #venta_list es una lista con sell_date, final_price, channel, buyer
        tmp_df_mer = pd.read_csv(self.path+'mercancia'+'_'+self.month+'.csv')
        tmp_df_mer['arr_date'] = pd.to_datetime(tmp_df_mer['arr_date'])
        # tmp_df_ven = pd.read_csv(self.path+'ventas'+'_'+self.month+'.csv') ###a descartar

        indx = tmp_df_mer[tmp_df_mer['ssid']==ssid].index

        total_cost = tmp_df_mer.loc[indx, 'cost'] + tmp_df_mer.loc[indx, 'shipping_cost']
        profit = venta_list[1] - total_cost

        # fecha_llegada = [int(i) for i in tmp_df_mer.loc[indx, 'arr_date'].item().split('-')]
       
    

        days_sell = pd.to_datetime(venta_list[0])-tmp_df_mer.loc[indx, 'arr_date']


        #eliminar de mercancia y agregara  ventas

        
        tmp_df_ven = pd.DataFrame(data=[[venta_list[0], tmp_df_mer.loc[indx, 'item'].item(),
        tmp_df_mer.loc[indx, 'ssid'].item(),tmp_df_mer.loc[indx, 'group'].item(), tmp_df_mer.loc[indx, 'weight'].item(),
        total_cost.item(), venta_list[1], venta_list[2], venta_list[3], days_sell.item().days, profit.item()]])
        tmp_df_mer.drop(indx, inplace=True)
        #almacenando 

        tmp_df_mer.to_csv(self.path+'mercancia'+'_'+self.month+'.csv', index=False)
        tmp_df_ven.to_csv(self.path+'ventas'+'_'+self.month+'.csv', mode='a', header=False, index=False)

    def ingreso(self, ingre_list):
        #En ingre_list irán [date, account, value, about]
        tmp_df_cap = pd.read_csv(self.path+'capital'+'_'+self.month+'.csv')
        ajuste = ingre_list[2] + tmp_df_cap[ingre_list[1]].iloc[-1]
        data_ajustada = tmp_df_cap.iloc[-1]
        data_ajustada[ingre_list[1]] = ajuste
   
        data_ajustada['date'] = ingre_list[0]
        
        data_ajustada['income'] = ingre_list[2]
        
        data_ajustada['about'] = ingre_list[3]
        data_list = data_ajustada.tolist()
  
        data_ajustada_fm = pd.DataFrame(data=[data_list], columns=tmp_df_cap.columns)        # #agregar al csv al final
        # print(tmp_df_cap.columns)
        data_ajustada_fm.to_csv(self.path+'capital'+'_'+self.month+'.csv', mode='a', header=False, index=False)

    def egreso(self, egreso_list):
        #en egreso_list irá ['date','global_group','group', 'details', 'amount', 'account']
        tmp_df_eg = pd.DataFrame(data=[egreso_list])

        #restar al capital de la cuenta 
        tmp_df_cap = pd.read_csv(self.path+'capital'+'_'+self.month+'.csv')
        tmp_df_cap_s = tmp_df_cap.iloc[-1]
        tmp_df_cap_s[egreso_list[5]] = tmp_df_cap_s[egreso_list[5]]-egreso_list[4]
        tmp_df_cap_s['date'] = egreso_list[0]
        tmp_df_cap_s['income'] = -egreso_list[4]

        cap_list = tmp_df_cap_s.tolist()

        cap_fm = pd.DataFrame(data=[cap_list], columns=tmp_df_cap.columns)

        #guardar en los csv
        tmp_df_eg.to_csv(self.path+'gastos'+'_'+self.month+'.csv', mode='a', header=False, index=False)
        cap_fm.to_csv(self.path+'capital'+'_'+self.month+'.csv', mode='a', header=False, index=False)
       

Mayo = Month('mayo')

##prueba

##creemos los archivos de mayo
Mayo.maker()

##agreguemos capital inicial
Mayo.add('capital', [datetime.date(2020,5,22), 250000, 3000, 7000, 500000, 0 ,0.002397, 400000, 0, 'inicial']) #FUNCIONA PERFECTO

Mayo.add('mercancia', [datetime.date(2020,5,21), 'MM710', '11194902776', 'mouse', 0.5, 164000, 7500, 220000])

Mayo.add('mercancia', [datetime.date(2020,5,21), 'All New Kindle (blanco)', 'g090wf050085002f', 'ereader', 1, 264000, 15000, 380000])
Mayo.add('mercancia', [datetime.date(2020,5,21), 'All New Kindle (blanco)', 'g090wf05008501ev', 'ereader', 1, 264000, 15000, 380000])
Mayo.add('mercancia', [datetime.date(2020,5,21), 'All New Kindle (negro)', 'g090vb05950202uo', 'ereader', 1, 264000, 15000, 380000])
Mayo.add('mercancia', [datetime.date(2020,5,21), 'All New Kindle (negro)', 'g090vb05950202t2', 'ereader', 1, 264000, 15000, 380000])

# Mayo.venta('g090vb05950202t2', [datetime.date(2020,5,22), 370000, 'mp', 'pepito'])

# Mayo.ingreso([datetime.date(2020,5,25), 'bancolombia', 50000, 'prueba2'])

# Mayo.egreso([datetime.date(2020,5,28), 'obligación', 'recibos', 'emcali', 240000, 'nequi'])