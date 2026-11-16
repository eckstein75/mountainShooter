# Mountain Shooter

Jogo 2D desenvolvido em Python com a biblioteca Pygame, utilizando programacao orientada a objetos.

O projeto apresenta um jogo de tiro com movimentacao lateral, dois jogadores, inimigos, efeitos visuais, pontuacao e progressao entre fases.

## Tecnologias

- Python 3
- Pygame 2.6.1
- Programacao Orientada a Objetos (POO)
- Git e GitHub
- Visual Studio Code

## Funcionalidades

- Menu principal interativo
- Modos de um ou dois jogadores
- Duas fases com cenarios diferentes
- Dificuldade progressiva
- Disparos dos jogadores e dos inimigos
- Sistema de colisao
- Pontuacao por inimigos eliminados
- Tres vidas individuais por jogador
- Protecao temporaria apos receber dano
- Efeito visual de invulnerabilidade
- Tela de Game Over
- Musicas especificas para menu e fases

## Controles

| Acao | Jogador 1 | Jogador 2 |
|------|-----------|-----------|
| Mover para cima | W | Seta para cima |
| Mover para baixo | S | Seta para baixo |
| Mover para esquerda | A | Seta para esquerda |
| Mover para direita | D | Seta para direita |
| Atirar | Espaco | Ctrl direito |

**Menu:** setas para selecionar e Enter para confirmar.

**Durante o jogo:** ESC retorna ao menu.

## Como executar

### 1. Clonar o repositorio

```bash
git clone https://github.com/eckstein75/mountainShooter.git
cd mountainShooter
```

### 2. Criar o ambiente virtual

No Windows:

```powershell
python -m venv venv
```

### 3. Ativar o ambiente virtual

No PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Caso a politica de execucao bloqueie a ativacao, utilize o interpretador diretamente:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe main.py
```

### 4. Instalar as dependencias

Com o ambiente virtual ativado:

```powershell
python -m pip install -r requirements.txt
```

### 5. Iniciar o jogo

```powershell
python main.py
```

## Organizacao do projeto

```text
mountainShooter/
|-- asset/
|-- code/
|   |-- __init__.py
|   |-- Background.py
|   |-- Enemy.py
|   |-- Entity.py
|   |-- EntityFactory.py
|   |-- Game.py
|   |-- Level.py
|   |-- Menu.py
|   `-- Player.py
|-- main.py
|-- requirements.txt
|-- .gitignore
`-- README.md
```

## Arquitetura

O projeto utiliza classes para separar as responsabilidades:

- **Entity:** classe-base das entidades.
- **Background:** movimentacao dos cenarios.
- **Player:** movimentacao, disparos e vidas.
- **Enemy:** comportamento dos inimigos.
- **EntityFactory:** criacao das entidades.
- **Menu:** interface inicial.
- **Level:** fases, colisoes e pontuacao.
- **Game:** inicializacao e fluxo principal do jogo.

## Desenvolvimento

Projeto desenvolvido para praticar Python, Pygame, orientacao a objetos, modularizacao e controle de versao.

## Autor

**eckstein75**

GitHub: https://github.com/eckstein75

Repositorio: https://github.com/eckstein75/mountainShooter