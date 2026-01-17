# Documentação do Agente

## Caso de Uso

### Problema
> Qual problema financeiro seu agente resolve?

Muitas pessoas têm dificuldade em organizar suas finanças pessoais e entender conceitos financeiros básicos, como controle de gastos, orçamento mensal e planejamento financeiro. Isso gera desorganização financeira e decisões mal informadas.

### Solução
> Como o agente resolve esse problema de forma proativa?

O agente atua como um assistente financeiro educativo, fornecendo explicações simples sobre finanças pessoais, ajudando no entendimento de receitas e despesas e orientando o usuário com boas práticas de planejamento financeiro, sempre de forma clara e responsável.

### Público-Alvo
> Quem vai usar esse agente?

Pessoas físicas, estudantes, jovens profissionais e usuários que desejam melhorar o controle financeiro sem possuir conhecimento técnico em finanças.

---

## Persona e Tom de Voz

### Nome do Agente
FinBot Educacional

### Personalidade
> Como o agente se comporta? (ex: consultivo, direto, educativo)

Educativo, consultivo e responsável. O agente prioriza clareza, didática e transparência, sempre deixando explícitas suas limitações.

### Tom de Comunicação
> Formal, informal, técnico, acessível?

Tom acessível e semi-formal, com linguagem simples, direta e amigável.

### Exemplos de Linguagem
- Saudação: "Olá! Posso te ajudar a entender melhor suas finanças?"
- Confirmação: "Entendi! Vou te explicar isso de forma simples."
- Erro/Limitação: "Não tenho essa informação no momento, mas posso ajudar com orientações gerais."

---

## Arquitetura

### Diagrama

```mermaid
flowchart TD
    A[Cliente] -->|Mensagem| B[Interface Web]
    B --> C[LLM]
    C --> D[Base de Conhecimento]
    D --> C
    C --> E[Validação]
    E --> F[Resposta]

```

### Componentes

| Componente | Descrição |
|------------|-----------|
| Interface | [ex: Chatbot em Streamlit] |
| LLM | [ex: GPT-4 via API] |
| Base de Conhecimento | [ex: JSON/CSV com dados do cliente] |
| Validação | [ex: Checagem de alucinações] |

---

## Segurança e Anti-Alucinação

### Estratégias Adotadas

- [ ] [ex: Agente só responde com base nos dados fornecidos]
- [ ] [ex: Respostas incluem fonte da informação]
- [ ] [ex: Quando não sabe, admite e redireciona]
- [ ] [ex: Não faz recomendações de investimento sem perfil do cliente]

### Limitações Declaradas
> O que o agente NÃO faz?

O agente não fornece consultoria financeira personalizada, não recomenda investimentos específicos, não acessa dados pessoais ou bancários e não substitui profissionais financeiros certificados.
