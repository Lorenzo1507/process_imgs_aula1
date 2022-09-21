from fileinput import filename
import io
import os
from pickletools import optimize
import requests
import PySimpleGUI as sg
from PIL import Image
from PIL import ImageFilter

def cria_thumbnail(filename):
    if os.path.exists(filename):
        imagem = Image.open(filename)
        imagem.thumbnail((75,75))
        imagem.save('thumbnail.png', format="PNG", optimize=True)    
    else:
        imagem = requests.get(filename)
        imagem = Image.open(io.BytesIO(imagem.content))
        imagem.thumbnail((75,75))
        imagem.save("thumb_web.png", format="PNG", optimize=True)

def mostrar_imagem(imagem, window):
    imagem.thumbnail((500,500))
    bio = io.BytesIO()
    imagem.save(bio, format="PNG")
    window["-IMAGE-"].draw_image(data=bio.getvalue(), location=(0,400))

def carrega_imagem(filename, window):
    if os.path.exists(filename):
        imagem = Image.open(filename)
        mostrar_imagem(imagem, window)

def reduzir_qualidade(filename, qualidade):
    if os.path.exists(filename):
        imagem = Image.open(filename)
        imagem.save("baixa_qualidade.jpg", format="JPEG", optimize=True, quality=int(qualidade))

    else:
        imagem = requests.get(filename)
        imagem = Image.open(io.BytesIO(imagem.content))
        imagem.save("baixa_qualidade_web.jpg", format="JPEG", optimize=True, quality= int(qualidade))

def abre_url(url, window):
    imagem = requests.get(url)
    imagem = Image.open(io.BytesIO(imagem.content))
    mostrar_imagem(imagem, window) 

def salvar_url(url, nomeSave):
    imagem = requests.get(url)
    imagem = Image.open(io.BytesIO(imagem.content))
    imagem.save(nomeSave + "_web.png", format="PNG", optimize=True)


def salvar_img(filename, nomeSave, formato):
    if formato == "jpeg":
        imageType = "jpg"
        imagem = Image.open(filename)

        if os.path.exists(filename):
            #imagePathList = filename.split("/")
            #imagePathList[len(imagePathList)-1] = imagePathList[len(imagePathList)-1].replace(".jpg", "."+imageType)
            #ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
            #ROOT_DIR += "/" + imagePathList[len(imagePathList)-1]

            nomeSave += "."+imageType

            imagem.save(nomeSave, format=formato)
            print(nomeSave)
            print("Salvo") 
        else:
            salvar_url(filename, nomeSave)

    else:
        if os.path.exists(filename):
            imagem = Image.open(filename)
            
            nomeSave += "." + formato

            imagem.save(nomeSave, format=formato)
            print(nomeSave)
            print("Salvo") 
            
        else:
            salvar_url(filename, nomeSave)

