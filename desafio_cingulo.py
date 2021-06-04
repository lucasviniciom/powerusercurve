import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


print('ok')

with open(r'C:\Users\lucas\Documents\Python\Cingulo\user_activities.json') as json_file:
    data = json.load(json_file)

df = pd.read_json (r'C:\Users\lucas\Documents\Python\Cingulo\user_activities.json')
print(df)
#365 valores/dias equivale a ano não bissexto
dias_mes = [31,28,31,30,31,30,31,31,30,31,30,31]
#Lista cumulativa para dia final de cada mes. Como o indice é n-1, funciona 
#[ 31  59  90 120 151 181 212 243 273 304 334 365]
dia_inic_mes = np.cumsum(dias_mes)

##Verificar se todos os valores sao 0 ou 1
##Verificar se os 40 usuarios tem 365 valores
for x in range(len(df)):
    a = np.array(df['activities'][x])
    if not ((a==0) | (a==1)).all():
      print("Existem valores diferentes de 0 ou 1")
    if len(df['activities'][x])!=365:
      print("Faltam valores")

## Criar colunas para cada mes e quantas vezes o cliente usou o app
nomes_mes = ['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez']
for x in nomes_mes:
    df[x] = np.nan


def freq_mensal(idx, mes): 
    a=0
    contagem = 0
    if idx>0:
        a = dia_inic_mes[idx-1]
    for user in range(40): 
        #Contagem e atribuição de um mes para um usuario
        for x in range(a, (a+dias_mes[idx])):
            contagem += (df['activities'][user][x])

        df.loc[user, mes] = contagem
        contagem = 0
   

for idx, mes in enumerate(nomes_mes):
    freq_mensal(idx, mes)
    
#Exporta arquivo para .csv 
#Para utilizar, substitua o caminho para onder será exportado o csv
#df.to_csv(r'C:\Users\lucas\Documents\Python\Cingulo\Pwr_Curve.csv', index = False)
#print('ok')

def rel_freq(x):
    freqs = [(value, x.count(value) / len(x)) for value in set(x)] 
    return freqs
 

#Modifica tamanho dos plots para melhor visualização neste notebook
plt.rcParams['figure.figsize'] = [12, 4]
#Gera os gráficos para os meses de fev, mar e abr. Para outros meses, apesas modificar pelo acronimo do mês.
for mes in ['fev','mar','abr']:
  pwr_user_curve = rel_freq(df[mes].tolist())
  xs = [x for x, y in pwr_user_curve]
  ys = [y*100 for x, y in pwr_user_curve]
#Diversas configurações para melhorar o estilo
  fig, ax = plt.subplots()
  barplot = ax.bar(
      x=xs,
      height=ys,
  )
#O numero de dias apresentados não muda a analise. 
#Obtou-se por manter todos os meses com 31 para comparação direta entre os meses. Poderia ser configurado para corresponder ao mes.
  ax.set_xlim(0,31)
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)
  ax.spines['left'].set_visible(False)
  ax.tick_params(bottom=False, left=False)
  ax.set_axisbelow(True)
  ax.yaxis.grid(True, color='#EEEEEE')
  ax.xaxis.grid(False)
  ax.set_xticks(range(32))

  bar_color = barplot[0].get_facecolor()
  #Labels nas barras
  for bar in barplot:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.001,
        round(bar.get_height(), 1),
        horizontalalignment='center',
        color=bar_color,
        size=8
    )
  #Labels dos eixos e titulo
  ax.set_xlabel('Total de dias ativos no mês', labelpad=15, color='#333333')
  ax.set_ylabel('Usuarios por dias de atividade no mês (%)', labelpad=15, color='#333333')
  ax.set_title(f'Power User Curve ({mes})', pad=15, color='#333333',
              weight='bold')
  
  fig.tight_layout()
  plt.show()
##
