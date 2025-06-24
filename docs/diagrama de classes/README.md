# Diagrama de Classes: Radiogram

Este documento apresenta o **Diagrama de Classes** do projeto Radiogram. Ele serve como uma representação visual e estrutural do sistema de mensagens, detalhando as **principais entidades (classes)** e as **relações** entre elas.

---

## O Que É Este Diagrama?

O Diagrama de Classes é uma ferramenta fundamental na área de engenharia de software, especialmente para o **design orientado a objetos**. No contexto do Radiogram, ele ilustra de forma clara:

* **Classes:** Cada caixa no diagrama representa uma classe (como `Usuário`, `Conversa`, `Mensagem`, `Contato`). Essas classes encapsulam os dados (atributos) e o comportamento (métodos) de partes do sistema.
* **Atributos:** Dentro de cada classe, são listados os atributos, que são as informações ou características que a classe possui (por exemplo, `nome`, `email`, `senha` para a classe `Usuário`).
* **Relacionamentos:** As linhas que conectam as classes indicam como elas interagem entre si. Estes relacionamentos podem ser de diferentes tipos, como associação (uma conexão geral), agregação/composição (partes de um todo), generalização/herança (uma classe é um tipo de outra), ou dependência (uma classe usa outra).
* **Multiplicidade:** Números e símbolos nas extremidades das linhas de relacionamento que indicam quantos objetos de uma classe estão relacionados com quantos objetos de outra (por exemplo, um usuário pode ter muitas mensagens, mas uma mensagem tem apenas um remetente).

### Objetivo do Diagrama de Classes do Radiogram

O principal objetivo deste diagrama é fornecer uma **visão arquitetônica** do Radiogram. Ele ajuda a:

* **Compreender a estrutura interna:** Entender como os dados são organizados e como as diferentes partes do sistema se conectam.
* **Facilitar o desenvolvimento:** Serve como um mapa para desenvolvedores, orientando a implementação das classes e seus comportamentos.
* **Apoiar a manutenção e evolução:** Torna mais fácil identificar onde e como as alterações podem ser feitas sem impactar negativamente outras partes do sistema.

Em essência, o Diagrama de Classes do Radiogram é um modelo fundamental que descreve a **espinha dorsal** do sistema, mostrando os "tijolos" (classes) e como eles são montados para construir o aplicativo de mensagens.