import xml.etree.cElementTree as ET
from registro import Registro
from curriculos import *
from listainvertida import ListaInvertida
from unidecode import unidecode
import re
from interface import *
from math import log
from operator import itemgetter
import os


class Main:
    def __init__(self):
        self.tela = Interface(self)
        self.lista_documentos = []
        self.lugares_temp = dict()
        self.lista_lugares = []
        self.global_count = 1
      
    def converte_para_grams(self, termo_pesquisado):
        lista_pesquisa = termo_pesquisado.split(' ')
        lista_grams = []
        for i in lista_pesquisa:
            for j in range(len(i)-2):
                lista_grams.append(i[j].title()+i[j+1]+i[j+2])
        return lista_grams
      
    def gerar_classes(self):
        doc_count = 1
        path = os.getcwd() + "/curriculos"
        for filename in os.listdir(path):
            documento = {}
            if filename.endswith(".xml"):
                os.chdir(path)
                tree = ET.ElementTree(file=filename)
                root = tree.getroot()

                lista_nomes = []
                lista_artigos = []
                texto_nomes = ''
                texto_artigos = ''
                tags = [
                    "DADOS-GERAIS",
                    "NOME-COMPLETO",
                    "NOME-EM-CITACOES-BIBLIOGRAFICAS",
                    "PRODUCAO-BIBLIOGRAFICA",
                    "ARTIGO-PUBLICADO",
                    "DADOS-BASICOS-DO-ARTIGO",
                    "ANO-DO-ARTIGO",
                    "TITULO-DO-ARTIGO",
                    "DETALHAMENTO-DO-ARTIGO",
                    "TITULO-DO-PERIODICO-OU-REVISTA"
                ]
                for chld in root:
                    if chld.tag == tags[0]:
                        lista_nomes.append(chld.get(tags[1]))
                        texto_nomes += chld.get(tags[1])
                        for nome in (chld.get(tags[2]).split(";")):
                            lista_nomes.append(nome)
                for chld in root:
                    if chld.tag == tags[3]:
                        for attr in chld:
                            for block in attr:
                                if block.tag == tags[4]:
                                    for line in block:
                                        if line.tag == tags[5]:
                                            ano = line.get(tags[6])
                                            trab = line.get(tags[7])
                                            trab = unidecode(
                                                re.sub(r'[^\w\s]',
                                                '',
                                                trab))
                                        if line.tag == tags[8]:
                                            artigo = line.get(tags[9])
                                            artigo_limpo = unidecode(
                                                re.sub(r'[^\w\s]',
                                                '',
                                                artigo.title()))
                                            texto_artigos += ' ' + artigo
                                            
                                            if artigo_limpo not in lista_artigos:
                                                lista_artigos.append([artigo_limpo,
                                                                      ano,
                                                                      trab])
                                                
                                            if self.lista_lugares == []:
                                                dic_temp = dict()
                                                dic_temp['id'] = self.global_count
                                                dic_temp['docs'] = [doc_count]
                                                dic_temp['texto_nomes'] = artigo_limpo
                                                self.lista_lugares.append(dic_temp)
                                                self.global_count += 1
                                            
                                            else:
                                                found = 0
                                                for lugar in self.lista_lugares:
                                                    if lugar['texto_nomes'] == artigo_limpo:
                                                        if doc_count not in lugar['docs']:
                                                            lugar['docs'].append(doc_count)
                                                        found = 1
                                                
                                                if found == 0:
                                                    dic_temp = dict()
                                                    dic_temp['id'] = self.global_count
                                                    dic_temp['docs'] = [doc_count]
                                                    dic_temp['texto_nomes'] = artigo_limpo
                                                    self.lista_lugares.append(dic_temp)
                                                    self.global_count += 1
                                                
                documento['id'] = doc_count
                documento['nomes'] = lista_nomes
                documento['artigos'] = lista_artigos
                documento['texto_nomes'] = texto_nomes
                documento['texto_artigos'] = texto_artigos
                self.lista_documentos.append(documento)
                doc_count += 1
           
    def iniciar(self):
        self.tela.criar_tela()
        rodando = True
        
        reg_nomes = Registro()
        reg_artigos = Registro()
        
        index_nomes = ListaInvertida(reg_nomes)
        index_artigos = ListaInvertida(reg_artigos)

        for documento in self.lista_documentos:
            index_nomes.processar_documento(documento)

        for lugar in self.lista_lugares:
            index_artigos.processar_documento(lugar)
               
        while rodando:

            event, values = self.tela.le_eventos()
            if event == sg.WIN_CLOSED:
                rodando = False
        
            elif event == "Buscar por nome":
                self.tela.limpa_resultado()
                resultado = self.converte_para_grams(values["nome"].lower())
                
                dic_score = dict()
                for gram in resultado:
                    if gram in index_nomes.index:
                        presenca = len(index_nomes.index[gram])
                        for aparicao in index_nomes.index[gram]:
                            tf = aparicao.frequencia/aparicao.frequencia_geral
                            idf = log(29/presenca, 2) + 1
                            tf_idf = (tf) * (idf)
                            if aparicao.docId in dic_score:
                                dic_score[aparicao.docId] += tf_idf
                            else:
                                dic_score[aparicao.docId] = tf_idf
                
                if (dic_score == {}):
                    print('Nenhum resultado encontrado.')
                
                else:                     
                    for count in range(len(dic_score)):
                        if count >= values["num"]:
                            break
                        maior_pontuacao = 0
                        maior_Id = 0
                        for Id, pontuacao in dic_score.items():
                            if pontuacao > maior_pontuacao:
                                maior_pontuacao = pontuacao
                                maior_Id = Id
                        print(reg_nomes.get(maior_Id)['nomes'][0])
                        print('--------------------------------------------')
                        lista_temp = []
                        for artigo in reg_nomes.get(maior_Id)['artigos']:
                            lista_temp.append(artigo)
                        lista_sorted = sorted(lista_temp,key=itemgetter(1))
                        lista_sorted.reverse()
                        dic_print = {}
                        for item in lista_sorted:
                            if item[0] not in dic_print:
                                dic_print[item[0]] = [[item[1], item[2]]]
                            else:
                                dic_print[item[0]].append([item[1], item[2]])
                        for key in dic_print:
                            print(f'  - {key}')
                            print()
                            for sub_key in dic_print[key]:
                                print(f'     "{sub_key[1]}", {sub_key[0]}.')
                            #print(f'  - {key}. {dic_print[key]}.')
                            print()
                            print()
                        print()
                        del dic_score[maior_Id]
                        
            elif event == "Buscar por local de publicação":
                self.tela.limpa_resultado()
                resultado = self.converte_para_grams(values["nome"].lower())
                
                dic_score = dict()
                for gram in resultado:
                    if gram in index_artigos.index:
                        presenca = len(index_artigos.index[gram])
                        for aparicao in index_artigos.index[gram]:
                            tf = aparicao.frequencia/aparicao.frequencia_geral
                            idf = log(374/presenca, 2) + 1
                            tf_idf = (tf) * (idf)
                            if aparicao.docId in dic_score:
                                dic_score[aparicao.docId] += tf_idf
                            else:
                                dic_score[aparicao.docId] = tf_idf
                                
                if (dic_score == {}):
                    print('Nenhum resultado encontrado.')
                
                else:                     
                    for count in range(len(dic_score)):
                        if count >= values["num"]:
                            break
                        maior_pontuacao = 0
                        maior_Id = 0
                        for Id, pontuacao in dic_score.items():
                            if pontuacao > maior_pontuacao:
                                maior_pontuacao = pontuacao
                                maior_Id = Id
                        print(reg_artigos.get(maior_Id)['texto_nomes'])
                        print('--------------------------------------------')
                        for id in reg_artigos.get(maior_Id)['docs']:
                            for documento in self.lista_documentos:
                                if id == documento['id']:
                                    print(f'  - {documento["nomes"][0]}')
                        print()
                        del dic_score[maior_Id]
                
            elif event == "Limpar":
                self.tela.limpa_resultado()
            
        self.tela.fim()
