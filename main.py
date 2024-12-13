import pandas as pd #para ler os dados do csv
import numpy as np #para realizar operacoes matematicas
import matplotlib.pyplot as plt #para fazer o plot dos graficos
import seaborn as sns #para fazer a funcao de distribuicao empirica
import statsmodels.api as sm #para fazer o QQ plot


# primeiro, devemos fazer um reescalonamento dos dados aplicando log10 nos bps e dps
# para cada um das etapas faremos uma função que calcula e salva os dados na pasta "resultados/Bloco-x" onde x é o bloco equivalente
def bloco_1_reescalonar_dados():
    # lemos os dataframes
    path_chrome = 'Estatística e Mod. Probabilist - COE241/data/dataset_chromecast.csv'
    path_smart_tv = 'Estatística e Mod. Probabilist - COE241/data/dataset_smart-tv.csv'
    
    dataframe_chromecast = pd.read_csv(filepath_or_buffer=path_chrome)
    dataframe_smart_tv = pd.read_csv(filepath_or_buffer = path_smart_tv)

    # aplicamos log 10 nas colunas "bytes_up" e "bytes_down"
    # iteramos pelo dataframe para evitar o caso de aplicarmos log10 em todos os elementos e ter algum elemento que seja 0 
    for col in ['bytes_up', 'bytes_down']:
        dataframe_chromecast[col] = dataframe_chromecast[col].apply(lambda x: np.log10(x) if x > 0 else 0)
        dataframe_smart_tv[col] = dataframe_smart_tv[col].apply(lambda x: np.log10(x) if x > 0 else 0)   
    
    return(dataframe_chromecast,dataframe_smart_tv)

# agora faremos cada uma das funções para o bloco 2 de estatisticas gerais

def histograma_bloco_2(df, name):
    # criamos uma figure para a parte do bytes up e outra para a parte do bytes down
    fig_bytes_up = plt.figure()
    fig_bytes_down = plt.figure()

    # em cada figure definimos um ax
    ax_bytes_up = fig_bytes_up.add_subplot(1,1,1)
    ax_bytes_down = fig_bytes_down.add_subplot(1,1,1)

    #usando o metodo de sturges, definimos a quantidade de bins
    bins = np.round(1 + 3.322*(np.log10(len(df))))

    ax_bytes_up.hist(df['bytes_up'], bins=int(bins),edgecolor ="darkblue")
    ax_bytes_up.set_xlabel(f'Histograma de bytes_up do {name}')
    
    ax_bytes_down.hist(df['bytes_down'], bins=int(bins),edgecolor ="darkblue")
    ax_bytes_down.set_xlabel(f'Histograma de bytes_down do {name}')

    path = f'Estatística e Mod. Probabilist - COE241/resultados/bloco2/{name}'
    # geramos 2 imagens para cada plot, 1 com fundo transparente e outra com fundo branco
    fig_bytes_up.savefig(f'{path}_histograma_bytes_up_transparente.png', format='png', transparent=True)
    fig_bytes_down.savefig(f'{path}_histograma_bytes_down_transparente.png', format='png', transparent=True)
    fig_bytes_up.savefig(f'{path}_histograma_bytes_up_fundo_branco.png', format='png', transparent=False)
    fig_bytes_down.savefig(f'{path}_histograma_bytes_down.png_fundo_branco', format='png', transparent=False)
    plt.close('all') #para liberar a memoria ocupada pelas figures
    return

def funcao_distribuicao_empirica(df,name):
    # criamos uma figure para a parte do bytes up e outra para a parte do bytes down
    fig_bytes_up = plt.figure()
    fig_bytes_down = plt.figure()

    # em cada figure definimos um ax
    ax_bytes_up = fig_bytes_up.add_subplot(1,1,1)
    ax_bytes_down = fig_bytes_down.add_subplot(1,1,1)

    #usando o metodo de sturges, definimos a quantidade de bins
    sns.ecdfplot(df['bytes_up'], ax = ax_bytes_up, color ="darkblue")
    ax_bytes_up.set_title(f'Função de Distribuição Empírica de bytes up do {name}')
    ax_bytes_up.set_xlabel(f'x(Valor do bytes up)')
    ax_bytes_up.set_ylabel(f'Probabilidade F(X <= x)')

    sns.ecdfplot(df['bytes_down'], ax = ax_bytes_down, color ="darkblue")
    ax_bytes_down.set_title(f'Função de Distribuição Empírica bytes down do {name}')
    ax_bytes_down.set_xlabel(f'x(Valor do bytes down)')
    ax_bytes_down.set_ylabel(f'Probabilidade F(X <= x)')

    path = f'Estatística e Mod. Probabilist - COE241/resultados/bloco2/{name}'
    # geramos 2 imagens para cada plot, 1 com fundo transparente e outra com fundo branco
    fig_bytes_up.savefig(f'{path}_funcao-distribuicao-empirica_bytes_up_transparente.png', format='png', transparent=True)
    fig_bytes_down.savefig(f'{path}_funcao-distribuicao-empirica_bytes_down_transparente.png', format='png', transparent=True)
    fig_bytes_up.savefig(f'{path}_funcao-distribuicao-empirica_bytes_up_fundo_branco.png', format='png', transparent=False)
    fig_bytes_down.savefig(f'{path}_funcao-distribuicao-empirica_bytes_down_fundo_branco.png', format='png', transparent=False)
    plt.close('all') #para liberar a memoria ocupada pelas figures
    return