def main():
    menu_def=[
        ['File', ['Save', ['Gerar thumbnail', 'Salvar atual', 'Salvar com qualidade',['Muito baixa', 'Baixa', 'Média', 'Original'],
        'Formato da Imagem', ['Salvar como png', 'Salvar como jpg']], 'Exit']],
        ['Edit', ['Filtros', ['sepia', 'preto e branco', 'cores'],
        'Polir', ['Blur', 'Box Blur', 'Contour', 'Detail', 'Edge Enhance', 'Emboss', 'Find Edges', 'Gaussian blur', 'Sharpen', 'Smooth'], 
        'Crop','Desfazer']],
        ['Informações']
    ]
    
    layout = [
        [sg.Menu(menu_def, background_color='lightsteelblue',text_color='navy', font='Verdana', pad=(10,10))],
       
        [sg.Graph(key="-IMAGE-", canvas_size=(500,500), graph_bottom_left=(0, 0), graph_top_right=(400, 400), change_submits=True, drag_submits=True)],
        [
            sg.Text("Arquivo ou URL da Imagem:"),
            sg.Input(size=(25,1), key="-FILE-"),
            sg.FileBrowse(file_types=[("JPEG (*.jpg)", "*.jpg"), ("Todos os arquivos", "*.*")]),
            sg.Button("Carregar Imagem")
        ]
    ]
        
    window = sg.Window("Visualizador de Imagem", layout=layout)
    dragging = False
    ponto_inicial = ponto_final = retangulo = None

    while True:
        event, value = window.read()
        if event == "Exit" or event == sg.WINDOW_CLOSED:
            break

        if event == "-IMAGE-":
            x, y = value["-IMAGE-"]
            if not dragging:
                ponto_inicial = (x, y)
                print("Inicio: xi:", x ,"yi: ", y)
                dragging = True
            else:
                ponto_final = (x, y)
                print("Fim: xf:", x ,"yf: ", y)
            if retangulo:
                window["-IMAGE-"].delete_figure(retangulo)
            if None not in (ponto_inicial, ponto_final):
                retangulo = window["-IMAGE-"].draw_rectangle(ponto_inicial, ponto_final, line_color='red')

        elif event.endswith('+UP'):
            dragging = False


        filename = value["-FILE-"]

        #print(event)

        if event == 'Gerar thumbnail':
            cria_thumbnail(filename)

        if event == "Carregar Imagem":

           if os.path.exists(filename):
                carrega_imagem(filename, window) 

           else:
                abre_url(filename, window)

        if event == 'Muito baixa':
            reduzir_qualidade(filename, 1)
        if event == 'Baixa':
             reduzir_qualidade(filename, 25)
        if event == 'Média':
             reduzir_qualidade(filename, 50)
        if event == 'Original':
             nomeImagem = sg.popup_get_text('Digite o nome do arquivo', keep_on_top=True)
             formato = "jpeg"
             salvar_img(filename, nomeImagem,formato)
        

        if event == 'Salvar como png':
            nomeImagem = sg.popup_get_text('Digite o nome do arquivo', keep_on_top=True)
            formato = "png"
            salvar_img(filename, nomeImagem,formato)

        if event == 'Salvar como jpg':
            nomeImagem = sg.popup_get_text('Digite o nome do arquivo', keep_on_top=True)
            formato = "png"
            salvar_img(filename, nomeImagem,formato)

        if event == 'Salvar atual':
            nomeImagem = sg.popup_get_text('Digite o nome do arquivo com o formato (ex: pizza.png)', keep_on_top=True)
            #condition.save(nomeImagem)
            
       
        if event == 'sepia':
            converte_sepia(filename, "pizza_sepia.png", window)
        
        if event == 'preto e branco':
            muda_para_cinza(filename, "pizza_cinza.jpg", window)

        #'Blur', 'Box Blur', 'Contour', 'Detail', 'Edge Enhance', 'Emboss', 'Find Edges', 'Gaussian blur', 'Sharpen', "Smooth"
        if event == 'Blur':
            #image_blur("blur.png","blur1.png", window)
            image_blur(filename,"blur1.png", window)
        
        if event == 'Box Blur':
            #image_boxblur("blur.png", "blur2.png", window)
            image_boxblur(filename, "blur2.png", window)
        
        if event == 'Contour':
            #image_contour("hand.jpg", "hand_contour.jpg", window)
            image_contour(filename, "hand_contour.jpg", window)
        
        if event == 'Detail':
            #image_detail("detail.png", "detail1.png", window)
            image_detail(filename, "detail1.png", window)
        
        if event == 'Edge Enhance':
            #image_edge_enhance("raiox.jpg", "raiox1.jpg", window)
            image_edge_enhance(filename, "raiox1.jpg", window)

        if event == 'Emboss':
            #image_emboss("emboss.jpg", "emboss2.jpg", window)
            image_emboss(filename, "emboss2.jpg", window)

        if event == 'Find Edges':
            #image_find_edges("emboss.jpg", "emboss1.jpg", window)
            image_find_edges(filename, "emboss1.jpg", window)

        if event == 'Gaussian blur':
            #image_gaussian_blur("blur.png", "blur3.png", window)
            image_gaussian_blur(filename, "blur3.png", window)

        if event == 'Sharpen':
            #image_sharpen("sharpen.jpg", "sharpen1.jpg", window)
            image_sharpen(filename, "sharpen1.jpg", window)

        if event == 'Smooth':
            #image_smooth("sharpen1.jpg", "sharpen2.jpg", window)
            image_smooth(filename, "sharpen2.jpg", window)

        if event == 'Crop':
            #(xi, yi) = ponto_inicial
            #(xf, yf) = ponto_final

            crop_image(filename,
              (203, 96, 294, 268), # Left, Upper, Right, Lower
              "raiox_cropped.jpg")

            
            

    window.close()

def calcula_paleta(branco):
    paleta = []
    r,g,b = branco
    
    for i in range(255):
        new_red = r * i // 255
        new_green = g * i // 255
        new_blue = b * i // 255
        paleta.extend((new_red, new_green, new_blue))
    return paleta

