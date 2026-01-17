# Base de Conhecimento

## Dados Utilizados


| Arquivo | Formato | Propósito FinBot Educacional |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores |
| `perfil_investidor.json` | JSON | Explanar sobre finanças, se baseando no perfil do cliente e em suas dúvidas |
| `produtos_financeiros.json` | JSON | Sugerir produtos adequados ao perfil, conhecendo os produtos para explicar ao cliente |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente, usando esses dados de forma didatica |


---

## Adaptações nos Dados

> FIIs substituiu o fundo multimercado, pois são mais famosos e estão na moda.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os dados são carregados a partir de arquivos estáticos (JSON ou CSV) no início da sessão do agente. Essa base contém conceitos financeiros, regras de negócio e informações educativas que são inseridas no contexto do agente antes do processamento das mensagens do usuário.

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Os dados são utilizados como contexto no system prompt, garantindo que o agente responda apenas com base nas informações previamente definidas. Quando necessário, partes específicas da base de conhecimento são consultadas dinamicamente para complementar a resposta, mantendo o escopo e evitando alucinações. Injetando os dados para que o agente tenha o melhor escopo possível para atuar
---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```

Dados Produtos Financeiros:
[
  {
    "nome": "Tesouro Selic",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "100% da Selic",
    "aporte_minimo": 30.00,
    "indicado_para": "Reserva de emergência e iniciantes"
  },
  {
    "nome": "CDB Liquidez Diária",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "102% do CDI",
    "aporte_minimo": 100.00,
    "indicado_para": "Quem busca segurança com rendimento diário"
  },
  {
    "nome": "LCI/LCA",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "95% do CDI",
    "aporte_minimo": 1000.00,
    "indicado_para": "Quem pode esperar 90 dias (isento de IR)"
  },
  {
    "nome": "FIIs",
    "categoria": "fundo",
    "risco": "medio",
    "rentabilidade": "De 6 a 12% ao ano",
    "aporte_minimo": 100.00,
    "indicado_para": "Perfil moderado que busca diversificação e renda recorrente"
  },
  {
    "nome": "Fundo de Ações",
    "categoria": "fundo",
    "risco": "alto",
    "rentabilidade": "Variável",
    "aporte_minimo": 100.00,
    &
    dados perfil do investidor:
    {
  "nome": "João Silva",
  "idade": 32,
  "profissao": "Analista de Sistemas",
  "renda_mensal": 5000.00,
  "perfil_investidor": "moderado",
  "objetivo_principal": "Construir reserva de emergência",
  "patrimonio_total": 15000.00,
  "reserva_emergencia_atual": 10000.00,
  "aceita_risco": false,
  "metas": [
    {
      "meta": "Completar reserva de emergência",
      "valor_necessario": 15000.00,
      "prazo": "2026-06"
    },
    {
      "meta": "Entrada do apartamento",
      "valor_necessario": 50000.00,
      "prazo": "2027-12"
    }
  ]
}
Contexto do Agente Financeiro:
Objetivo:
Auxiliar o usuário com educação financeira básica, controle de gastos e planejamento financeiro geral.

Base de Conhecimento:
- Conceitos de orçamento pessoal
- Boas práticas de controle financeiro
- Definições de receitas, despesas e planejamento

Regras:
- Não fornecer recomendações de investimento
- Não acessar dados pessoais ou bancários
- Admitir limitações quando a informação não estiver disponível

Mensagem do Usuário:
"Como posso organizar melhor meus gastos mensais?"

```