def boxplot(dfchrome, dfsmarttv):
    # criamos a figure para comparar cada uma das taxas de bps
    fig_box_plot = plt.figure(figsize=(10, 6))  
    ax_data = fig_box_plot.add_subplot(1, 1, 1)
    
    # criamos o boxplot
    box = ax_data.boxplot([dfchrome['bytes_up'], dfsmarttv['bytes_up'], dfchrome['bytes_down'], dfsmarttv['bytes_down']],patch_artist=True, notch=True,  widths=0.6)
    
    ax_data.set_xticklabels(['Bytes Up (Chrome)', 'Bytes Up (Smart TV)', 'Bytes Down (Chrome)', 'Bytes Down (Smart TV)'], fontsize=10)
    ax_data.set_title(f'Comparação de Taxas de Upload/Download', fontsize=14)
    ax_data.set_ylabel('Taxa (bps)', fontsize=10)
    
    # botamos grades para facilitar a visualização
    ax_data.yaxis.grid(True, linestyle='--', alpha=0.7)
    
    # plt.tight_layout() 
    path = f'Estatística e Mod. Probabilist - COE241/resultados/bloco2/'
    # geramos 2 imagens para cada plot, 1 com fundo transparente e outra com fundo branco
    fig_box_plot.savefig(f'{path}boxplot_transparente.png', format='png', transparent=True)
    fig_box_plot.savefig(f'{path}boxplot_fundo_branco.png', format='png', transparent=False)
    plt.close('all') #para liberar a memoria ocupada pelas figures
    return


def media_variancia_desvio_padrao(dfchrome,dfsmarttv):
    # criamos um arquivo txt e com as funcoes prontas do pandas extraimos as estatisticas
    with open('Estatística e Mod. Probabilist - COE241/resultados/bloco2/media_variancia_desvio_padrao.txt', 'w') as file:
        file.write("Estatísticas do Chrome Cast[dos dados em log10]: \n")
        file.write(f"Média bytes_up: {dfchrome['bytes_up'].mean()}bps \n")
        file.write(f"Variância bytes_up: {dfchrome['bytes_up'].var()}bps^2 \n")
        file.write(f"Desvio padrão bytes_up: {dfchrome['bytes_up'].std()}bps \n")
        file.write(f"Média bytes_down: {dfchrome['bytes_down'].mean()}bps \n")
        file.write(f"Variância bytes_down: {dfchrome['bytes_down'].var()}bps^2 \n")
        file.write(f"Desvio padrão bytes_down: {dfchrome['bytes_down'].std()}bps \n")
        file.write("\n")
        file.write("Estatísticas da Smart TV[dos dados em log10]: \n")
        file.write(f"Média bytes_up: {dfsmarttv['bytes_up'].mean()}bps \n")
        file.write(f"Variância bytes_up: {dfsmarttv['bytes_up'].var()}bps^2 \n")
        file.write(f"Desvio padrão bytes_up: {dfsmarttv['bytes_up'].std()}bps \n")
        file.write(f"Média bytes_down: {dfsmarttv['bytes_down'].mean()}bps \n")
        file.write(f"Variância bytes_down: {dfsmarttv['bytes_down'].var()}bps^2 \n")
        file.write(f"Desvio padrão bytes_down: {dfsmarttv['bytes_down'].std()}bps \n")
        file.close()
    return

def bloco_2_estatistica_gerais():
    print("Obtendo estatísticas gerais!")
    dfchrome, dfsmarttv = bloco_1_reescalonar_dados()
    histograma_bloco_2(dfchrome, "chromecast")
    histograma_bloco_2(dfsmarttv, "smart tv")
    funcao_distribuicao_empirica(dfchrome, "chromecast")
    funcao_distribuicao_empirica(dfsmarttv, "smart tv")
    boxplot(dfchrome,dfsmarttv)
    media_variancia_desvio_padrao(dfchrome,dfsmarttv)
    print("Estatísticas gerais obtidas!")
    return