def converte_sepia(input, output, window):
    branco = (255, 240, 192)
    paleta = calcula_paleta(branco)

    imagem = Image.open(input)
    imagem = imagem.convert("L")
    imagem.putpalette(paleta)

    sepia = imagem.convert("RGB")

    mostrar_imagem(sepia, window)
    return sepia
    #sepia.save(output)

def muda_para_cinza(imagem_entrada, imagem_saida, window):
    imagem = Image.open(imagem_entrada)
    #LUMA é um padrão de converção para a escala de cinza, por isso usa "L"
    #Para outras escalas apenas usa o convert usando "1" (entre aspas mesmo)
    #CYMK para imagens RGBA
    imagem = imagem.convert("L")
    mostrar_imagem(imagem, window)

    return imagem
    #imagem.save(imagem_saida)


def image_blur(input_image, output_image, window):
    image = Image.open(input_image)
    filtered_image = image.filter(ImageFilter.BLUR)

    mostrar_imagem(filtered_image, window)
    #filtered_image.save(output_image)


def image_boxblur(input_image, output_image, window):
    image = Image.open(input_image)
    filtered_image = image.filter(ImageFilter.BoxBlur(radius=3))
    
    mostrar_imagem(filtered_image, window)
    #filtered_image.save(output_image)


def image_contour(input_image, output_image, window):
    image = Image.open(input_image)
    filtered_image = image.filter(ImageFilter.CONTOUR)
    
    mostrar_imagem(filtered_image, window)
    #filtered_image.save(output_image)


def image_detail(input_image, output_image, window):
    image = Image.open(input_image)
    filtered_image = image.filter(ImageFilter.DETAIL)
    
    mostrar_imagem(filtered_image, window)
    #filtered_image.save(output_image)


def image_edge_enhance(input_image, output_image, window):
    image = Image.open(input_image)
    filtered_image = image.filter(ImageFilter.EDGE_ENHANCE)
   
    mostrar_imagem(filtered_image, window)
    #filtered_image.save(output_image)


def image_emboss(input_image, output_image, window):
    image = Image.open(input_image)
    filtered_image = image.filter(ImageFilter.EMBOSS)
   
    mostrar_imagem(filtered_image, window)
    #filtered_image.save(output_image)


def image_find_edges(input_image, output_image, window):
    image = Image.open(input_image)
    filtered_image = image.filter(ImageFilter.FIND_EDGES)
    
    mostrar_imagem(filtered_image, window)
    #filtered_image.save(output_image)


def image_gaussian_blur(input_image, output_image, window):
    image = Image.open(input_image)
    filtered_image = image.filter(ImageFilter.GaussianBlur)
    
    mostrar_imagem(filtered_image, window)
    #filtered_image.save(output_image)


def image_sharpen(input_image, output_image, window):
    image = Image.open(input_image)
    filtered_image = image.filter(ImageFilter.SHARPEN)
    
    mostrar_imagem(filtered_image, window)
    #filtered_image.save(output_image)


def image_smooth(input_image, output_image, window):
    image = Image.open(input_image)
    filtered_image = image.filter(ImageFilter.SMOOTH)
    
    mostrar_imagem(filtered_image, window)
    #filtered_image.save(output_image)

def mirror(image_path, output_image_path):
    image = Image.open(image_path)
    mirror_image = image.transpose(Image.FLIP_TOP_BOTTOM) #FLIP_LEFT_RIGHT, FLIP_TOP_BOTTOM, TRANSPOSE
    mirror_image.save(output_image_path)
    #mirror("raiox.jpg", "raiox_mirrored.jpg")


def crop_image(image_path, coords, output_image_path):
    image = Image.open(image_path)
    cropped_image = image.crop(coords)
    cropped_image.save(output_image_path)
    # crop_image("raiox.jpg",
              # (140, 61, 328, 383), # Left, Upper, Right, Lower
              # "raiox_cropped.jpg")

def resize(input_image_path, output_image_path, size):
    image = Image.open(input_image_path)
    resized_image = image.resize(size)
    resized_image.save(output_image_path)
    #resize("raiox.jpg", "raiox_resized.jpg", (100,300))

def rotate(image_path, degrees_to_rotate, output_image_path):
    image_obj = Image.open(image_path)
    rotated_image = image_obj.rotate(degrees_to_rotate)
    rotated_image.save(output_image_path)
    #rotate("raiox.jpg", 45, "raiox_rotated.jpg")






if __name__ == "__main__":
    main()