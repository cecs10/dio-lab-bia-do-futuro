import json
import pandas as pd
import requests
import streamlit as st
import re
import os 

# =========== CONFIGURAÇÃO ===========
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "deepseek-r1:8b"

# =========== CARREGAMENTO DE DADOS (COM CORREÇÃO DE DISCO) ===========
@st.cache_data
def carregar_dados():
    try:
        # CORREÇÃO CRÍTICA: São dois sublinhados antes e dois depois (__file__)
        arquivo_atual = os.path.abspath(__file__) 
        
        # Descobre a pasta onde o app.py está (ex: D:\Desktop\EDU\src)
        pasta_src = os.path.dirname(arquivo_atual)
        
        # Volta uma pasta para achar a raiz (ex: D:\Desktop\EDU)
        pasta_raiz = os.path.dirname(pasta_src)
        
        # Monta o caminho final para a pasta data
        caminho_dados = os.path.join(pasta_raiz, 'data')

        # Se não achar na raiz, tenta na mesma pasta (caso de segurança)
        if not os.path.exists(caminho_dados):
            caminho_dados = os.path.join(pasta_src, 'data')

        # Carrega os arquivos
        perfil = json.load(open(os.path.join(caminho_dados, 'perfil_investidor.json'), encoding='utf-8'))
        transacoes = pd.read_csv(os.path.join(caminho_dados, 'transacoes.csv'))
        historico = pd.read_csv(os.path.join(caminho_dados, 'historico_atendimento.csv'))
        produtos = json.load(open(os.path.join(caminho_dados, 'produtos_financeiros.json'), encoding='utf-8'))
        
        return perfil, transacoes, historico, produtos

    except FileNotFoundError as e:
        st.error(f"❌ Erro: Não encontrei a pasta 'data'.\nO Python procurou em: {caminho_dados}\nVerifique se a pasta 'data' está dentro de 'EDU'.")
        return None, None, None, None
    except Exception as e:
        st.error(f"Erro técnico: {e}")
        return None, None, None, None

perfil, transacoes, historico, produtos = carregar_dados()

# Só monta o contexto se os dados carregarem corretamente
if perfil:
    contexto = f"""
    CLIENTE: {perfil.get('nome', 'Cliente')}, {perfil.get('idade', 'N/A')} anos, perfil {perfil.get('perfil_investidor', 'N/A')}
    OBJETIVO: {perfil.get('objetivo_principal', 'N/A')}
    PATRIMÔNIO: R$ {perfil.get('patrimonio_total', 0)} | RESERVA: R$ {perfil.get('reserva_emergencia_atual', 0)}

    TRANSAÇÕES RECENTES:
    {transacoes.to_string(index=False)}

    ATENDIMENTOS ANTERIORES:
    {historico.to_string(index=False)}

    PRODUTOS DISPONÍVEIS:
    {json.dumps(produtos, indent=2, ensure_ascii=False)}
    """
else:
    contexto = ""

# ===================== SYSTEM PROMPT =====================
SYSTEM_PROMPT = """
Você é o FinBot Educacional, um educador financeiro amigável, didático e responsável.
OBJETIVO: Ensinar conceitos de finanças pessoais de forma simples.
DIRETRIZES:
- NÃO recomende investimentos específicos.
- Explique COMO funciona, nunca O QUE comprar.
- Limite suas respostas a no máximo 3 parágrafos curtos.
- Use o contexto do cliente para dar exemplos.
"""

# =========== CHAMAR OLLAMA ===========
def perguntar(msg):
    prompt_completo = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}
    """
    
    try:
        r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt_completo, "stream": False})
        r.raise_for_status()
        resposta_raw = r.json()['response']
        
        # Tratamento para separar o "pensamento" (Chain of Thought) da resposta final
        pensamento = ""
        resposta_final = resposta_raw
        
        match = re.search(r'<think>(.*?)</think>', resposta_raw, re.DOTALL)
        if match:
            pensamento = match.group(1).strip()
            resposta_final = re.sub(r'<think>.*?</think>', '', resposta_raw, flags=re.DOTALL).strip()
            
        return resposta_final, pensamento
        
    except requests.exceptions.ConnectionError:
        return "Erro: O Ollama parece estar desligado. Verifique se o servidor local está rodando.", None

# =========== INTERFACE STREAMLIT ===========
st.set_page_config(page_title="FinBot Educacional", page_icon="💸")
st.title("💸 Edu, Seu Educador Financeiro")

# 1. Inicializar Histórico na Sessão
if "mensagens" not in st.session_state:
    st.session_state["mensagens"] = []

# 2. Exibir mensagens anteriores (para não sumirem ao atualizar)
for msg in st.session_state["mensagens"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 3. Capturar nova interação
if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    # Exibe pergunta do usuário
    st.chat_message("user").write(pergunta)
    st.session_state["mensagens"].append({"role": "user", "content": pergunta})

    with st.spinner("O Edu está analisando..."):
        resposta, pensamento = perguntar(pergunta)
        
        with st.chat_message("assistant"):
            if pensamento:
                with st.expander("Ver raciocínio (Debug)"):
                    st.write(pensamento)
            
            st.markdown(resposta)
        
        # Salva resposta no histórico
        st.session_state["mensagens"].append({"role": "assistant", "content": resposta})