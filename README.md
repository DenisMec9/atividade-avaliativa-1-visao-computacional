[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/GBRRvVcH)
# Atividade Avaliativa 01

## Descrição da Atividade
Desenvolver uma aplicação simples com 2 ou 3 telas que utilize visão computacional em um caso de uso realista. A aplicação deve executar inferência com um modelo de IA, podendo envolver:
- classificação;
- e/ou detecção;
- e/ou segmentação

Não é obrigatório treinar um modelo do zero. A sugestão é utilizar modelos prontos, preferencialmente com apoio do Hugging Face para inferência.

## Requisitos

A aplicação deverá:
- possuir 2 ou 3 telas
- ter front-end livre, podendo ser usado, por exemplo:
  - HTML/CSS/JavaScript puro
  - Angular
  - React
  - outro framework equivalente
- ter front-end em Python, podendo ser usado qualquer framework, como por exemplo:
  - FastAPI
  - Django
  - Flask
  - outro framework equivalente
- implementar um caso de uso específico de uma aplicação real
- usar visão computacional com inferência de modelo
- não precisa implementar o sistema completo, apenas o fluxo principal do caso de uso escolhido
- estar com o código disponível em um repositório GitHub
- conter um README detalhado, explicando claramente como executar o projeto localmente
- além disso, no README detalhar o caso de uso implementado, além do nome completo de todos os integrantes do grupo.
- sugiro ser o mesmo grupo de Projeto Integrador V.
- todos os integrantes devem enviar a atividade com o link do github, caso contrário será despontuado ou poderá ficar sem nota.

## Exemplos de Casos de Uso

A ideia é implementar apenas um recorte funcional, e não uma solução corporativa completa, esses exemplos podem inspirar:
- detectar se uma pessoa está usando capacete em ambiente industrial
- classificar tipos de resíduos recicláveis a partir de imagem
- detectar presença de pessoas em área restrita
- segmentar região de doença em folha de planta
- classificar alimento saudável vs ultraprocessado por imagem da embalagem
- detectar rachaduras ou defeitos em superfícies
- segmentar áreas urbanas, vegetação ou água em imagens aéreas
- etc.

## Notas 
- Pontuação na média: 1,5 pontos
- Extra: 0,3 se caso consiga dockerizar, subir numa nuvem e se estiver funcionando plenamente no momento do teste do professor (Render, por exemplo).

## Detalhes Adicionais

Avaliação individual, portanto todos devem commitar no repositório. A nota individual será de acordo com parcela de contribuição de cada integrante do grupo.
Atenção: Commits feitos após esta data de corte serão desconsiderados.
Entrega até: segunda-feira 16/03/26, de 23h59min (não ultrapassar o prazo)

## Tutoriais

Exemplos de tutoriais que podem ajudar na resolução da atividade (configuração do servidor local):
- Anaconda (gerenciador de ambientes e pacotes): https://medium.com/@shb8086/tutorial-series-anaconda-7bfdfd84e2ff  
- FastAPI (considerar a parte de servidor, pois front-end deverá ser aplicação web simples): https://medium.com/@arun.badhai/fastapi-client-server-setup-using-conda-and-pip-a-beginner-friendly-guide-c239454ba254 
- A respeito de como fazer inferências com modelos, seguir algum padrão que foi apresentado em sala de aula. Recomendo utilizar Huggingface ou Ultralytics YoloV8.
