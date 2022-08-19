from pickletools import optimize
from PIL import Image

#Pega a imagem pizza no arquivo e abre ela 
#imagem = Image.open('pizza.png')
#imagem.show("Pizza")

#Pega uma imagem jpg e salva como png
def image_converter(input_file, output_file, format):
    imagem = Image.open(input_file)
    #O arquivo png que irá ser salvo deve ser mais pesado que o jpg para ser validado corretamente
    #Coloca o format para garantir que independente do nome, eu quero sempre que salve no formato PNG
    #em quality 1 é a pior qualidade de imagem para quando otimizar poder mandar facilmente para qualquer lugar. Porém se salvar em 75 ela 
    #mantém a qualidade e reduz o tamanho drasticamente
    imagem.save(output_file, format=format, optimize=True, quality=75)
    
    #Altera a largura e a altura para reduzir mais ainda o tamanho do arquivo
    imagem.thumbnail((75, 75))
    imagem.save("thumbnail.jpg")


#Para melhor validação, pegamos a imagem e vemos o formato para ver se está correto
def image_format(input_file):
    image = Image.open(input_file)
    print(f"Formato: {image.format_description}")



#É como se fosse o void main do C. É algo que deve ser decorado
if __name__ == "__main__":
   #image_converter("pizza2.jpg", "pizza2.gif", "PNG")
   #image_converter("pizza2.jpg", "pizza2.hso", "PNG")

   image_converter("sushi.jpg", "damedane.png", "png")

   #image_format("pizza2.jpg")
   #image_format("pizza2.gif")
   #image_format("pizza2.hso")
   #image_format("pizza.jpg")