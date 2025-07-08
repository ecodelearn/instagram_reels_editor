# Editor de Vídeo para Reels do Instagram

## 📖 Descrição

Esta é uma aplicação web desenvolvida com Streamlit que permite a criação rápida e personalizada de vídeos no formato de Reels para o Instagram (9:16). A ferramenta oferece uma interface intuitiva para combinar imagens, adicionar logos, sobreposições, legendas dinâmicas e trilha sonora, automatizando o processo de edição de vídeo.

## 🌊 Fluxo de Uso

A interface é dividida em duas seções principais: à esquerda, os controles para upload e personalização; à direita, um preview que é atualizado em tempo real.

```mermaid
graph TD
    subgraph "Tela da Aplicação"
        direction LR
        subgraph "Coluna de Controles (Esquerda)"
            A[Upload de Arquivos] --> B & C & D & E
            A---
            B(Imagens de Fundo)
            C(Logo)
            D(Legendas)
            E(Áudio)
            ---
            F[Configurações Gerais]
            F---
            G[Ajustes da Logo]
            G---
            H[Ajustes da Sobreposição]
            H---
            I[Ajustes da Legenda]
            I---
            J[Gerar Vídeo Final] --> K & L
            K(Nome do Arquivo)
            L(Botão 'Gerar Vídeo')
        end
        subgraph "Coluna de Visualização (Direita)"
            P[📺 Preview Reativo]
            P -- Atualiza com alterações em --> G
            P -- Atualiza com alterações em --> H
            P -- Atualiza com alterações em --> I
        end
    end
```

## ✨ Funcionalidades

-   **Upload de Múltiplos Arquivos:**
    -   Logo da marca (PNG).
    -   Imagem de sobreposição (PNG).
    -   Múltiplas imagens de fundo (JPG/PNG).
        -   **Ordenação Automática:** As imagens são ordenadas numericamente com base em seus nomes (ex: `01-foto.jpg`, `02-foto.jpg`, ...), garantindo a sequência correta no vídeo.
    -   Arquivo de texto (`.txt`) para as legendas.
    -   Trilha sonora (MP3/WAV).
-   **Configurações Gerais do Vídeo:**
    -   Definição da duração total do vídeo (15 a 90 segundos).
    -   Ajuste da duração de exibição de cada imagem.
-   **Personalização de Elementos:**
    -   **Logo:** Controle de posição (X, Y), tamanho e transparência.
    -   **Sobreposição:** Controle de posição (X, Y), tamanho e transparência.
    -   **Legendas:**
        -   Efeito de letreiro (scrolling text).
        -   Opção de loop para a animação da legenda.
        -   Controle de posição (Y), velocidade, tamanho da fonte, cor e tipo da fonte.
-   **Preview Reativo e Instantâneo:**
    -   Visualize as alterações em tempo real. A área de preview é atualizada automaticamente sempre que um controle (como a posição ou o tamanho da logo) é ajustado, fornecendo feedback visual imediato sem a necessidade de clicar em um botão.
-   **Geração e Download:**
    -   **Nome de Arquivo Personalizado:** Escolha o nome do arquivo de vídeo final. Um nome padrão com data e hora é sugerido para facilitar.
    -   Renderização do vídeo final em formato `.mp4`.
    -   Incorporação da trilha sonora, ajustada à duração do vídeo.
    -   Opção para baixar o vídeo diretamente pela interface.

## 🛠️ Tecnologias Utilizadas

-   **Python 3:** Linguagem de programação principal.
-   **Streamlit:** Framework para a criação da interface web.
-   **MoviePy:** Biblioteca para edição de vídeo.
-   **Pillow (PIL):** Para manipulação de imagens.
-   **NumPy:** Para operações numéricas, utilizada pelo MoviePy e Pillow.

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e executar a aplicação em seu ambiente local.

### 1. Pré-requisitos

-   Python 3.8 ou superior instalado.
-   `pip` (gerenciador de pacotes do Python).

### 2. Configuração do Ambiente

**Clone o repositório (se aplicável):**
```bash
git clone https://github.com/ecodelearn/instagram_reels_editor.git
cd instagram_reels_editor
```

**Crie e ative o ambiente virtual:**
```bash
# Crie o ambiente virtual
python -m venv .venv

# Ative o ambiente (Linux/macOS)
source .venv/bin/activate

# Ative o ambiente (Windows)
.venv\Scripts\activate
```

### 3. Instalação das Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

### 4. Executando a Aplicação

Para iniciar o editor de vídeo, execute o seguinte comando no seu terminal:
```bash
streamlit run video_editor.py
```

A aplicação será aberta automaticamente no seu navegador padrão.