#aqui começamos as funcoes para o bloco 3
def bloco_3_data():
    # vamos reorgazinar os dados de acordo com hora para podermos fazer o que é pedido
    dfchrome,dfsmarttv = bloco_1_reescalonar_dados()

    dfchrome['date_hour'] = pd.to_datetime(dfchrome['date_hour']).dt.hour
    dfsmarttv['date_hour'] = pd.to_datetime(dfsmarttv['date_hour']).dt.hour

    # agora os dataframes estão filtrados por hora onde por exemplo a hora 0 representa o horário 12:XX:XX AM
    return dfchrome,dfsmarttv



def boxplot_por_hora():
    
    # primeiro reorgazinamos os nossos dataframes
    dfchrome,dfsmarttv = bloco_3_data()    

    # criamos a figure para cada um dos itens pedidos 
    fig_chrome_upload = plt.figure()  
    ax_chrome_upload = fig_chrome_upload.add_subplot(1, 1, 1)

    fig_chrome_download = plt.figure()  
    ax_chrome_download = fig_chrome_download.add_subplot(1, 1, 1)

    fig_smarttv_upload = plt.figure()  
    ax_smarttv_upload = fig_smarttv_upload.add_subplot(1, 1, 1)

    fig_smarttv_download = plt.figure()  
    ax_smarttv_download = fig_smarttv_download.add_subplot(1, 1, 1)

    # agora fazemos cada um dos plots

    dfchrome.boxplot(column='bytes_up', by='date_hour', figsize=(10, 6), ax= ax_chrome_upload, grid=False)
    dfchrome.boxplot(column='bytes_down', by='date_hour', figsize=(10, 6), ax= ax_chrome_download, grid=False)
    dfsmarttv.boxplot(column='bytes_up', by='date_hour', figsize=(10, 6), ax= ax_smarttv_upload, grid=False)
    dfsmarttv.boxplot(column='bytes_down', by='date_hour', figsize=(10, 6), ax= ax_smarttv_download, grid=False)

    ax_chrome_upload.set_title("Taxa de uploads chromecast por horário")
    ax_chrome_upload.set_xlabel("Horário")
    ax_chrome_upload.set_ylabel("Taxa(bps)")
    ax_chrome_upload.yaxis.grid(True, linestyle='--',alpha = 0.7)

    ax_chrome_download.set_title("Taxa de downloads chromecast por horário")
    ax_chrome_download.set_xlabel("Horário")
    ax_chrome_download.set_ylabel("Taxa(bps)")
    ax_chrome_download.yaxis.grid(True, linestyle='--',alpha = 0.7)

    ax_smarttv_upload.set_title("Taxa de uploads smarttv por horário")
    ax_smarttv_upload.set_xlabel("Horário")
    ax_smarttv_upload.set_ylabel("Taxa(bps)")
    ax_smarttv_upload.yaxis.grid(True, linestyle='--',alpha = 0.7)

    ax_smarttv_download.set_title("Taxa de downloads smarttv por horário")
    ax_smarttv_download.set_xlabel("Horário")
    ax_smarttv_download.set_ylabel("Taxa(bps)")
    ax_smarttv_download.yaxis.grid(True, linestyle='--',alpha = 0.7)


    path = f'Estatística e Mod. Probabilist - COE241/resultados/bloco3/'
    # geramos 2 imagens para cada plot, 1 com fundo transparente e outra com fundo branco
    fig_chrome_upload.savefig(f'{path}boxplot_chrome_upload_transparente.png', format='png', transparent=True)
    fig_chrome_upload.savefig(f'{path}boxplot_chrome_upload_fundo_branco.png', format='png', transparent=False)

    fig_chrome_download.savefig(f'{path}boxplot_chrome_download_transparente.png', format='png', transparent=True)
    fig_chrome_download.savefig(f'{path}boxplot_chrome_download_fundo_branco.png', format='png', transparent=False)

    fig_smarttv_upload.savefig(f'{path}boxplot_smarttv_upload_transparente.png', format='png', transparent=True)
    fig_smarttv_upload.savefig(f'{path}boxplot_smarttv_upload_fundo_branco.png', format='png', transparent=False)

    fig_smarttv_download.savefig(f'{path}boxplot_smarttv_download_transparente.png', format='png', transparent=True)
    fig_smarttv_download.savefig(f'{path}boxplot_smarttv_download_fundo_branco.png', format='png', transparent=False)

    plt.close('all') #para liberar a memoria ocupada pelas figures
    return

