# API Python: Open-Meteo to SAMSON

Este projeto é uma API desenvolvida em Python que utiliza a [Open meteo](https://open-meteo.com/) para acessar dados meteorológicos específicos e converte esses dados no formato JSON para o formato SAMSON (.sam). Foi especialmente desenvolvido para otimizar o trabalho dos colaboradores da minha empresa que atuam na área de meteorologia. Com isso, reduzi significativamente o tempo gasto na coleta, organização e formatação de dados meteorológicos, transformando isso em apenas um clique no link [https://renan-rezende.azurewebsites.net/generate-file](https://renan-rezende.azurewebsites.net/generate-file)

## Objetivo

Antes da implementação desta solução, os colaboradores precisavam:

1. Acessar manualmente o site do Open-Meteo.
2. Baixar os dados meteorológicos necessários.
3. Ajustar colunas e formatação em um software separado para compatibilizá-los com suas ferramentas de análise.

Este projeto automatiza todo esse fluxo de trabalho, aumentando a produtividade e a precisão ao preparar os dados para análise no software que utiliza apenas arquivos SAMSON.

---

## Funcionalidades

- **Acesso à API Open-Meteo:**

  - Obtenção de dados meteorológicos específicos com base em parâmetros configuráveis, como localização e período de tempo.

- **Conversão de formatos:**

  - Conversão automática dos dados obtidos no formato JSON para o formato SAMSON (.sam).

- **Configurações flexíveis:**

  - Parâmetros personalizáveis para extração de dados e mapeamento preciso para o arquivo SAMSON.

---

## Requisitos

- **Linguagem:** Python 3.8+
- **Bibliotecas Necessárias:**
  - `fastapi`
  - `uvicorn`
  - `pandas`
  - `openmeteo-requests`
  - `requests-cache`
  - `retry-requests`
  - `openpyxl`

Instale as dependências com:

```bash
pip install -r requirements.txt
```

---

## Como Usar

### 1. Clone o repositório:

```bash
git clone https://github.com/renan-rezende/conversao.git
cd conversao
```

### 2. Execute o programa:

```bash
uvicorn main:app --reload
```

### 3. Resultado:

- Acesse a rota `/generate-file` para gerar e baixar o arquivo `.sam`.

---

## Estrutura do Projeto

```
.
├── main.py               # Script principal
├── requirements.txt      # Dependências
└── arquivos/             # Arquivos gerados no formato SAMSON
```

---

## Benefícios

- **Redução de tempo:** Automatiza um processo que anteriormente demandava várias etapas manuais.
- **Precisão:** Garante a formatação correta e compatibilidade com o software SAMSON.
- **Escalabilidade:** Permite ajustar os parâmetros para diferentes tipos de dados meteorológicos e locais.

---

## Contribuição

Contribuições são bem-vindas! Para sugerir melhorias ou corrigir bugs, envie um *pull request* ou abra uma *issue*.

---

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

