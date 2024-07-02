import os
import glob
import eyed3
import logging
import pandas as pd
import tabulate

# Desativar avisos e mensagens de erro não críticas do eyed3
eyed3.log.setLevel(logging.ERROR)

def carregar_trilhas(diretorio):
    return glob.glob(os.path.join(diretorio, '*.mp3'))

def exibir_dataframe(trilhas):
    linhas = []
    for i in range(1, len(trilhas)+1):
        linhas.append(i)
    df = pd.DataFrame(columns=['Nome do Arquivo', 'Título', 'Tipo de Música', 'Autor', 'Intérprete', 'Classificação'], index=linhas)
    for i, trilha in enumerate(trilhas):
        mp3_file = eyed3.load(trilha)
        if mp3_file.tag is None:
            mp3_file.initTag(version=(2,4,0))

        df.loc[i+1,'Nome do Arquivo'] = os.path.splitext(os.path.basename(trilha))[0]
        df.loc[i+1,'Título'] = mp3_file.tag.title or "N/A"
        df.loc[i+1,'Tipo de Música'] = " | ".join([comment.text for comment in mp3_file.tag.comments]) if mp3_file.tag.comments else "N/A"
        df.loc[i+1,'Autor'] = mp3_file.tag.composer or "N/A"
        df.loc[i+1,'Intérprete'] = mp3_file.tag.artist or "N/A"
        df.loc[i+1,'Classificação'] = mp3_file.tag.genre.name if mp3_file.tag.genre else "N/A"
    print(tabulate.tabulate(df, headers='keys', tablefmt='psql'))

def alterar_metadados(trilha,trilhas_mp3,step):
    arq_mp3 = eyed3.load(trilha)
    if arq_mp3.tag is None:
        arq_mp3.initTag(version=(2,4,0))
    while True:
        step_2 = input('O que deseja alterar?\n1) Autor\n2) Interprete\n3) Classificação\n4) Salvar e Sair\n')
        if step == '1000':
            for i in range(0, len(trilhas_mp3)):
                arq_mp3_todos = eyed3.load(trilhas_mp3[i])
                nome_arq = os.path.splitext(os.path.basename(trilhas_mp3[i]))[0]
                nome_arq1 = nome_arq.split('-')
                arq_mp3_todos.tag.title = nome_arq1[0]
                arq_mp3_todos.tag.save()
        else:
            nome_arq = os.path.splitext(os.path.basename(trilha))[0]
            nome_arq1 = nome_arq.split('-')
            arq_mp3.tag.title = nome_arq1[0]
            arq_mp3.tag.save()
        if step_2 == '1' and step != '1000':
            arq_mp3.tag.composer = input('Digite o autor: ')
        
        elif step_2 == '2' and step != '1000':
            arq_mp3.tag.artist = input('Digite o intérprete: ')

        elif step_2 == '3':
            if step == '1000':
                classificacao = input('Digite a classificação (TA, TE, TM, ...) para todos os arquivos da pasta: ')
                for i in range(0, len(trilhas_mp3)):
                    arq_mp3 = eyed3.load(trilhas_mp3[i])
                    arq_mp3.tag.genre = classificacao
                    arq_mp3.tag.save()
                    
            else:
                arq_mp3.tag.genre = input('Digite a classificação (TA, TE, TM, ...): ')
        
        elif step_2 == '4':
            comentarios = 'Biblioteca Musical'
            arq_mp3.tag.comments.set(comentarios)
            arq_mp3.tag.save()
            break
    os.system('cls')
    print('\nMetadados alterados com sucesso (supostamente)')

def alterar_metadados_casa(trilhas):
    for i in range(0, len(trilhas)):
        arq_mp3 = eyed3.load(trilhas[i])
        if arq_mp3.tag is None:
            arq_mp3.initTag(version=(2,4,0))
        arq_mp3.tag.title = os.path.splitext(os.path.basename(trilhas[i]))[0]
        arq_mp3.tag.artist = 'Alberto Valério'
        arq_mp3.tag.composer = 'Alberto Valério'
        arq_mp3.tag.album_artist = 'Alberto Valério'
        arq_mp3.tag.comments.set('Trilha Musical')
        arq_mp3.tag.save()
    while True:
        exibir_dataframe(trilhas)
        step = input('\nDentre as trilhas a seguir, qual você deseja alterar a classificação (TA, TE, TM, ...)? ')
        if step.isdigit() and (0 <= int(step) <= len(trilhas)):
            arq_mp3 = eyed3.load(trilhas[int(step)-1])
            print(f'\nVocê escolheu a trilha {step}: {os.path.splitext(os.path.basename(trilhas[int(step)-1]))[0]}')
            arq_mp3.tag.genre = input('Digite a classificação das trilhas (TA, TE, TM, ...): ')
            arq_mp3.tag.save()
            break
        else:
            print('Por favor, insira um número válido')
    print('\nMetadados alterados com sucesso (supostamente)')


def main():
    origem_arq = input("O(s) arquivo(s) .mp3 que deseja ler são de autoria da Câmara dos Deputados? \n1) Sim\n2) Não\n")
    while origem_arq not in ("1", "2"):
        origem_arq = input("Por favor, insira 1 ou 2: ")

    os.system('cls')

    if origem_arq == '2':
        diretorio = r"C:\Users\p_702811\Desktop\TODAS TRILHAS\Trilhas editadas\Faixas formatadas"
    else:
        diretorio = r"C:\Users\p_702811\Desktop\TODAS TRILHAS\Trilhas editadas\Programas da casa"

    trilhas_mp3 = carregar_trilhas(diretorio)
    while True:
        next_step = input('\nO que deseja fazer a seguir?\n1) Ler metadados do arquivo\n2) Alterar metadados de arquivo\n3) Finalizar\n')
        os.system('cls')
        if origem_arq == '1' and next_step == '2':
            alterar_metadados_casa(trilhas_mp3)
        elif origem_arq == '1' and next_step == '1':
            exibir_dataframe(trilhas_mp3)
        else:
            if next_step == '3':
                break
            
            if next_step == '1':
                print('Os arquivos .mp3 presentes na pasta são:\n')
                exibir_dataframe(trilhas_mp3)

            elif next_step == '2':
                while True:
                    exibir_dataframe(trilhas_mp3)
                    step = input('\nDentre as trilhas a seguir, qual você deseja alterar? ')
                    if step.isdigit() and (0 <= int(step) <= len(trilhas_mp3) or step == '1000'):
                        if step == '1000':
                            print('Você escolheu todas as trilhas')
                            alterar_metadados(trilhas_mp3[0], trilhas_mp3,step)
                        else:
                            print(f'\nVocê escolheu a trilha {step}: {os.path.splitext(os.path.basename(trilhas_mp3[int(step)-1]))[0]}')
                            alterar_metadados(trilhas_mp3[int(step)-1], trilhas_mp3,step)
                        break
                    else:
                        print('Por favor, insira um número válido')
if __name__ == "__main__":
    main()