from PIL import Image
import numpy as np
import colorsys

def carregar_imagem(caminho_imagem):
    """Carrega a imagem e a converte para um array numpy em RGB."""
    imagem = Image.open(caminho_imagem).convert('RGB')
    return np.array(imagem)

def dividir_em_quadrados(imagem, linhas, colunas):
    """Divide a imagem em uma grade de quadrados iguais."""
    altura, largura, _ = imagem.shape
    tamanho_quadrado_y = altura // linhas
    tamanho_quadrado_x = largura // colunas
    quadrados = []

    for i in range(linhas):
        for j in range(colunas):
            y_inicio = i * tamanho_quadrado_y
            y_fim = (y_inicio + tamanho_quadrado_y) if i < linhas - 1 else altura
            x_inicio = j * tamanho_quadrado_x
            x_fim = (x_inicio + tamanho_quadrado_x) if j < colunas - 1 else largura

            quadrado = imagem[y_inicio:y_fim, x_inicio:x_fim]
            quadrados.append((i, j, quadrado))
    return quadrados

def classificar_cor(rgb):
    """Classifica a cor em uma das 5 categorias pré-definidas usando HSV."""
    r, g, b = rgb
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    h *= 360
    s *= 100
    v *= 100

    # Limiares para classificação
    LIMIAR_SATURACAO = 15  # Cores abaixo são consideradas cinza
    LIMIAR_VALOR_CLARO = 70  # Valor para diferenciar cinza claro/escuro
    LIMIAR_VALOR_ESCURO = 40  # Valor para diferenciar cinza escuro

    # Classificação de cores
    if s < LIMIAR_SATURACAO:
        if v > LIMIAR_VALOR_CLARO:
            return (166, 166, 166)  # Cinza claro
        elif v > LIMIAR_VALOR_ESCURO:
            return (128, 128, 128)  # Cinza médio
        else:
            return (64, 64, 64)     # Cinza escuro
    else:
        if (h < 15 or h >= 345):  # Vermelho
            return (255, 0, 0)
        elif 15 <= h < 45:  # Laranja
            return (255, 165, 0)
        elif 200 <= h < 270:  # Azul
            return (0, 0, 255)
        else:  # Cor não mapeada (default para cinza médio)
            return (128, 128, 128)

def cor_predominante(quadrado):
    """Calcula a cor predominante e aplica a classificação."""
    avg_color = np.mean(quadrado, axis=(0, 1)).astype(int)
    return classificar_cor(tuple(avg_color))

def processar_imagem(caminho_imagem, linhas=42, colunas=42):
    """Processa a imagem e retorna as posições com cores categorizadas."""
    imagem = carregar_imagem(caminho_imagem)
    quadrados = dividir_em_quadrados(imagem, linhas, colunas)
    resultados = []

    for i, j, quadrado in quadrados:
        cor = cor_predominante(quadrado)
        resultados.append(((i, j), cor))
    
    return resultados

def rgb_to_color_name(rgb):
    """Converte valores RGB para o nome da cor correspondente."""
    r, g, b = rgb
    if rgb == (255, 0, 0):
        return "Vermelho"
    elif rgb == (255, 165, 0):
        return "Laranja"
    elif rgb == (0, 0, 255):
        return "Azul"
    elif rgb in [(166, 166, 166), (128, 128, 128)]:
        return "Cinza"
    elif rgb == (64, 64, 64):
        return "Cinza Escuro"
    else:
        return "Desconhecida"

# Exemplo de uso
caminho_imagem = "image2.png"
resultados = processar_imagem(caminho_imagem)

# Exibir resultados
for posicao, cor in resultados:
    print(f"Posicao: {posicao}, Cor: {rgb_to_color_name(cor)}")



# Salvar resultados em arquivo
with open("resultado.txt", "w") as file:
    for posicao, cor in resultados:
        file.write(f"Posicao: {posicao}, Cor: {rgb_to_color_name(cor)}\n") 



print("--------------------------------")
posicao_desejada = (35, 7)
for posicao, cor in resultados:
    if posicao == posicao_desejada:
        print(f"Posição {posicao_desejada}:")
        print(f"Cor RGB: {cor}")
        print(f"Nome da cor: {rgb_to_color_name(cor)}")
        break