def media_variancia_desvio_padrao_por_horario():

    # primeiro reorgazinamos os nossos dataframes
    dfchrome,dfsmarttv = bloco_3_data()    

    # agora vamos calcular todos os dados que precisamos para fazer os plots
    chrome_upload_estatisticas = dfchrome.groupby(dfchrome['date_hour'])['bytes_up'].agg(['mean', 'var', 'std'])
    chrome_download_estatisticas = dfchrome.groupby(dfchrome['date_hour'])['bytes_down'].agg(['mean', 'var', 'std'])
    smarttv_upload_estatisticas = dfsmarttv.groupby(dfsmarttv['date_hour'])['bytes_up'].agg(['mean', 'var', 'std'])
    smarttv_download_estatisticas = dfsmarttv.groupby(dfsmarttv['date_hour'])['bytes_down'].agg(['mean', 'var', 'std'])

    # criamos a figure para cada um dos itens pedidos e plotamos o necessário
    fig_chrome_upload_media = plt.figure()  
    ax_chrome_upload_media = fig_chrome_upload_media.add_subplot(1, 1, 1)
    chrome_upload_estatisticas['mean'].plot(ax = ax_chrome_upload_media, title = "Média de Uploads Chromecast", xlabel='Hora', ylabel='Taxa(bps)')

    fig_chrome_upload_variancia = plt.figure()  
    ax_chrome_upload_variancia = fig_chrome_upload_variancia.add_subplot(1, 1, 1)
    chrome_upload_estatisticas['var'].plot(ax=ax_chrome_upload_variancia, title = "Variância de Uploads Chromecast", xlabel='Hora', ylabel='Taxa(bps)')

    fig_chrome_upload_desviopadrao = plt.figure()  
    ax_chrome_upload_desviopadrao = fig_chrome_upload_desviopadrao.add_subplot(1, 1, 1)
    chrome_upload_estatisticas['std'].plot(ax=ax_chrome_upload_desviopadrao, title = "Desvio padrão de Uploads Chromecast", xlabel='Hora', ylabel='Taxa(bps)')

    fig_chrome_download_media = plt.figure()  
    ax_chrome_download_media = fig_chrome_download_media.add_subplot(1, 1, 1)
    chrome_download_estatisticas['mean'].plot(ax=ax_chrome_download_media, title = "Média de Downloads Chromecast", xlabel='Hora', ylabel='Taxa(bps)')

    fig_chrome_download_variancia = plt.figure()  
    ax_chrome_download_variancia = fig_chrome_download_variancia.add_subplot(1, 1, 1)
    chrome_download_estatisticas['var'].plot(ax=ax_chrome_download_variancia, title = "Variância de Downloads Chromecast", xlabel='Hora', ylabel='Taxa(bps)')

    fig_chrome_download_desviopadrao = plt.figure()  
    ax_chrome_download_desviopadrao = fig_chrome_download_desviopadrao.add_subplot(1, 1, 1)
    chrome_download_estatisticas['std'].plot(ax=ax_chrome_download_desviopadrao, title = "Desvio padrão de Downloads Chromecast", xlabel='Hora', ylabel='Taxa(bps)')

    fig_smarttv_upload_media = plt.figure()  
    ax_smarttv_upload_media = fig_smarttv_upload_media.add_subplot(1, 1, 1)
    smarttv_upload_estatisticas['mean'].plot(ax = ax_smarttv_upload_media, title = "Média de Uploads Smart tv", xlabel='Hora', ylabel='Taxa(bps)')

    fig_smarttv_upload_variancia = plt.figure()  
    ax_smarttv_upload_variancia = fig_smarttv_upload_variancia.add_subplot(1, 1, 1)
    smarttv_upload_estatisticas['var'].plot(ax = ax_smarttv_upload_variancia, title = "Variância de Uploads Smart tv", xlabel='Hora', ylabel='Taxa(bps)')

    fig_smarttv_upload_desviopadrao = plt.figure()  
    ax_smarttv_upload_desviopadrao = fig_smarttv_upload_desviopadrao.add_subplot(1, 1, 1)
    smarttv_upload_estatisticas['std'].plot(ax = ax_smarttv_upload_desviopadrao, title = "Desvio padrão de Uploads Smart tv", xlabel='Hora', ylabel='Taxa(bps)')

    fig_smarttv_download_media = plt.figure()  
    ax_smarttv_download_media = fig_smarttv_download_media.add_subplot(1, 1, 1)
    smarttv_download_estatisticas['mean'].plot(ax = ax_smarttv_download_media, title = "Média de Downloads Smart tv", xlabel='Hora', ylabel='Taxa(bps)')

    fig_smarttv_download_variancia = plt.figure()  
    ax_smarttv_download_variancia = fig_smarttv_download_variancia.add_subplot(1, 1, 1)
    smarttv_download_estatisticas['var'].plot(ax = ax_smarttv_download_variancia, title = "Variância de Downloads Smart tv", xlabel='Hora', ylabel='Taxa(bps)')

    fig_smarttv_download_desviopadrao = plt.figure()  
    ax_smarttv_download_desviopadrao = fig_smarttv_download_desviopadrao.add_subplot(1, 1, 1)
    smarttv_download_estatisticas['std'].plot(ax = ax_smarttv_download_desviopadrao, title = "Desvio padrão de Downloads Smart tv", xlabel='Hora', ylabel='Taxa(bps)')

    # agora salvamos todas as figuras
    path = f'Estatística e Mod. Probabilist - COE241/resultados/bloco3/'
    # geramos 2 imagens para cada plot, 1 com fundo transparente e outra com fundo branco
    fig_chrome_upload_media.savefig(f'{path}media_chrome_upload_transparente.png', format='png', transparent=True)
    fig_chrome_upload_media.savefig(f'{path}media_chrome_upload_fundo_branco.png', format='png', transparent=False)

    fig_chrome_upload_variancia.savefig(f'{path}variancia_chrome_upload_transparente.png', format='png', transparent=True)
    fig_chrome_upload_variancia.savefig(f'{path}variancia_chrome_upload_fundo_branco.png', format='png', transparent=False)

    fig_chrome_upload_desviopadrao.savefig(f'{path}desviopadrao_chrome_upload_transparente.png', format='png', transparent=True)
    fig_chrome_upload_desviopadrao.savefig(f'{path}desviopadrao_chrome_upload_fundo_branco.png', format='png', transparent=False)

    fig_chrome_download_media.savefig(f'{path}media_chrome_download_transparente.png', format='png', transparent=True)
    fig_chrome_download_media.savefig(f'{path}media_chrome_download_fundo_branco.png', format='png', transparent=False)

    fig_chrome_download_variancia.savefig(f'{path}variancia_chrome_download_transparente.png', format='png', transparent=True)
    fig_chrome_download_variancia.savefig(f'{path}variancia_chrome_download_fundo_branco.png', format='png', transparent=False)

    fig_chrome_download_desviopadrao.savefig(f'{path}desviopadrao_chrome_download_transparente.png', format='png', transparent=True)
    fig_chrome_download_desviopadrao.savefig(f'{path}desviopadrao_chrome_download_fundo_branco.png', format='png', transparent=False)

    fig_smarttv_upload_media.savefig(f'{path}media_smarttv_upload_transparente.png', format='png', transparent=True)
    fig_smarttv_upload_media.savefig(f'{path}media_smarttv_upload_fundo_branco.png', format='png', transparent=False)

    fig_smarttv_upload_variancia.savefig(f'{path}variancia_smarttv_upload_transparente.png', format='png', transparent=True)
    fig_smarttv_upload_variancia.savefig(f'{path}variancia_smarttv_upload_fundo_branco.png', format='png', transparent=False)

    fig_smarttv_upload_desviopadrao.savefig(f'{path}desviopadrao_smarttv_upload_transparente.png', format='png', transparent=True)
    fig_smarttv_upload_desviopadrao.savefig(f'{path}desviopadrao_smarttv_upload_fundo_branco.png', format='png', transparent=False)

    fig_smarttv_download_media.savefig(f'{path}media_smarttv_download_transparente.png', format='png', transparent=True)
    fig_smarttv_download_media.savefig(f'{path}media_smarttv_download_fundo_branco.png', format='png', transparent=False)

    fig_smarttv_download_variancia.savefig(f'{path}variancia_smarttv_download_transparente.png', format='png', transparent=True)
    fig_smarttv_download_variancia.savefig(f'{path}variancia_smarttv_download_fundo_branco.png', format='png', transparent=False)

    fig_smarttv_download_desviopadrao.savefig(f'{path}desviopadrao_smarttv_download_transparente.png', format='png', transparent=True)
    fig_smarttv_download_desviopadrao.savefig(f'{path}desviopadrao_smarttv_download_fundo_branco.png', format='png', transparent=False)

    plt.close('all') #para liberar a memoria ocupada pelas figures
    return 

