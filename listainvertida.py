from aparicao import Aparicao
from unidecode import unidecode
import re


class ListaInvertida:
    def __init__(self, reg):
        self.index = dict()
        self.reg = reg

    def __repr__(self):
        return str(self.index)

    def processar_documento(self, documento):
        # Removendo pontuacao
        clean_text = unidecode(re.sub(r'[^\w\s]', '', documento['texto_nomes']))
        
        # Limpando o texto referente a cada documento
        termos = []
        termos_temp = clean_text.title().split(' ')

        for i in termos_temp:
            if (isinstance(i, str) and len(i) >= 3 and i not in termos):
                termos.append(i)

        # Separando os termos em formato de 3-grams
        dic_temp = []
        for termo in termos:
            for i in range(len(termo)-2):
                dic_temp.append(termo[i].title()+termo[i+1]+termo[i+2])
                
        # Instanciando as aparicoes de cada gram
        dic_aparicoes = dict()
        for gram in dic_temp:
            frequencia_termo = (dic_aparicoes[gram].frequencia
                                if gram in dic_aparicoes
                                else 0)
            dic_aparicoes[gram] = Aparicao(documento['id'],
                                           frequencia_termo + 1,
                                           len(dic_temp))
        
        # Atualiza a lista invertida
        update_dic = {key: [appearance]
        if key not in self.index
        else self.index[key] + [appearance]
                       for (key, appearance) in dic_aparicoes.items()} 
        self.index.update(update_dic)
        
        # Adiciona o documento no registro
        self.reg.add(documento)
