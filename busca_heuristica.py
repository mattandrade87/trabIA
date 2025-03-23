from grid_color import processar_imagem, rgb_to_color_name
from heapq import heappush, heappop
import math

# Posições dos personagens
posicaoDustin = (5,7)
posicaoEleven = (6,40)
posicaoMike = (17,37)
posicaoLucas = (20,10)
posicaoWill = (30, 11)
posicaoSaida = (41,40)

# Custo de cada tipo de terreno
CUSTOS = {
    "Cinza": 1,
    "Azul": 3,
    "Vermelho": 6,
    "Laranja": 4,
    "Cinza Escuro": 10000,
    "Desconhecida": 10000
}

def manhattan_distance(p1, p2):
    """Calcula a distância de Manhattan entre dois pontos."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def get_neighbors(pos, grid_size):
    """Retorna os vizinhos válidos de uma posição."""
    x, y = pos
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Movimentos: direita, baixo, esquerda, cima
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < grid_size[0] and 0 <= new_y < grid_size[1]:
            neighbors.append((new_x, new_y))
    return neighbors

def get_cost(pos, resultados):
    """Retorna o custo de uma posição baseado na cor do terreno."""
    for (i, j), cor in resultados:
        if (i, j) == pos:
            return CUSTOS[rgb_to_color_name(cor)]
    return 10000  # Custo alto para posições inválidas

def a_star(start, goal, resultados, grid_size):
    """Implementa o algoritmo A* para encontrar o caminho mais curto entre dois pontos."""
    frontier = [(0, start, [start])]
    heappush(frontier, (0, start, [start]))
    visited = set()
    costs = {start: 0}
    
    while frontier:
        _, current, path = heappop(frontier)
        
        if current == goal:
            return path, costs[current]
            
        if current in visited:
            continue
            
        visited.add(current)
        
        for next_pos in get_neighbors(current, grid_size):
            if next_pos in visited:
                continue
                
            new_cost = costs[current] + get_cost(next_pos, resultados)
            
            if next_pos not in costs or new_cost < costs[next_pos]:
                costs[next_pos] = new_cost
                priority = new_cost + manhattan_distance(next_pos, goal)
                heappush(frontier, (priority, next_pos, path + [next_pos]))
    
    return None, float('inf')

def encontrar_melhor_rota():
    """Encontra a melhor rota para coletar todos os personagens e chegar à saída."""
    resultados = processar_imagem("image2.png")
    grid_size = (42, 42)  # Tamanho da grade

    # Lista de pontos a visitar (somente os personagens)
    pontos_personagens = [posicaoMike, posicaoLucas, posicaoDustin, posicaoWill]
    
    # Posição inicial (posição da Eleven)
    posicao_atual = posicaoEleven
    rota_completa = [posicao_atual]
    custo_total = 0
    
    # Encontra o melhor caminho para cada personagem
    while pontos_personagens:
        melhor_caminho = None
        melhor_custo = float('inf')
        melhor_ponto = None
        
        # Testa cada ponto restante para encontrar o melhor próximo destino
        for ponto in pontos_personagens:
            caminho, custo = a_star(posicao_atual, ponto, resultados, grid_size)
            if caminho and custo < melhor_custo:
                melhor_caminho = caminho
                melhor_custo = custo
                melhor_ponto = ponto
        
        if melhor_caminho:
            # Adiciona o caminho à rota (exceto a posição inicial que já está incluída)
            rota_completa.extend(melhor_caminho[1:])
            custo_total += melhor_custo
            posicao_atual = melhor_ponto
            pontos_personagens.remove(melhor_ponto)
        else:
            break

    # Após coletar todos os personagens, adiciona o caminho até a saída
    caminho_saida, custo_saida = a_star(posicao_atual, posicaoSaida, resultados, grid_size)
    if caminho_saida:
        rota_completa.extend(caminho_saida[1:])
        custo_total += custo_saida

    return rota_completa, custo_total

def main():
    rota, custo_total = encontrar_melhor_rota()
    
    # Imprime os resultados
    print("\nRota completa:")
    for i, pos in enumerate(rota):
        print(f"Passo {i}: {pos}")
    
    print(f"\nCusto total: {custo_total}")
    
    # Salva os resultados em um arquivo
    with open("rota_resultado.txt", "w") as f:
        f.write("Rota completa:\n")
        for i, pos in enumerate(rota):
            f.write(f"Passo {i}: {pos}\n")
        f.write(f"\nCusto total: {custo_total}")

if __name__ == "__main__":
    main()