def bloco_3_estatisticas_por_hora():
    print("Obtendo estatísticas por hora!")
    boxplot_por_hora()
    media_variancia_desvio_padrao_por_horario()
    print("Estatísticas por hora obtidas!")
    return 

# aqui comecamos as funcoes para o bloco 4
def bloco_4_data():
    # vamos pegar os dados que tem os maiores valores de media para um horario
    # primeiro reorgazinamos os nossos dataframes
    dfchrome,dfsmarttv = bloco_3_data()    

    # agora vamos calcular todos os dados que precisamos para fazer os plots
    chrome_upload_estatisticas = dfchrome.groupby(dfchrome['date_hour'])['bytes_up'].mean()
    chrome_download_estatisticas = dfchrome.groupby(dfchrome['date_hour'])['bytes_down'].mean()
    smarttv_upload_estatisticas = dfsmarttv.groupby(dfsmarttv['date_hour'])['bytes_up'].mean()
    smarttv_download_estatisticas = dfsmarttv.groupby(dfsmarttv['date_hour'])['bytes_down'].mean()

    maximo_chrome_upload_hora = chrome_upload_estatisticas.idxmax()
    maximo_chrome_download_hora = chrome_download_estatisticas.idxmax()
    maximo_smarttv_upload_hora = smarttv_upload_estatisticas.idxmax()
    maximo_smarttv_download_hora = smarttv_download_estatisticas.idxmax()

    # agora que já obtemos os dados que precisávamos, vamos criar 4 datasets conforme o solicitado
    df_chrome_max_upload = dfchrome[dfchrome['date_hour'] == maximo_chrome_upload_hora][['device_id', 'date_hour', 'bytes_up']]
    df_chrome_max_download = dfchrome[dfchrome['date_hour'] == maximo_chrome_download_hora][['device_id', 'date_hour', 'bytes_down']]
    df_smarttv_max_upload = dfsmarttv[dfsmarttv['date_hour'] == maximo_smarttv_upload_hora][['device_id', 'date_hour', 'bytes_up']]
    df_smarttv_max_download = dfsmarttv[dfsmarttv['date_hour'] == maximo_smarttv_download_hora][['device_id', 'date_hour', 'bytes_down']]
    

    print(f"O horário de maior média de upload para o Chrome Cast é: {maximo_chrome_upload_hora} horas \n", f"O horário de maior média de download para o Chrome Cast é: {maximo_chrome_download_hora} horas \n", 
    f"O horário de maior média de upload para a Smart TV é: {maximo_smarttv_upload_hora} horas \n", f"O horário de maior média de download para a Smart TV é: {maximo_smarttv_download_hora} horas \n")

    return df_chrome_max_upload, df_chrome_max_download, df_smarttv_max_upload, df_smarttv_max_download

