from PIL import Image
import numpy as np

def carregar_rota():
    """Carrega as posições da rota do arquivo resultado."""
    posicoes = []
    with open("rota_resultado.txt", "r") as f:
        for linha in f:
            if linha.startswith("Passo"):
                # Extrai a posição da linha "Passo X: (i, j)"
                pos_str = linha.split(": ")[1].strip()
                pos = eval(pos_str)  # Converte a string "(i, j)" em tupla
                posicoes.append(pos)
    return posicoes

def criar_imagem_destacada():
    """Cria uma nova imagem com as posições da rota destacadas em verde claro."""
    # Carrega a imagem original e converte para RGB
    imagem_original = Image.open("image2.png").convert('RGB')
    imagem_array = np.array(imagem_original)
    
    # Carrega as posições da rota
    posicoes_rota = carregar_rota()
    
    # Define a cor verde claro (RGB)
    VERDE_CLARO = np.array([144, 238, 144])
    
    # Obtém as dimensões da grade
    altura, largura = imagem_array.shape[:2]
    tamanho_quadrado_y = altura // 42
    tamanho_quadrado_x = largura // 42
    
    # Cria uma cópia da imagem original
    nova_imagem = imagem_array.copy()
    
    # Pinta cada posição da rota de verde claro
    for i, j in posicoes_rota:
        y_inicio = i * tamanho_quadrado_y
        y_fim = (y_inicio + tamanho_quadrado_y) if i < 41 else altura
        x_inicio = j * tamanho_quadrado_x
        x_fim = (x_inicio + tamanho_quadrado_x) if j < 41 else largura
        
        # Pinta o quadrado inteiro da posição (i,j) de verde claro
        nova_imagem[y_inicio:y_fim, x_inicio:x_fim] = VERDE_CLARO
    
    # Converte o array numpy de volta para uma imagem PIL
    imagem_final = Image.fromarray(nova_imagem)
    
    # Salva a nova imagem
    imagem_final.save("image_highlighted.png")
    print("Nova imagem criada com sucesso: image_highlighted.png")

if __name__ == "__main__":
    criar_imagem_destacada()
