from PIL import Image
from PIL import ImageColor

def cria_imagem(fileName, size):
    imagem = Image.new("RGBA", size)
    cor1 = ImageColor.getcolor("white", "RGBA")
    cor2 = ImageColor.getcolor("black", "RGBA")
    cor = cor1
    count = 0

    for y in range(size[1]):
        for x in range(size[0]):
            if count == 3:
                cor = cor1 if cor == cor2 else cor2
                count = 0
            imagem.putpixel((x,y), cor)
            count += 1

    imagem.save(fileName)


if __name__ == "__main__":
    cria_imagem("imagem.png", (100,100))