def histograma_bloco_4():
    
    # criamos os nossos dataframes 
    df_chrome_max_upload, df_chrome_max_download, df_smarttv_max_upload, df_smarttv_max_download = bloco_4_data()

    # criamos uma figure para cada um dos histogramas
    fig_chrome_bytes_up = plt.figure()
    ax_chrome_bytes_up = fig_chrome_bytes_up.add_subplot(1,1,1)

    fig_chrome_bytes_down = plt.figure()
    ax_chrome_bytes_down = fig_chrome_bytes_down.add_subplot(1,1,1)

    fig_smarttv_bytes_up = plt.figure()
    ax_smarttv_bytes_up = fig_smarttv_bytes_up.add_subplot(1,1,1)

    fig_smarttv_bytes_down = plt.figure()
    ax_smarttv_bytes_down = fig_smarttv_bytes_down.add_subplot(1,1,1)

    #usando o metodo de sturges, definimos a quantidade de bins
    bins_chrome_bytes_up = np.round(1 + 3.322*(np.log10(len(df_chrome_max_upload))))
    bins_chrome_bytes_down = np.round(1 + 3.322*(np.log10(len(df_chrome_max_download))))
    bins_smarttv_bytes_up = np.round(1 + 3.322*(np.log10(len(df_smarttv_max_upload))))
    bins_smarttv_bytes_down = np.round(1 + 3.322*(np.log10(len(df_smarttv_max_download))))

    # fazemos os plots
    ax_chrome_bytes_up.hist(df_chrome_max_upload['bytes_up'], bins=int(bins_chrome_bytes_up),edgecolor ="darkblue")
    ax_chrome_bytes_up.set_xlabel(f'Histograma de bytes_up do chrome no horário com maior média')

    ax_chrome_bytes_down.hist(df_chrome_max_download['bytes_down'], bins=int(bins_chrome_bytes_down),edgecolor ="darkblue")
    ax_chrome_bytes_down.set_xlabel(f'Histograma de bytes_down do chrome no horário com maior média')

    ax_smarttv_bytes_up.hist(df_smarttv_max_upload['bytes_up'], bins=int(bins_smarttv_bytes_up),edgecolor ="darkblue")
    ax_smarttv_bytes_up.set_xlabel(f'Histograma de bytes_up da smart tv no horário com maior média')

    ax_smarttv_bytes_down.hist(df_smarttv_max_download['bytes_down'], bins=int(bins_smarttv_bytes_down),edgecolor ="darkblue")
    ax_smarttv_bytes_down.set_xlabel(f'Histograma de bytes_down da smart tv no horário com maior média')
    
    path = f'Estatística e Mod. Probabilist - COE241/resultados/bloco4/'
    # geramos 2 imagens para cada plot, 1 com fundo transparente e outra com fundo branco
    fig_chrome_bytes_up.savefig(f'{path}_histograma_chrome_bytes_up_transparente.png', format='png', transparent=True)
    fig_chrome_bytes_up.savefig(f'{path}_histograma_chrome_bytes_up_fundo_branco.png', format='png', transparent=False)

    fig_chrome_bytes_down.savefig(f'{path}_histograma_chrome_bytes_down_transparente.png', format='png', transparent=True)
    fig_chrome_bytes_down.savefig(f'{path}_histograma_chrome_bytes_down_fundo_branco.png', format='png', transparent=False)

    fig_smarttv_bytes_up.savefig(f'{path}_histograma_smarttv_bytes_up_transparente.png', format='png', transparent=True)
    fig_smarttv_bytes_up.savefig(f'{path}_histograma_smarttv_bytes_up_fundo_branco.png', format='png', transparent=False)

    fig_smarttv_bytes_down.savefig(f'{path}_histograma_smarttv_bytes_down_transparente.png', format='png', transparent=True)
    fig_smarttv_bytes_down.savefig(f'{path}_histograma_smarttv_bytes_down_fundo_branco.png', format='png', transparent=False)
    plt.close('all') #para liberar a memoria ocupada pelas figures
    return 

