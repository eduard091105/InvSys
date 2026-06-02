# InvSys

## Autores

- Eduardo Cesar Goncalves
- Diogo Cruz

## Sobre o projeto

Sistema desktop para gerenciamento de inventário de computadores, desenvolvido em Python 3 com PyQt5 e SQLite.

O **InvSys** foi desenvolvido como um sistema desktop para auxiliar empresas, especialmente empresas da area de tecnologia, no controle de computadores, setores, funcionarios e licencas de inteligencia artificial. A proposta e centralizar informacoes importantes do ambiente de TI em uma interface simples, organizada e funcional.

O sistema permite cadastrar e acompanhar computadores da empresa, identificar o setor responsavel, controlar o status de seguranca de cada maquina e manter cadastros auxiliares como sistemas operacionais, antivirus, setores, funcionarios e licencas de IA.

## Objetivo

O objetivo do InvSys e oferecer uma solucao simples para inventario de TI, permitindo que a equipe responsavel tenha uma visao clara dos ativos cadastrados, dos funcionarios vinculados e da situacao de seguranca dos computadores.

Com isso, o sistema ajuda em tarefas como:

- Organizar os computadores da empresa
- Identificar maquinas vulneraveis ou em analise
- Relacionar computadores aos seus responsaveis
- Filtrar equipamentos por setor e status
- Controlar funcionarios e licencas de IA
- Preparar o projeto para build automatizado com Jenkins

## Publico-alvo

O sistema e voltado para equipes de TI, suporte tecnico, infraestrutura e seguranca da informacao que precisam manter um controle basico, mas eficiente, dos computadores e usuarios de uma empresa.

## Tecnologias utilizadas

- Python 3
- PyQt5
- SQLite
- sqlite3
- PyInstaller
- Inno Setup
- Jenkins

## Visao geral do funcionamento

Ao iniciar o InvSys, o banco de dados SQLite e criado automaticamente, sem necessidade de configuracao manual. A tela principal permite visualizar os computadores cadastrados em uma tabela, aplicar filtros e executar acoes de cadastro, edicao e exclusao.

O sistema tambem possui abas para manter cadastros auxiliares. Esses cadastros deixam o inventario mais consistente, pois permitem reaproveitar dados como setores, sistemas operacionais, antivirus, funcionarios e licencas de IA.

No cadastro de computadores, ao selecionar um setor, o campo de responsavel exibe apenas funcionarios vinculados ao setor escolhido. Isso evita associacoes incorretas e torna o preenchimento mais organizado.

## Funcionalidades

- Cadastro de computadores
- Edição de computadores cadastrados
- Exclusão de computadores
- Exclusão de múltiplos computadores pelo modo de seleção
- Listagem em tabela
- Filtro por status de segurança
- Filtro por setor
- Menu de botão direito na tabela para editar ou excluir
- Cadastros auxiliares de sistemas operacionais, antivírus e setores
- Cadastro de funcionarios
- Controle de licencas de IA por funcionario
- Tema claro e escuro com preferência salva
- Criação automática do banco SQLite

## Campos do cadastro

- Nome da máquina
- IP
- Sistema Operacional
- Antivírus
- Setor
- Responsável
- Status de segurança: Seguro, Vulnerável ou Em análise

## Estrutura

```text
inventario-ti/
├── assets/
│   └── README.md
├── app/
│   ├── ui/
│   │   ├── computer_form.py
│   │   ├── main_window.py
│   │   ├── reference_manager.py
│   │   └── styles.py
│   ├── database/
│   │   └── db_manager.py
│   ├── services/
│   │   └── computer_service.py
│   │   └── reference_data_service.py
│   └── main.py
├── installer/
│   └── setup.iss
├── inventario-ti.spec
├── requirements.txt
├── Jenkinsfile
└── README.md
```

## Banco de dados

O banco é criado automaticamente na primeira execução.

No Windows, o arquivo fica em:

```text
%APPDATA%\InvSys\inventario.db
```

Tabela criada automaticamente:

```sql
CREATE TABLE IF NOT EXISTS computadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    ip TEXT NOT NULL,
    sistema_operacional TEXT NOT NULL,
    antivirus TEXT,
    responsavel TEXT,
    status_seguranca TEXT,
    setor TEXT
);
```

O sistema tambem cria tabelas auxiliares para:

- `sistemas_operacionais`
- `antivirus_cadastrados`
- `setores`
- `licencas_ia`
- `funcionarios`

## Cadastros auxiliares

Na aba `Cadastros`, e possivel manter listas de sistemas operacionais, antivirus, setores e licencas de IA. Esses valores aparecem nos formularios e filtros do sistema.

Tambem e possivel digitar um valor novo diretamente ao adicionar/editar um computador; o InvSys salva esse valor no cadastro auxiliar automaticamente.

## Funcionarios e licencas de IA

Na aba `Funcionarios`, o sistema permite cadastrar:

- Nome
- Setor
- Cargo
- Licenca de IA
- Status da licenca

Status possiveis:

- Ativa
- Pendente
- Expirada
- Nao possui

O sistema ja vem com dados de exemplo para uma empresa de TI, incluindo computadores, setores, antivirus, sistemas operacionais, funcionarios e licencas de IA.

No cadastro de computadores, o campo `Responsavel` usa os funcionarios cadastrados. Ao selecionar um `Setor`, o InvSys mostra apenas os funcionarios daquele setor na lista de responsaveis.

## Tema claro e escuro

Na tela principal, use o campo `Tema` para alternar entre:

- Claro
- Escuro

A escolha fica salva automaticamente nas configuracoes do usuario pelo Qt e sera reaplicada na proxima abertura do InvSys.

## Como executar em desenvolvimento

Requisitos:

- Python 3 instalado
- Windows recomendado

Comandos:

```bat
cd inventario-ti
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m app.main
```

## Icone do sistema

Para o executavel, instalador e janela usarem uma imagem personalizada, coloque o arquivo no caminho:

```text
assets\app.ico
```

O Jenkins usara esse arquivo automaticamente quando ele existir. Para melhor resultado no Windows, use um `.ico` com tamanhos 16x16, 32x32, 48x48 e 256x256.

Se voce tiver apenas PNG ou JPG, salve primeiro em `assets\logo.png` e converta para `assets\app.ico` antes do build.

O Jenkins ja executa automaticamente:

```bat
python tools\create_icon.py
```

quando encontrar `assets\logo.png`.

## Build do executável com PyInstaller

```bat
cd inventario-ti
.venv\Scripts\activate
pyinstaller --clean --noconfirm inventario-ti.spec
```

O executavel sera gerado em:

```text
dist\InvSys\InvSys.exe
```

## Build do instalador com Inno Setup

Instale o Inno Setup 6 e execute:

```bat
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer\setup.iss
```

O instalador sera gerado em:

```text
dist\installer\InvSys-Setup.exe
```

## Jenkins

O `Jenkinsfile` executa:

- criação de ambiente virtual
- instalação das dependências
- build do executável com PyInstaller
- geração do instalador com Inno Setup
- arquivamento dos artefatos da pasta `dist`

O agente Jenkins precisa ter:

- Python 3 no `PATH`
- Inno Setup 6 instalado
- permissão de escrita no workspace
