import io
import os
import PySimpleGUI as sg
from PIL import Image

def main():
    layout = [
        #Na biblioteca que gria janelas, eu quero que crie um picturebox com a ID "-IMAGE-". Este primeiro array é a primeira linha
        #como se fosse a primeira div
        [sg.Image(key="-IMAGE-", size=(500, 500))],
        #Segunda div
        [
            sg.Text("Arquivo de Imagem"),
            sg.Input(size=(25,1), key="-FILE-"),
            #Faz a seleção do arquivo. O último item é o filtro real dos arquivos
            sg.FileBrowse(file_types=[("JPEG (*.jpg)", "*jpg"), ("Todos os arquivos", "*.*")]),
            sg.Button("Carregar imagem")
        ]
    ]

    #Cria a janela com o layout que fizemos
    window = sg.Window("Visualizador de Imagem", layout=layout)

    while True:
        event, value = window.read()

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

                #Muda o tamanha da div imagem pelo 
                window["-IMAGE-"].update(data=bio.getvalue(), size=(500, 500))

        window.close()


if __name__ == "__main__":
    main()
