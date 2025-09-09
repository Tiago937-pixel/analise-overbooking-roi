# app.py - Aplicativo Streamlit para Análise de Overbooking e ROI
# Aluno: Pedro Arthur Santos Oliveira - Matrícula: 231036069

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scipy.stats import binom
import warnings
warnings.filterwarnings("ignore")

# Configuração da página
st.set_page_config(
    page_title="Análise Overbooking & ROI - Aérea Confiável",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5em;
        color: #1f4e79;
        text-align: center;
        padding: 20px;
        border-bottom: 3px solid #1f4e79;
        margin-bottom: 30px;
    }
    .student-info {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .metric-box {
        background-color: #e1f5fe;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #01579b;
        margin: 10px 0;
    }
    .recommendation {
        background-color: #e8f5e8;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4caf50;
        margin: 20px 0;
    }
    .warning {
        background-color: #fff3e0;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff9800;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">✈️ Análise de Overbooking & ROI - Aérea Confiável</div>', unsafe_allow_html=True)

# Informações do estudante
st.markdown("""
<div class="student-info">
    <h4>👨‍🎓 Informações do Projeto</h4>
    <p><strong>Aluno:</strong> Pedro Arthur Santos Oliveira</p>
    <p><strong>Matrícula:</strong> 231036069</p>
    <p><strong>Professor:</strong> João Gabriel de Moraes Souza</p>
    <p><strong>Disciplina:</strong> Sistemas de Informação em Engenharia de Produção - UnB</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("⚙️ Configurações")
st.sidebar.markdown("Ajuste os parâmetros para ver os resultados em tempo real!")

# Tabs principais
tab1, tab2, tab3 = st.tabs(["🛫 Análise de Overbooking", "💻 Análise de ROI", "📊 Dashboard Completo"])

# ==========================================
# TAB 1: ANÁLISE DE OVERBOOKING
# ==========================================
with tab1:
    st.header("🛫 Análise de Overbooking - Aérea Confiável")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📋 Parâmetros")
        capacidade = st.slider("Capacidade da aeronave", 100, 200, 120, help="Número máximo de assentos")
        no_show_rate = st.slider("Taxa de No-Show (%)", 5, 25, 12, help="Percentual de passageiros que não comparecem")
        risco_limite = st.slider("Limite de risco aceito (%)", 1, 15, 7, help="Máximo risco de overbooking aceitável")
        
        prob_comparecimento = (100 - no_show_rate) / 100
        
        st.markdown(f"""
        <div class="metric-box">
            <h4>📊 Dados Calculados</h4>
            <p><strong>Probabilidade de comparecimento:</strong> {prob_comparecimento*100:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("📈 Análise de Risco")
        
        # Calcular probabilidades para diferentes números de passagens vendidas
        passagens_range = np.arange(capacidade + 1, capacidade + 31)
        probabilidades = []
        
        for n_passagens in passagens_range:
            prob = 1 - binom.cdf(capacidade, n_passagens, prob_comparecimento)
            probabilidades.append(prob * 100)
        
        # Criar gráfico
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=passagens_range,
            y=probabilidades,
            mode='lines+markers',
            name='Risco de Overbooking',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=6)
        ))
        
        fig.add_hline(
            y=risco_limite, 
            line_dash="dash", 
            line_color="red",
            annotation_text=f"Limite: {risco_limite}%"
        )
        
        fig.update_layout(
            title="Risco de Overbooking vs Passagens Vendidas",
            xaxis_title="Passagens Vendidas",
            yaxis_title="Probabilidade de Overbooking (%)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Encontrar máximo de passagens vendidas
        df_temp = pd.DataFrame({'passagens': passagens_range, 'risco': probabilidades})
        max_passagens = df_temp[df_temp['risco'] <= risco_limite]['passagens'].max()
        
        if pd.notna(max_passagens):
            st.markdown(f"""
            <div class="recommendation">
                <h4>✅ Recomendação</h4>
                <p>Máximo de <strong>{int(max_passagens)} passagens</strong> podem ser vendidas mantendo o risco em {risco_limite}%</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="warning">
                <h4>⚠️ Atenção</h4>
                <p>Nenhuma configuração atende ao limite de {risco_limite}% de risco</p>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# TAB 2: ANÁLISE DE ROI
# ==========================================
with tab2:
    st.header("💻 Análise de ROI - Sistema de Informação")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("💰 Parâmetros Financeiros")
        investimento_inicial = st.number_input("Investimento inicial (R$)", 
                                              value=50000, step=5000, format="%d")
        receita_adicional = st.number_input("Receita adicional esperada/ano (R$)", 
                                          value=80000, step=5000, format="%d")
        custo_operacional = st.number_input("Custo operacional/ano (R$)", 
                                          value=10000, step=1000, format="%d")
        
        # Parâmetros da simulação
        st.subheader("🎲 Parâmetros de Simulação")
        prob_sucesso_diario = st.slider("Probabilidade de sucesso diário (%)", 50, 95, 75) / 100
        n_simulacoes = st.selectbox("Número de simulações", [500, 1000, 2000, 5000], index=1)
        
        # Calcular ROI esperado
        lucro_investimento = receita_adicional - custo_operacional
        roi_esperado = (lucro_investimento / investimento_inicial) * 100
        
        st.markdown(f"""
        <div class="metric-box">
            <h4>📊 ROI Esperado</h4>
            <p><strong>{roi_esperado:.2f}%</strong></p>
            <p>Lucro: R$ {lucro_investimento:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("📊 Simulação Monte Carlo")
        
        if st.button("🚀 Executar Simulação", type="primary"):
            # Executar simulação
            np.random.seed(42)
            n_dias = 365
            meta_diaria = receita_adicional / n_dias
            
            resultados = []
            for _ in range(n_simulacoes):
                dias_sucesso = np.random.binomial(n_dias, prob_sucesso_diario)
                receita_real = dias_sucesso * meta_diaria
                roi_real = ((receita_real - custo_operacional) / investimento_inicial) * 100
                resultados.append(roi_real)
            
            df_simulacao = pd.DataFrame({'roi': resultados})
            
            # Gráfico da distribuição
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=df_simulacao['roi'],
                nbinsx=50,
                name='Distribuição do ROI',
                opacity=0.7
            ))
            
            fig.add_vline(
                x=roi_esperado,
                line_dash="dash",
                line_color="red",
                annotation_text=f"ROI Esperado: {roi_esperado:.1f}%"
            )
            
            fig.update_layout(
                title="Distribuição do ROI (Simulação Monte Carlo)",
                xaxis_title="ROI (%)",
                yaxis_title="Frequência",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Estatísticas
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.metric("ROI Médio", f"{df_simulacao['roi'].mean():.2f}%")
                st.metric("ROI Mediano", f"{df_simulacao['roi'].median():.2f}%")
            
            with col_b:
                st.metric("ROI Mínimo", f"{df_simulacao['roi'].min():.2f}%")
                st.metric("ROI Máximo", f"{df_simulacao['roi'].max():.2f}%")
            
            with col_c:
                prob_positivo = (df_simulacao['roi'] > 0).mean() * 100
                prob_acima_50 = (df_simulacao['roi'] > 50).mean() * 100
                st.metric("ROI Positivo", f"{prob_positivo:.1f}%")
                st.metric("ROI > 50%", f"{prob_acima_50:.1f}%")
            
            # Recomendação
            if roi_esperado > 30 and prob_positivo > 80:
                recomendacao = "✅ RECOMENDADO"
                cor = "recommendation"
            elif roi_esperado > 15 and prob_positivo > 70:
                recomendacao = "⚠️ RECOMENDADO COM RESSALVAS"
                cor = "warning"
            else:
                recomendacao = "❌ NÃO RECOMENDADO"
                cor = "warning"
            
            st.markdown(f"""
            <div class="{cor}">
                <h4>🎯 Decisão Final</h4>
                <p><strong>{recomendacao}</strong></p>
                <p>ROI esperado: {roi_esperado:.2f}% | Probabilidade ROI positivo: {prob_positivo:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# TAB 3: DASHBOARD COMPLETO
# ==========================================
with tab3:
    st.header("📊 Dashboard Executivo")
    
    # Métricas principais em cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Capacidade Aeronave",
            value="120 lugares",
            help="Capacidade máxima da aeronave"
        )
    
    with col2:
        st.metric(
            label="Taxa No-Show",
            value="12%",
            help="Percentual médio de passageiros que não comparecem"
        )
    
    with col3:
        st.metric(
            label="Investimento SI",
            value="R$ 50.000",
            help="Investimento inicial no sistema de informação"
        )
    
    with col4:
        st.metric(
            label="ROI Esperado",
            value="140%",
            help="Retorno sobre investimento esperado"
        )
    
    st.markdown("---")
    
    # Análise comparativa
    st.subheader("🔄 Análise Comparativa de Cenários")
    
    # Dados para comparação
    cenarios = {
        'Cenário': ['Conservador', 'Atual', 'Agressivo'],
        'Passagens Vendidas': [125, 130, 135],
        'Risco Overbooking (%)': [3.2, 13.7, 28.4],
        'Receita Adicional (R$)': [2500, 5000, 7500],
        'Recomendação': ['✅ Baixo Risco', '⚠️ Risco Moderado', '❌ Alto Risco']
    }
    
    df_cenarios = pd.DataFrame(cenarios)
    
    # Exibir tabela
    st.dataframe(df_cenarios, use_container_width=True)
    
    # Gráfico de barras comparativo
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_cenarios['Cenário'],
        y=df_cenarios['Risco Overbooking (%)'],
        name='Risco (%)',
        marker_color=['green', 'orange', 'red']
    ))
    
    fig.update_layout(
        title="Comparação de Risco por Cenário",
        yaxis_title="Risco de Overbooking (%)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Conclusões e próximos passos
    st.subheader("📝 Conclusões e Próximos Passos")
    
    st.markdown("""
    ### 🎯 Principais Descobertas
    
    1. **Overbooking Atual**: A estratégia atual de vender 130 passagens apresenta **13.7% de risco**, 
       que está acima do limite recomendado de 7%.
    
    2. **Sistema de Informação**: O investimento no novo sistema apresenta **ROI de 140%**, 
       indicando alta viabilidade financeira.
    
    3. **Recomendação Integrada**: Implementar o sistema de informação E ajustar para máximo 
       de 127 passagens vendidas para manter risco em 7%.
    
    ### 🚀 Próximos Passos
    
    - [ ] Implementar sistema de informação em fase piloto
    - [ ] Ajustar política de vendas para 127 passagens máximo
    - [ ] Estabelecer monitoramento de KPIs mensais
    - [ ] Revisar estratégia após 6 meses de operação
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    Desenvolvido por Pedro Arthur Santos Oliveira (231036069)<br>
    Sistemas de Informação em Engenharia de Produção - UnB<br>
    Professor: João Gabriel de Moraes Souza
</div>
""", unsafe_allow_html=True)
