import pandas as pd
import datetime
class Consistencia():
#criando um datarame vazio para inserir os erros encontrados na base de dados
    def __init__(self):
        self.df_resultado = pd.DataFrame(columns = ['ID-SGC', 'ID-P', 'P', 'C1', 'Data da Entrevista', 
        'Entrevistador(a)', 'Cód. Questão', 'Rót. Questão', 'Erro']) 
#crianddo uma lista de colunas de interesse nas abas de pessoas e de propriedades. Mudar de  acordo com o proeto
        self.colunas_de_interesse = ['ID-SGC','C1', 'C2', '1.1.1'] 
        self.colunas_de_interesse_pessoas = ['ID-SGC', 'C1', 'C2', 'ID-P', 'P']

    def abrir_bases(self, arquivo):
        print("Iniciando...")
        print("Carregando aba de Propriedade...")
        self.dfpropriedade = pd.DataFrame(pd.read_excel(f"{arquivo}.xlsx", sheet_name = "propriedade"))
        print("Carregando aba de Pessoas...")
        self.dfpessoas = pd.DataFrame(pd.read_excel(f"{arquivo}.xlsx", sheet_name = "pessoas"))
        print("Tudo pronto!")

    def valida_missing_propriedades (self, df, value):
        missing_prop = []
        #checar misings na aba propriedades / retorna um df com valores boleanos True (caso encontre o valor procurao) or False (caso não encontre )
        checkprop = df.isin([value])
        #checando em quais colunas tem o valor procurado (missing)
        seriesObj = checkprop.any()
        #salvando em uma lista, o nome da coluna aonde foi encontrado o valor procurado
        colErrosProp = list(seriesObj[seriesObj == True].index)
        #looping para identificar o index aonde o valor procurado existe no dataframe e salvar em uma lista chamada linhas esta indicação
        for col in colErrosProp:
            rows = list(checkprop[col][checkprop[col] == True].index)
        #looping para pegar o IDSGC o dataframe de propriedades na linha aonde o valor procurado (missing) foi encontrado
        #e a coluna que o valor procurado está salvando em uma lista de tuplas com [('IDSGC', 'código da coluna'),('IDSGC', 'código da coluna')]
            for row in rows:
                missing_prop.append((self.dfpropriedade['ID-SGC'][row], self.dfpropriedade['C1'][row], self.dfpropriedade['C2'][row],self.dfpropriedade['C5'][row], col, value))
        #crindo um DF com as informações basicas da pesquisa (mudar a depender do projeto), código das colunas e a resposa erro inserida no campo "Value" da função
        self.errosprop = pd.DataFrame(data = missing_prop, columns= ['ID-SGC', 'Indexador', 'Data da Entrevista', 'Coletor', 'Códio da Questão', 'Erro de resposta encontrado'])   
        return self.errosprop
    #Mesma coisa feita em propriedades
    def valida_missing_pessoas (self, df, value):
        missing_pess = []
        checkarpess = df.isin([value])
        seriesObjPess = checkarpess.any()
        colErrosPessoas = list(seriesObjPess[seriesObjPess == True].index)
        for col in colErrosPessoas:
            rows = list(checkarpess[col][checkarpess[col]==True].index)
            for row in rows:
                missing_pess.append((self.dfpessoas['ID-SGC'][row], self.dfpessoas['C1'][row], self.dfpessoas['C2'][row], self.dfpessoas['ID-P'][row], col, value))
        self.errospess = pd.DataFrame(data = missing_pess, columns= ['ID-SGC', 'Indexador', 'Data da Entrevista', 'ID-P', 'Códio da Questão', 'Erro de resposta encontrado'])
        return self.errospess
    #Validação de indexadores
    def valida_indexadores (self, df):
    #Criei uma lista com o nome das colunas que eu quer dabase inteira, para esta validação
        colunas_procuradas = ['ID-SGC','C1', 'C1.2', 'C1.3','C1.4', '1.1.1']
    #pegei o mesmo df que criei e usei nas validações de missing
        df = self.dfpropriedade
        base_de_dados = pd.DataFrame(data = df, columns= colunas_procuradas)
    #Duplicated procura por valores duplicados com o referencial das ([colunas que se passa dentro do colchetes]), 
    #Por padrão preserva o primeiro valor e aponta os outros (keep='first') ou preserva o ultimo e aponta os anteriores (keep='last')
        self.index_dupli = base_de_dados[base_de_dados.duplicated(['C1', 'C1.2', 'C1.3','C1.4'], keep='first')]
        return self.index_dupli

  






objeto = Consistencia()
#lerbase de pessoas e propridades
objeto.abrir_bases("bd156.00")
#procurar os missings em propriedades 
objeto.valida_missing_propriedades(objeto.dfpropriedade, '[missing]')
#procurarmissings em pessoas
objeto.valida_missing_pessoas(objeto.dfpessoas, '[missing]')
objeto.valida_indexadores(objeto.dfpropriedade)
objeto.planilha_de_coreção()