def QQplot():
    # criamos os nossos dataframes 
    df_chrome_max_upload, df_chrome_max_download, df_smarttv_max_upload, df_smarttv_max_download = bloco_4_data()

    # criamos uma figure para cada um dos QQplots
    fig_qqplot_upload = plt.figure()
    ax_qqplot_upload = fig_qqplot_upload.add_subplot(1,1,1)

    fig_qqplot_download = plt.figure()
    ax_qqplot_download = fig_qqplot_download.add_subplot(1,1,1)

    # agpra vamos seguir o passo a passo recomendado na orientacao do trabalho
    # primeiro ordenamos os nossos dataframes
    df_chrome_max_upload.sort_values('bytes_up',inplace=True)
    df_chrome_max_download.sort_values('bytes_down',inplace=True)
    df_smarttv_max_upload.sort_values('bytes_up',inplace=True)
    df_smarttv_max_download.sort_values('bytes_down',inplace=True)

    # agora calculamos os quantis para o conjunto com menor amostras em cada um dos casos
    
    if(df_chrome_max_upload.shape[0]>df_smarttv_max_upload.shape[0]):
        menor_upload = df_smarttv_max_upload['bytes_up']
        maior_upload = df_chrome_max_upload['bytes_up']
    else: 
        maior_upload = df_smarttv_max_upload['bytes_up']
        menor_upload = df_chrome_max_upload['bytes_up']
   
    if(df_chrome_max_download.shape[0]>df_smarttv_max_download.shape[0]):
        menor_download = df_smarttv_max_download['bytes_down']
        maior_download = df_chrome_max_download['bytes_down']
    else: 
        maior_download = df_smarttv_max_download['bytes_down']
        menor_download = df_chrome_max_download['bytes_down']
    
    # agora que temos os nossos dados organizados podemos fazer o qq plot conforme solicitado usando a funcao de plotar da biblioteca statsmodels
    # primeiro fazemos o do upload
    sm.qqplot_2samples(menor_upload, maior_upload, line='r', ax=ax_qqplot_upload)
    ax_qqplot_upload.set_title('QQ Plot - Upload')
    ax_qqplot_upload.set_ylabel("Quantiles da primeira amostra")
    ax_qqplot_upload.set_xlabel("Quantiles da segunda amostra")

    # agora fazemos o do download
    sm.qqplot_2samples(menor_download, maior_download, line='r', ax=ax_qqplot_download)
    ax_qqplot_download.set_title('QQ Plot - Download')
    ax_qqplot_download.set_ylabel("Quantiles da primeira amostra")
    ax_qqplot_download.set_xlabel("Quantiles da segunda amostra")

    path = f'Estatística e Mod. Probabilist - COE241/resultados/bloco4/'
    # geramos 2 imagens para cada plot, 1 com fundo transparente e outra com fundo branco
    fig_qqplot_upload.savefig(f'{path}_qqplot_upload_transparente.png', format='png', transparent=True)
    fig_qqplot_upload.savefig(f'{path}_qqplot_upload_fundo_branco.png', format='png', transparent=False)

    fig_qqplot_download.savefig(f'{path}_qqplot_download_transparente.png', format='png', transparent=True)
    fig_qqplot_download.savefig(f'{path}_qqplot_download_fundo_branco.png', format='png', transparent=False)

    plt.close('all') #para liberar a memoria ocupada pelas figures
    return

