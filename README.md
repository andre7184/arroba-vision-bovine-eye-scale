# 🐂 Arroba Vision: Bovine Eye-Scale (Estimativa de Peso por Visão Computacional)

## Visão Geral do Projeto

O **Arroba Vision** é uma prova de conceito (PoC) que utiliza Inteligência Artificial (Visão Computacional) para estimar o peso e a faixa etária do gado (inicialmente da raça Nelore) a partir de uma única foto lateral.

O projeto resolve o problema da medição de área em 2D de forma inovadora: em vez de usar uma régua fixa, ele usa a geometria estável do animal como referência de escala.

O cálculo central é baseado na **Proporção da Área do Torso em Pixels vs. a Área do Olho em Pixels**, aproveitando o princípio biológico de que o diâmetro do globo ocular cresce muito mais lentamente do que o corpo do animal, tornando o olho a nossa "régua" de pixels.

### Status do Projeto

A lógica *backend* (o algoritmo de cálculo) e o *frontend* (aplicação web) estão completos. A funcionalidade depende da finalização do treinamento do Modelo v4 (Estimação de Pose).

---

## 💻 Tecnologias Utilizadas (O Stack)

| Componente | Tecnologia | Função no Projeto |
| :--- | :--- | :--- |
| **Backend Principal** | **Python** (Django) | Estrutura web, manipulação de arquivos, chamadas de API. |
| **IA/Visão Computacional** | **Roboflow API** | Hospedagem, *deployment* e inferência (uso) do modelo treinado. |
| **Arquitetura de IA** | **YOLOv8-Pose** (ou similar) | Modelo treinado para **Estimação de Pose** (Keypoint Detection). |
| **Comunicação** | **`requests` (Python)** | Faz a chamada para a API do Roboflow e recebe o JSON das predições. |
| **Lógica de Cálculo** | **Python (analysis_utils)** | Processa os pontos Keypoints (X, Y) para calcular a área, altura e proporção. |
| **Frontend** | **Django Templates (HTML/CSS)** | Interface de usuário simples para upload e visualização de resultados. |

---

## 🧠 Conceitos de Visão Computacional e Matemática Aplicada

O valor técnico deste projeto reside na forma como a IA e a matemática são combinadas:

### 1. Modelo de Estimação de Pose (Keypoint Detection)

* **Tarefa:** Substituir a imprecisão da "Área do Retângulo" pela precisão da "Estrutura Geométrica".
* **Anotação:** O modelo foi treinado com **10 Pontos Chave (Keypoints)** em cada animal, definindo:
    * **Régua:** Ponto do Olho.
    * **Dimensões:** Pontos no Cupim, Cascos, Ombros e Focinho.
* **Vantagem:** Permite calcular a **Altura Total** e a **Área do Torso** (em pixels) de forma consistente, eliminando a distorção da perspectiva 2D.

### 2. O Algoritmo de Proporção (Area-Ratio Scale)

O cálculo central é baseado em uma Proporção (`R`), que é a medida primária do animal.

$$\large R = \frac{\text{Área do Torso (Pixels)}}{\text{Área do Olho (Pixels)}}$$

* **Área do Torso:** Calculada no código Python (TASK-19) usando a **Fórmula de Shoelace** sobre os Keypoints do torso (para obter a área exata do polígono, sem incluir o ar e o pasto).
* **Escala Biológica:** O Olho é a régua. Como o olho cresce lentamente, o valor de $R$ se torna um indicador direto da idade e do tamanho do animal.

### 3. Estimativa de Idade e Peso (Alometria)

O projeto utiliza o princípio da **Alometria** (crescimento desigual de partes do corpo) para classificar o animal e estimar o peso:

* Se $R \le R_{\text{Bezerro Max}}$: O animal é classificado como **Bezerro** e usa o $K_{\text{bezerro}}$.
* Se $R \ge R_{\text{Adulto Min}}$: O animal é classificado como **Adulto** e usa o $K_{\text{adulto}}$.
* **Cálculo Final:** $\text{Peso} = R \times K_{\text{calibrado}}$

Os fatores $K$ e os limites de proporção ($R_{\text{max}}$/$R_{\text{min}}$) foram calibrados usando dados reais de testes, garantindo a precisão do algoritmo.

---

## 🛠️ Próximos Passos de Desenvolvimento

1.  **Finalizar o Treinamento do Modelo Keypoint (YOLOv8-Pose):** O treinamento da IA (Modelo v4) deve ser finalizado para que a API retorne os dados de pose.
2.  **Implementar a TASK-19 (Lógica de Geometria):** Atualizar o arquivo `analisador/analysis_utils.py` com a função de cálculo de área de polígono (`Fórmula de Shoelace`) a partir dos Keypoints retornados pela IA.
3.  **Calibração Final:** Usar o aplicativo para testar imagens de referência de Nelore adulto para refinar os fatores $K$ e os limites de proporção no arquivo `breed_data.json`.