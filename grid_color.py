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
    LIMIAR_SATURACAO = 20  # Cores abaixo são consideradas cinza
    LIMIAR_VALOR_CLARO = 90  # Valor para diferenciar cinza claro/escuro

    # Classificação de cores
    if s < LIMIAR_SATURACAO:
        if v > LIMIAR_VALOR_CLARO:
            return (211, 211, 211)  # Cinza claro
        else:
            return (128, 128, 128)  # Cinza médio/escuro
    else:
        if (h < 15 or h >= 345):  # Vermelho
            return (255, 0, 0)
        elif 15 <= h < 45:  # Laranja
            return (255, 165, 0)
        elif 200 <= h < 270:  # Azul
            return (0, 0, 255)
        else:  # Cor não mapeada (default para cinza)
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

# Exemplo de uso
caminho_imagem = "image2.png"
resultados = processar_imagem(caminho_imagem)

# Exibir resultados
for posicao, cor in resultados:
    print(f"Posição [i, j]: {posicao}, Cor categorizada: {cor}")


with open("resultado.txt", "w") as file:
    for item in resultados:
        file.write(str(item) + "\n") 