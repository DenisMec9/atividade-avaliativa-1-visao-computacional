# Area Segura CV

Aplicacao web com visao computacional para detectar pessoas em imagens e sinalizar risco em area restrita.

## Sobre o projeto

Este projeto foi desenvolvido com FastAPI e Jinja2, com inferencia de IA usando o modelo `facebook/detr-resnet-50` (Hugging Face).

Fluxo principal:
1. Usuario envia uma imagem na tela de analise.
2. O sistema detecta objetos na imagem.
3. Se houver pessoa com confianca minima definida, o sistema marca risco.
4. A interface exibe imagem original, imagem anotada e resumo das deteccoes.

## Caso de uso implementado

Deteccao de pessoas em area restrita (cenario industrial).

Regra atual:
- Se pelo menos 1 pessoa for detectada com score >= 0.70, o sistema considera risco.

## Tecnologias

- Python 3.11+
- FastAPI
- Uvicorn
- Jinja2
- Transformers (Hugging Face)
- PyTorch
- Pillow

## Estrutura do projeto

```text
app/
  main.py                 # Rotas e paginas
  services/inference.py   # Pipeline de deteccao e regra de risco
templates/                # Paginas HTML
static/css/               # Estilos
static/generated/         # Imagens geradas (originais e anotadas)
requirements.txt
Dockerfile
```

## Rotas da aplicacao

- `GET /` -> pagina inicial
- `GET /analisar` -> formulario para enviar imagem
- `POST /analisar` -> executa inferencia e retorna resultado
- `GET /sobre` -> descricao do caso de uso

## Como rodar localmente

### Requisitos

- Python 3.11 ou superior
- `pip` atualizado
- Conexao com internet no primeiro uso (para baixar o modelo)

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Linux/macOS (bash)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abra no navegador:

`http://127.0.0.1:8000`

## Como rodar com Docker

```bash
docker build -t area-segura-cv .
docker run --rm -p 8000:8000 area-segura-cv
```

Abra no navegador:

`http://127.0.0.1:8000`

## Observacoes importantes

- A primeira inferencia pode demorar mais por causa do download/carregamento do modelo.
- As imagens de entrada e saida sao salvas em `static/generated/`.
- Formatos aceitos no upload: JPG, PNG e WEBP.

## Integrantes

- Integrante 1: NOME COMPLETO
- Integrante 2: NOME COMPLETO
- Integrante 3: NOME COMPLETO
- Integrante 4: NOME COMPLETO
- Integrante 5: NOME COMPLETO
- Integrante 6: NOME COMPLETO
