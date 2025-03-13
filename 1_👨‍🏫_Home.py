import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import time

# Configuração da página
st.set_page_config(page_title="Portfólio - Rafael Sigoli", layout="wide")

# Carregar imagens
octocat = Image.open("octocatRafael.png")

# Criar menu lateral estilizado
with st.sidebar:
    selected = option_menu("Menu", ["Sobre Mim", "Experiencia", "Projetos", "Skills", "Contato"],
                          icons=["person", "book", "code", "bar-chart", "envelope"],
                          menu_icon="cast", default_index=0, styles={
                              "container": {"padding": "5px"},
                              "icon": {"color": "#f39c12", "font-size": "15px"},
                              "nav-link": {"text-align": "left", "margin": "5px"},
                              "nav-link-selected": {"background-color": "#f39c12"}
                          })

# Adicionando imagem de perfil
col1, col2 = st.columns([1, 3])
with col1:
    st.image("octocatRafael.png", width=150)
with col2:
    st.title("Rafael de Almeida Sigoli")
    st.subheader("Desenvolvedor Full-stack | Engenharia de Software")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/rafael-almeida-7660a6290/)")

# Seções do portfólio
if selected == "Sobre Mim":
    st.header("Sobre Mim")
    st.write("Sou um desenvolvedor Full-stack apaixonado por tecnologia e inovação.")
    st.write("Tenho experiência com diversas linguagens e frameworks, sempre buscando resolver problemas complexos com soluções inteligentes.")
    st.write("Atualmente, curso Engenharia de Software na FIAP e desenvolvo projetos que combinam tecnologia e criatividade.")
    st.success("🌐 Interessado em aprendizado de máquina, desenvolvimento sustentável e novas tecnologias.")

elif selected == "Experiencia":
    st.header("Formação Acadêmica")
    st.write("🎓 **Bacharelado em Engenharia de Software - FIAP**")
    
    st.header("Experiência Profissional")
    expander = st.expander("🔹 Starbucks - Learning & Development")
    expander.write("- Administração da plataforma self-learning\n- Tradução e criação de cursos\n- Desenvolvimento do curso 'Barista Treinador'")
    
    expander = st.expander("🔹 Projeto Goleiro 2D - FIAP")
    expander.write("- Desenvolvimento de IA para goleiro automatizado\n- Uso de Arduino, Raspberry Pi e visão computacional")

    expander = st.expander("🔹 Estágio Pekus | Desenvolvedor")
    expander.write("- Desenvolvimento de aplicativos	mobile utilizando Android	Studio	(Java) e .NET	MAUI	(C#), garantindo uma experiencia luida para os usuarios.\n- Identificaçao e correçao de bugs, alem da realizaçao de testes para assegurar a estabilidade e funcionalidade das aplicaçoes.\n -  Colaboraçao na implementaçao de novas	funcionalidades e melhorias em diversos projetos mobile.\n Otimizaçao de performance	e	estrutura	de	código, aprimorando a eiciencia e a escalabilidade das aplicaçoes.\n -  Utilizaçao de Git	para versionamento de codigo e documentaçao de processos tecnicos para garantir a escalabilidade do projeto.")
    
elif selected == "Projetos":
    st.header("Projetos Destacados")
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    with col1:

        st.subheader("App do Mecânico")
        st.image("mecanico.png", width=100)
        st.markdown("- Desenvolvimento de um aplicativo mobile para mecanicos que compram peças automotivas da Rede Ancora para revenda ou manutençao de veıculos.")
        st.markdown("- Implementaçao do back-end	em Java com	Spring	Boot, seguindo uma arquitetura em camadas para maior organizaçao e escalabilidade.")
        st.markdown("- Criaçao de APIs RESTful para integraçao futura com React Native")
        st.markdown("- Implementaçao de JWT (JSON Web Token) para autenticaçao e controle de acesso seguro a dados sensıveis.")
        st.markdown("-  Coniguraçao do banco de dados PostgreSQL, otimizando buscas e consultas de usuarios e historico de operaçoes.")

        
    with col2:
        st.subheader("Plataforma ICR - USP")
        st.image("instituto-da-crianca.jpg", width=300)
        st.markdown("- Desenvolvimento de plataforma interativa para Hospital das Clínicas, com foco em acessibilidade para pais e entretenimento para crianças.")
        st.markdown("- Apresentei o projeto na feira de tecnologia NEXT da FIAP, conquistando o segundo lugar pela inovação e impacto social da solução.")
        st.markdown("- Desenvolvi o front-end com React, criando uma interface atraente e responsiva, resultando em umamelhoria de 70% na experiência do usuário.")
        st.markdown("- Implementei o back-end com Java e Spring Boot, configurando APIs RESTful para conectar o frontend ao banco de dados de forma eficiente e segura.")
        st.markdown("- Implementei MySQL para armazenar e gerenciar dados de usuários, facilitando o acesso e a consulta de informações importantes, aumentando a eficiência do processamento de dados em 40%.")


    
elif selected == "Skills":
    st.header("Minhas Habilidades")
    
    st.subheader("Hard Skills")
    st.write("- **Linguagens:** Java, Python, C#, JavaScript.")
    st.write("- **Frameworks:** Spring Boot, .NET Core, React, Node.js, Angular.")
    st.write("- **Banco de Dados:** MySQL, PostgreSQL, SQL Server, Oracle.")
    st.write("- **Ferramentas:** Git/GitHub, Power BI, Excel.")
    st.write("- **Metodologias:** Scrum, Kanban.")
    
    st.subheader("Soft Skills")
    st.write("- Trabalho em equipe 🤝")
    st.write("- Comunicação assertiva 🎙️")
    st.write("- Resolução de problemas 🔍")
    st.write("- Adaptabilidade 💡")
    
elif selected == "Contato":
    st.header("Entre em Contato")
    st.write("📧 E-mail: rafael.almeida.sigoli@gmail.com")
    st.write("💼 [LinkedIn](https://www.linkedin.com/in/rafael-almeida-7660a6290/)")
    st.write("🐙 [GitHub](https://github.com/RafaelDevProjects)")
    
# Animação de carregamento
with st.spinner("Carregando mais informações..."):
    time.sleep(1)
