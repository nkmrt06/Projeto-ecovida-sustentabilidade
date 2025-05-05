import streamlit as st

def mostrar_dicas_sustentaveis():


    st.write("Aqui estão as dicas sustentáveis!")

st.set_page_config(
    page_title="Dicas Sustentáveis • Eco-vida",
    page_icon="♻️",
    layout="centered"
)

    
st.title("♻️ Dicas Sustentáveis do Eco-vida")
st.markdown("Bem-vindo(a) ao seu guia de hábitos conscientes para um planeta mais saudável!")

    
tabs = st.tabs(["💧 Água", "⚡ Energia", "🚗 Transporte", "🗑️ Resíduos"])

with tabs[0]:
    st.subheader("💧 Economizando Água")
    st.write("- Tome banhos mais curtos (menos de 5 minutos).")
    st.write("- Feche a torneira enquanto escova os dentes.")
    st.write("- Reaproveite a água da chuva para regar plantas.")
    st.write("- Conserte vazamentos imediatamente.")
    st.write("- Lave roupas com carga completa na máquina.")

with tabs[1]:
    st.subheader("⚡ Economizando Energia")
    st.write("- Desligue aparelhos da tomada quando não estiverem em uso.")
    st.write("- Prefira lâmpadas de LED.")
    st.write("- Aproveite a luz natural sempre que possível.")
    st.write("- Use ventilador em vez de ar-condicionado quando possível.")
    st.write("- Programe aparelhos para o modo de economia de energia.")

with tabs[2]:
        st.subheader("🚗 Mobilidade Sustentável")
        st.write("- Prefira caminhar, pedalar ou usar transporte público.")
        st.write("- Organize caronas com colegas e vizinhos.")
        st.write("- Faça manutenções regulares no carro para reduzir emissões.")
        st.write("- Use aplicativos de mobilidade compartilhada.")
        st.write("- Se possível, opte por veículos elétricos ou híbridos.")

with tabs[3]:
    st.subheader("🗑️ Reduzindo e Reciclando Resíduos")
    st.write("- Separe lixo reciclável do orgânico.")
    st.write("- Evite produtos com excesso de embalagem.")
    st.write("- Reutilize potes, sacolas e materiais sempre que possível.")
    st.write("- Leve sacolas reutilizáveis ao fazer compras.")
    st.write("- Participe de iniciativas locais de coleta seletiva.")

    # Rodapé
st.markdown("---")
st.markdown("🌱 _Continue registrando seus hábitos no sistema Eco-vida para acompanhar seu impacto sustentável!_")