def bloco_4_caracterizando_maior_valor_trafego():
    print("Obtendo historgrama e qqplot!")
    histograma_bloco_4()
    QQplot()
    print("Historgrama e qqplot obtidos!")
    return

# aqui começamos as funções do bloco 5

def scatter_plot():
    # criamos os nossos dataframes 
    df_chrome_max_upload, df_chrome_max_download, df_smarttv_max_upload, df_smarttv_max_download = bloco_4_data()

    # corrigimos os nossos dataframes e unimos eles em um só de forma que eles tenham a mesma quantidade de elementos para evitar problemas de nan ou incompatibilidade
    # por algum motivo o dataframe dos dados do chrome precisaram de uma correção mais profunda
    df_chrome_max_upload = df_chrome_max_upload.reset_index(drop=True)
    df_chrome_max_download = df_chrome_max_download.reset_index(drop=True)

    # df_chrome_upload_download = pd.concat([df_chrome_max_upload[['bytes_up']], df_chrome_max_download[['bytes_down']]], axis=1)
    df_chrome_upload_download = df_chrome_max_upload[['bytes_up']].join(df_chrome_max_download[['bytes_down']], how='inner')
    df_smarttv_upload_download = df_smarttv_max_upload[['bytes_up']].join(df_smarttv_max_download[['bytes_down']], how='inner')

    # calculamos os coeficientes de correlacao amostrais, vamos disponibilizar essas informacoes nos graficos
    coeficiente_correlacao_chrome = df_chrome_upload_download['bytes_up'].corr(df_chrome_upload_download['bytes_down'])
    coeficiente_correlacao_smarttv = df_smarttv_upload_download['bytes_up'].corr(df_smarttv_upload_download['bytes_down'])

    # criamos uma figure para cada um dos scatteplots
    fig_scatterplot_chrome = plt.figure()
    ax_scatterplot_chrome = fig_scatterplot_chrome.add_subplot(1,1,1)

    fig_scatterplot_smarttv = plt.figure()
    ax_scatterplot_smarttv = fig_scatterplot_smarttv.add_subplot(1,1,1)
    
    # fazemos os plots
    ax_scatterplot_chrome.scatter(df_chrome_upload_download['bytes_up'], df_chrome_upload_download['bytes_down'], alpha=0.7, color='blue')
    ax_scatterplot_chrome.set_title(f'Scatterplot Chrome: Upload vs Download \n Coeficiente de Correlação Amostral :{coeficiente_correlacao_chrome}')
    ax_scatterplot_chrome.set_xlabel('Upload (bps)')
    ax_scatterplot_chrome.set_ylabel('Download (bps)')

    ax_scatterplot_smarttv.scatter(df_smarttv_upload_download['bytes_up'], df_smarttv_upload_download['bytes_down'], alpha=0.7, color='blue')
    ax_scatterplot_smarttv.set_title(f'Scatterplot Smart tv: Upload vs Download \n Coeficiente de Correlação Amostral :{coeficiente_correlacao_smarttv}')
    ax_scatterplot_smarttv.set_xlabel('Upload (bps)')
    ax_scatterplot_smarttv.set_ylabel('Download (bps)')

    path = f'Estatística e Mod. Probabilist - COE241/resultados/bloco5/'
    # geramos 2 imagens para cada plot, 1 com fundo transparente e outra com fundo branco
    fig_scatterplot_chrome.savefig(f'{path}_scatterplot_chrome_transparente.png', format='png', transparent=True)
    fig_scatterplot_chrome.savefig(f'{path}_scatterplot_chrome_fundo_branco.png', format='png', transparent=False)

    fig_scatterplot_smarttv.savefig(f'{path}_scatterplot_smarttv_transparente.png', format='png', transparent=True)
    fig_scatterplot_smarttv.savefig(f'{path}_scatterplot_smarttv_fundo_branco.png', format='png', transparent=False)
    plt.close('all') #para liberar a memoria ocupada pelas figures
    return

def bloco_5_correlacao():
    print("Obtendo scatterplot!")
    scatter_plot()
    print("Scatterplot obtido!")
    return

# agora que já criamos todas as funções e podemos obter todos os dados dos relatorios, vamos fazer uma funcao que junta tudo e executala

def main():
    print("Começando coleta de dados")
    bloco_2_estatistica_gerais()
    bloco_3_estatisticas_por_hora()
    bloco_4_caracterizando_maior_valor_trafego()
    bloco_5_correlacao()
    print("Coleta de dados finalizada! :)")
    return

main()
