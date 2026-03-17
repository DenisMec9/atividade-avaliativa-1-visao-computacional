# Area Segura CV

Aplicacao web com visao computacional para detectar pessoas em imagens e sinalizar risco em area restrita.

## Sobre o projeto

Este projeto foi desenvolvido com FastAPI e Jinja2, com inferencia de IA usando o modelo hustvl/yolos-tiny no deploy da Render.

Fluxo principal:
1. Usuario envia uma imagem na tela de analise.
2. O sistema detecta objetos na imagem.
3. Se houver pessoa com confianca minima definida, o sistema marca risco.
4. A interface exibe imagem original, imagem anotada e resumo das deteccoes.

## Caso de uso implementado

Deteccao de pessoas em area restrita (cenario industrial).

Regra atual:
- Se pelo menos 1 pessoa for detectada com score maior ou igual a 0.70, o sistema considera risco.

## Requisitos da atividade

- 2 ou 3 telas web (Inicio, Analisar, Sobre)
- Front-end web com HTML/CSS
- Back-end em Python com FastAPI
- Inferencia de visao computacional com modelo pronto
- Fluxo principal funcional de upload e resultado
- Execucao com Docker

## Tecnologias

- Python 3.11+
- FastAPI
- Uvicorn
- Jinja2
- Transformers
- PyTorch
- Pillow

## Estrutura do projeto

app/
  main.py
  services/inference.py
templates/
static/css/
static/generated/
requirements.txt
Dockerfile
render.yaml

## Rotas da aplicacao

- GET /
- GET /analisar
- POST /analisar
- GET /sobre

## Como rodar localmente

### Windows (PowerShell)

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload

### Linux/macOS (bash)

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload

Acesse no navegador:
http://127.0.0.1:8000

## Variaveis opcionais

- PERSON_THRESHOLD: limiar de confianca para considerar pessoa (0.0 a 1.0)
- DETECTION_SCORE_THRESHOLD: score minimo para exibir deteccoes (0.0 a 1.0)
- NMS_IOU_THRESHOLD: limiar de IoU para remover caixas duplicadas da mesma classe (0.0 a 1.0)
- MIN_BOX_AREA_RATIO: area minima relativa da caixa para filtrar ruido (0.0 a 1.0)
- ENABLE_FLIP_TTA: ativa inferencia extra com espelhamento horizontal (true/false)
- HF_MODEL_ID: modelo do Hugging Face para deteccao

## Presets recomendados

### 1) Fotos com muitas pessoas (mais conservador)

Reduz caixas duplicadas e falsos positivos.

- PERSON_THRESHOLD=0.75
- DETECTION_SCORE_THRESHOLD=0.68
- NMS_IOU_THRESHOLD=0.40
- MIN_BOX_AREA_RATIO=0.002
- ENABLE_FLIP_TTA=true

### 2) Nao perder pessoas (mais sensivel)

Prioriza recall, podendo aumentar um pouco o ruido.

- PERSON_THRESHOLD=0.65
- DETECTION_SCORE_THRESHOLD=0.55
- NMS_IOU_THRESHOLD=0.50
- MIN_BOX_AREA_RATIO=0.001
- ENABLE_FLIP_TTA=true

No Render, esses valores podem ser editados em Environment.

Exemplo:
PERSON_THRESHOLD=0.75

## Deploy na Render

O projeto esta preparado para deploy via Blueprint com o arquivo render.yaml.

Passos:
1. Conectar repositorio no Render.
2. Criar Blueprint usando render.yaml.
3. Aguardar deploy.
4. Abrir URL publica gerada.

## Observacoes importantes

- No plano free, a instancia pode hibernar por inatividade.
- A pasta static/generated nao e persistente em reinicios.
- O primeiro uso pode demorar mais por download inicial de modelo.

## Integrantes

- Denis Barbosa
- Mateus Santiago
- Vitoria Iorhana
- Joao Victor
- Lucas Menezes
- Mayara Roberta
