# Area Segura CV - README para o Grupo

Aplicacao web com visao computacional para detectar pessoas em area restrita usando inferencia com modelo pronto do Hugging Face.

## Objetivo da atividade
Implementar um recorte funcional de um caso realista com:
- 2 ou 3 telas web
- backend em Python (FastAPI)
- inferencia de visao computacional (deteccao)
- codigo no GitHub
- README detalhado

## Caso de uso escolhido
Deteccao de pessoas em area restrita de ambiente industrial.

Quando uma imagem e enviada, o sistema:
- detecta objetos na cena
- conta pessoas detectadas
- sinaliza risco (presenca de pessoa em area restrita)
- mostra imagem anotada

## Modelo de IA utilizado
- Modelo: facebook/detr-resnet-50
- Plataforma: Hugging Face
- Tipo: object-detection

## Tecnologias
- Python 3.11+
- FastAPI
- Jinja2
- CSS
- Transformers
- PyTorch
- Pillow

## Telas da aplicacao
1. Inicio (/)
2. Analisar (/analisar)
3. Sobre (/sobre)

## Como rodar localmente
### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Acesse: http://127.0.0.1:8000

## Divisao do trabalho (6 integrantes)
1. Integrante 1: validacoes de upload no backend.
2. Integrante 2: melhorias visuais da tela de analise.
3. Integrante 3: regras de risco (baixo/medio/alto).
4. Integrante 4: historico de inferencias em JSON.
5. Integrante 5: testes basicos das rotas.
6. Integrante 6: documentacao + deploy (extra).

## Fluxo de Git (obrigatorio para nota individual)
Cada integrante deve:
1. Criar branch propria.
2. Fazer commits proprios.
3. Abrir pull request para main.

Exemplo:
```bash
git checkout -b feat/integranteX-tarefa
git add .
git commit -m "feat(area): implementa parte X"
git push -u origin feat/integranteX-tarefa
```

## O que ainda falta antes da entrega
- Preencher nomes completos dos 6 integrantes.
- Inserir link final do repositorio.
- Garantir commits de todos os integrantes.
- Opcional: deploy em nuvem com Docker para pontuacao extra.

## Integrantes (preencher)
- Integrante 1: NOME COMPLETO
- Integrante 2: NOME COMPLETO
- Integrante 3: NOME COMPLETO
- Integrante 4: NOME COMPLETO
- Integrante 5: NOME COMPLETO
- Integrante 6: NOME COMPLETO

## Link do repositorio (preencher)
- Repositorio: LINK_GITHUB_AQUI
