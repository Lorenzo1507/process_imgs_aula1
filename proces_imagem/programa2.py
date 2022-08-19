import io
import os
import PySimpleGUI as sg
import urllib.request
import cv2
import numpy as np
from PIL import Image

def main():
    layout = [
        #Na biblioteca que gria janelas, eu quero que crie um picturebox com a ID "-IMAGE-". Este primeiro array é a primeira linha
        #como se fosse a primeira div, a imagem será inserida aqui
        [sg.Image(key="-IMAGE-", size=(500, 500))],
        [
           sg.Text("Pegar imagem através do link:"), 
           sg.Input(size=(25,1), key="-URL-"),
           sg.Button("Carregar imagem da internet")
        ],
        #Segunda div
        [
            sg.Text("Arquivo de Imagem"),
            sg.Input(size=(25,1), key="-FILE-"),
            #Faz a seleção do arquivo. O último item é o filtro real dos arquivos
            sg.FileBrowse(file_types=[("JPEG (*.jpg)", "*jpg"), ("Todos os arquivos", "*.*")]),
            sg.Button("Carregar imagem"),
            sg.Button("Salvar thumbnail"),
            sg.Button("Salvar qualidade reduzida"),
        ],
        [
            sg.Text("Formato da Imagem"),
            sg.Combo(["png", "jpeg"], key="-COMBO-"),
            sg.Button("Salvar imagem")

        ]
    ]

    #Cria a janela com o layout que fizemos
    window = sg.Window("Visualizador de Imagem", layout=layout)

    while True:
        event, value = window.read()
        print(event)
        print(value)

        #Se executar função sair ou fechar a janela.
        if event =="Exit" or event == sg.WINDOW_CLOSED:
            break

        if event =="Carregar imagem":
            filename = value["-FILE-"]

            #Se o arquivo existir
            if os.path.exists(filename):
                image = Image.open(filename)
                image.thumbnail((500, 500))

                bio = io.BytesIO()
                image.save(bio, format="PNG")

                #Muda o tamanho da div imagem pelo tamanho que for a imagem
                window["-IMAGE-"].update(data=bio.getvalue(), size=(500, 500))
                

        comboItem = value["-COMBO-"]

        if event == "Salvar imagem" and comboItem != '':
            filePath = value["-FILE-"]

            imagem = Image.open(filePath)

            imagePathList = filename.split("/")

            imagePathList[len(imagePathList)-1] = imagePathList[len(imagePathList)-1].replace(".jpg", "."+comboItem)

            imageNewPath  = '/'.join(imagePathList)

            imagem.save(imageNewPath, format=comboItem)
            print(imageNewPath)
            print("Salvo")

                
        if event == "Salvar thumbnail":
            filePath = value["-FILE-"]

            imagem = Image.open(filePath)

            imagePathList = filename.split("/")

            filename = imagePathList[len(imagePathList)-1]
            #remove o ultimo item da lista, que no caso é o nome do arquivo
            imagePathList.pop()
            
            imagePathList.append("thumbnail_"+filename)

            imageNewPath  = '/'.join(imagePathList)

            print(imageNewPath)

            imagem.thumbnail((75, 75))

            imagem.save(imageNewPath)
            print("Thumbnail salvo")


        if event == "Salvar qualidade reduzida" and comboItem == 'jpeg':
            filePath = value["-FILE-"]

            imagem = Image.open(filePath)

            imagePathList = filename.split("/")

            filename = imagePathList[len(imagePathList)-1]

            #remove o ultimo item da lista, que no caso é o nome do arquivo
            imagePathList.pop()
            
            imagePathList.append("lowRes_"+filename)

            imageNewPath  = '/'.join(imagePathList)

            imagem.save(imageNewPath, quality=1)

            print(imageNewPath)
            print("Imagem de baixa resolução salva")


        if event == "Carregar imagem da internet":
            #Pega a url digitada no input e a abre em uma variável o retorno da request
            url = value["-URL-"]
            url_reponse = urllib.request.urlopen(url)

            #Convertemos a resposta em bytearray para armazenarmos pordemos armazenar em um array
            img_array = np.array(bytearray(url_reponse.read()), dtype=np.uint8)

            #Está parte faz o decode da imagem. Atribui o array a ser decodificado e a cor da imagem
            #1 mantém a cor padrão da imagem
            img = cv2.imdecode(img_array, 1)
            #img = cv2.imdecode(img_array, cv2.IMREAD_GREYSCALE) # deixa a imagem preto e branco

            cv2.imshow('URL Image', img)

            #Muda o tamanho da div imagem pelo tamanho que for a imagem
            window["-IMAGE-"].update(data=bio.getvalue(), size=(500, 500))
            
            #esperará por tempo especificado
            cv2.waitKey()
                
    
    window.close()


if __name__ == "__main__":
    main()
