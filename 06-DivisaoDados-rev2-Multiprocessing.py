# Importa as bibliotecas
import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns
import numpy as np
import multiprocessing
import time

# Importa as funções de divisão de dados
import x06a_cx_alimentacao as cx_alim
import x06b_cx_recirculacao as cx_reci
import x06c_rougher1 as rg_01
import x06d_rougher2 as rg_02
import x06e_cleaner1 as cl_01
import x06f_cleaner2 as cl_02
import x06g_recleaner as recleaner
import x06h_scavenger1b1 as sc_1b1
import x06i_scavenger1b2 as sc_1b2
import x06j_scavenger1b3 as sc_1b3
import x06k_scavenger2b1 as sc_2b1
import x06l_scavenger2b2 as sc_2b2
import x06m_scavenger2b3 as sc_2b3


if __name__ == '__main__':
    starttime = time.time()
    
    target = pd.read_excel('T_Conceicao.xlsx')
    
    # Pasta para armazenamento dos dados
    #pasta = 'Experimentos/Maio/'
    pasta = 'Delay/02-Fevereiro/'

    # Data a partir da qual coletar os dados (horário da primeira análise)
    # base = target.iloc[1007][0] ## Abril 01
    #base = target.iloc[0][0] ## Primeiro dado
    base = pd.Timestamp('2019-02-01')
    #base = base - np.timedelta64(2, 'h') ## Antes do primeiro, para que pegue todos os dados disponíveis
    base = base - np.timedelta64(3, 'h') ## Antes do primeiro, para que pegue todos os dados disponíveis
    bkp_base = base
    # Data até a qual coletar os dados (última análise)
    #fim = target.iloc[1094,0] ## Abril 10
    #fim = target.iloc[-1,0]
    fim = pd.Timestamp('2019-03-01')
    bkp_fim = fim
    
    # Renomeia o cabeçalho de target
    target.columns = ['DataHora', 'Ferro', 'Silica']
    
    # Selecao dos target a partir da data inicial até a data final
    selecao = target.iloc[:,0] > base
    selecao = selecao & (target.iloc[:,0] <= fim)
    target = target[selecao]

    # Zera o índice
    target.reset_index(drop=True, inplace=True)
    
    target.to_excel(pasta + 'T_Conceicao.xlsx', 'Planilha1', index=False)
    
    # Cria uma lista de processos a serem executados de forma paralela
    #processes = []
    #funcoes = [cx_alim, cx_reci, rg_01, rg_02, cl_01, cl_02, recleaner, sc_1b1, sc_1b2, sc_1b3, sc_2b1, sc_2b2, sc_2b3]
    funcoes = [cx_alim, cx_reci, rg_01, rg_02, cl_01, recleaner, sc_1b2, sc_1b3, sc_2b3]
    #funcoes = [rg_01, sc_2b2]
    #funcoes = [sc_2b2]
    
    pool = multiprocessing.Pool() #use all available cores, otherwise specify the number you want as an argument
    for func in funcoes:
        pool.apply_async(func.executar, args=(bkp_base,bkp_fim,pasta,target,))
    pool.close()
    pool.join()

    # for func in funcoes:
        # p = multiprocessing.Process(target=func.executar, args=(bkp_base,bkp_fim,pasta,target,))
        # processes.append(p)
        # p.start()

    # for process in processes:
        # process.join()

    print('Foram gastos {} segundos'.format(time.time() - starttime))