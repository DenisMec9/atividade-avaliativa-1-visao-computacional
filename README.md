# Área Segura CV

Aplicação web com visão computacional para detectar pessoas em imagens e sinalizar risco em área restrita.

## Sobre o projeto

Este projeto foi desenvolvido com FastAPI e Jinja2, com inferência de IA usando o modelo `facebook/detr-resnet-50` (Hugging Face).

Fluxo principal:
1. Usuário envia uma imagem na tela de análise.
2. O sistema detecta objetos na imagem.
3. Se houver pessoa com confiança mínima definida, o sistema marca risco.
4. A interface exibe imagem original, imagem anotada e resumo das detecções.

## Caso de uso implementado

Detecção de pessoas em área restrita (cenário industrial).

Regra atual:
- Se pelo menos 1 pessoa for detectada com score >= 0.70, o sistema considera risco.

## Requisitos da atividade (checklist)

- [x] 2 ou 3 telas web (Início, Analisar, Sobre)
- [x] Front-end web (HTML/CSS com Jinja2)
- [x] Back-end em Python (FastAPI)
- [x] Caso de uso realista (monitoramento de área restrita)
- [x] Inferência de visão computacional com modelo pronto
- [x] Fluxo principal funcional de upload + inferência + resultado
- [x] Dockerfile para execução containerizada

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
  main.py                 # Rotas e páginas
  services/inference.py   # Pipeline de detecção e regra de risco
templates/                # Páginas HTML
static/css/               # Estilos
static/generated/         # Imagens geradas (originais e anotadas)
requirements.txt
Dockerfile
```

## Rotas da aplicação

- `GET /` -> página inicial
- `GET /analisar` -> formulário para enviar imagem
- `POST /analisar` -> executa inferência e retorna resultado
- `GET /sobre` -> descrição do caso de uso

## Como rodar localmente

### Requisitos

- Python 3.11 ou superior
- `pip` atualizado
- Conexão com internet no primeiro uso (para baixar o modelo)

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

### Configuração opcional

Você pode ajustar o limiar de confiança para considerar pessoa com variável de ambiente:

```bash
export PERSON_THRESHOLD=0.75
uvicorn app.main:app --reload
```

## Observações importantes

- A primeira inferência pode demorar mais por causa do download/carregamento do modelo.
- As imagens de entrada e saída são salvas em `static/generated/`.
- Formatos aceitos no upload: JPG, PNG e WEBP.
- Em caso de arquivo inválido, a aplicação retorna erro amigável sem quebrar a página.

## Integrantes

- Integrante 1: Denis Barbosa 
- Integrante 2: Mateus santiago  
- Integrante 3: Vitória iorhana
- Integrante 4: João victor
- Integrante 5: Lucas menezes 
- Integrante 6: Mayara roberta 
