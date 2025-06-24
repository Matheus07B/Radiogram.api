# Diagrama de Caso de Uso: Radiogram

Este documento explica o **Diagrama de Caso de Uso** para o projeto Radiogram. Ele oferece uma visão de alto nível das **funcionalidades do sistema** e como os **usuários (atores)** interagem com ele.

---

## O Que É Este Diagrama?

O Diagrama de Caso de Uso é uma ferramenta de modelagem que descreve o **comportamento funcional de um sistema** do ponto de vista do usuário. Ele ilustra:

* **Atores:** Representam as entidades que interagem com o sistema (geralmente usuários, mas podem ser outros sistemas ou dispositivos). No Radiogram, o principal ator seria o **Usuário**.
* **Casos de Uso:** Descrevem as tarefas ou funcionalidades específicas que o sistema pode realizar em resposta à interação de um ator (por exemplo, "Fazer Login", "Enviar Mensagem", "Criar Conversa em Grupo"). Cada caso de uso representa um objetivo alcançável pelo ator usando o sistema.
* **Relacionamentos:** As linhas que conectam atores e casos de uso, indicando qual ator pode executar qual caso de uso. Relacionamentos entre os próprios casos de uso (como `<<include>>` para funcionalidades obrigatórias e `<<extend>>` para funcionalidades opcionais) também podem ser mostrados.

### Objetivo do Diagrama de Caso de Uso do Radiogram

O principal objetivo deste diagrama é fornecer uma **compreensão clara dos requisitos funcionais** do Radiogram. Ele ajuda a:

* **Identificar as funcionalidades essenciais:** O que o sistema deve fazer.
* **Definir as interações do usuário:** Como os usuários utilizam o sistema para atingir seus objetivos.
* **Comunicar o escopo do projeto:** Dar uma visão geral do que será desenvolvido para todas as partes interessadas, de forma simples e compreensível.
* **Guiar a criação de testes:** Os casos de uso podem ser diretamente relacionados a cenários de teste para verificar se as funcionalidades estão implementadas corretamente.

Em essência, o Diagrama de Caso de Uso do Radiogram é um mapa que mostra as **ações que um usuário pode realizar** dentro do aplicativo e as **respostas esperadas do sistema**, sem detalhar como essas ações são implementadas internamente.