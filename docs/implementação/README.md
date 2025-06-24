# Implementação do Radiogram: Guia Visual

Este `README.md` apresenta a implementação do aplicativo de mensagens **Radiogram**, oferecendo uma visão clara de suas funcionalidades principais através de capturas de tela das telas mais importantes. O Radiogram foi construído para ser um ambiente de comunicação dinâmico e eficiente, permitindo interações em tempo real entre usuários.

---

## Estrutura da Implementação

A implementação do Radiogram reflete o mini mundo conceitual, traduzindo suas entidades e interações em componentes funcionais do aplicativo.

### 1. Tela Principal (Início)

Esta é a primeira tela que o usuário vê. Ela exibe a **logo do aplicativo** e inclui botões para **Login** e **Registrar**. Além disso, oferece opções de download do **app para Windows** e para **Android**.

### 2. Tela de Login

Dedicada ao acesso de usuários já registrados. Além dos campos de credenciais, esta tela contém um botão **"Esqueci minha senha"**. Este botão leva o usuário a um fluxo de recuperação de conta que se desdobra em outras páginas: uma para **envio de e-mail** (onde o usuário informa o e-mail de cadastro), uma para **validar o código** de segurança recebido, e uma página final para **trocar a senha**, após a validação bem-sucedida do código.

### 3. Tela de Registrar

Permite que novos usuários criem uma conta no Radiogram, coletando as informações necessárias para configurar um novo perfil.

### 4. Tela Principal do Aplicativo (Menu)

Após o login, o usuário é direcionado para a tela principal de interação, que funciona como um **menu**. O principal destaque desta tela é a funcionalidade de **Chat**, onde todas as conversas acontecem.

### 5. Tela de Painel de Configurações

Esta tela centraliza todas as opções para configurar e personalizar o aplicativo, permitindo ao usuário gerenciar seu perfil e outras preferências do Radiogram.

### 6. Tela de Envio de Mídia/Arquivo

Esta tela, ou um componente similar, é acessada quando o usuário opta por anexar conteúdo, permitindo selecionar e enviar **imagens, vídeos ou outros arquivos** diretamente para a conversa.

---

## Detalhes Técnicos e Persistência

A implementação do Radiogram utiliza uma **API** robusta no backend para gerenciar todas as operações de dados. Isso abrange:

* **Autenticação de Usuários**: Gerenciamento seguro de credenciais e sessões.
* **Gerenciamento de Contatos**: Armazenamento e recuperação eficientes dos contatos.
* **Persistência de Mensagens**: Todas as mensagens são salvas de forma segura na API, garantindo que o histórico de conversas esteja sempre disponível e seja recuperável em qualquer dispositivo.
* **Comunicação em Tempo Real**: A arquitetura do app é projetada para permitir a troca instantânea de mensagens, assegurando uma experiência fluida.

Este `README.md` oferece uma visão geral da implementação do Radiogram e suas telas principais, mostrando como o conceito do mini mundo se materializa em um aplicativo funcional e intuitivo.