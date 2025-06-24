# Mini Mundo: Radiogram

Este documento descreve o **Mini Mundo Radiogram**, um ambiente conceitual de um aplicativo de mensagens projetado para simular as interações e funcionalidades essenciais de uma plataforma de comunicação em tempo real. Ele serve como um modelo para entender a estrutura de dados, o fluxo de comunicação e as principais entidades envolvidas em um sistema de mensagens.

---

## O Que É o Mini Mundo Radiogram?

O Radiogram é um ambiente simulado onde **usuários** podem se cadastrar e interagir através de **mensagens individuais ou em grupo**. Ele foi concebido para ser um ecossistema digital dinâmico, com foco na **troca de textos, imagens, vídeos e documentos**. O gerenciamento de perfis, contatos e o ciclo de vida das mensagens são claramente definidos, simulando um sistema de comunicação completo.

---

## Elementos Fundamentais do Mini Mundo

### Usuários e Seus Perfis

Cada entidade de **usuário** no Radiogram possui uma identidade digital única e bem definida:

* **ID Único**: Um identificador primário para o usuário no sistema.
* **UUID Único**: Um Identificador Universalmente Único para operações internas do aplicativo.
* **Nome**: O nome que outros usuários verão.
* **E-mail**: Utilizado para contato e recuperação de conta.
* **Número de Celular**: Serve como o identificador principal para adição e gerenciamento de contatos.
* **Senha**: Para autenticação e segurança do perfil.
* **Foto de Perfil**: Uma representação visual do usuário.

### Conexões e Gerenciamento de Contatos

A interação entre usuários é facilitada por um sistema de contatos direto. Para **adicionar um contato**, basta que um usuário insira o **número de telefone** do outro, e a conexão é estabelecida imediatamente, sem necessidade de aprovação bidirecional.

### Conversas e Seu Dinamismo

As **conversas** são o cerne da interação neste mini mundo e podem ser de dois tipos:

* **Conversas Individuais**: Bate-papos privados entre dois usuários.
* **Conversas em Grupo**: Permitem que múltiplos usuários interajam simultaneamente.

Cada conversa possui um **ID único** para sua identificação e rastreabilidade. A **comunicação em tempo real** dentro dessas conversas é simulada através do conceito de um **protocolo WebSocket**, que permitiria uma conexão bidirecional e persistente com um servidor para a troca instantânea de mensagens.

### Mensagens e Seus Atributos

As **mensagens** são o conteúdo principal das conversas e são gerenciadas com precisão:

* **ID Único da Mensagem**: Um identificador exclusivo para cada mensagem.
* **Conteúdo Versátil**: As mensagens podem conter **texto, imagem, vídeo ou arquivos**, enriquecendo as possibilidades de comunicação.
* **Data/Hora de Envio**: Um registro temporal exato do envio da mensagem.
* **ID do Usuário Remetente**: Indica claramente quem enviou a mensagem.

---

## Funcionalidades e Persistência de Dados no Mini Mundo

No contexto deste mini mundo, algumas funcionalidades essenciais são consideradas para o gerenciamento de mensagens e dados:

* **Excluir Mensagens para Todos**: Permite que o remetente remova uma mensagem enviada da visualização de todos os participantes da conversa. Importante: apenas as mensagens que ele próprio enviou podem ser removidas.
* **Backup e Restauração de Conversas**: A **persistência dos dados** é um pilar deste mini mundo. O histórico de conversas é salvo e acessível, com a premissa de que a **API** subjacente é responsável por gerenciar o backup e a restauração de forma segura.

O Mini Mundo Radiogram, portanto, descreve um sistema de mensagens completo e funcional em um nível conceitual, detalhando suas entidades e como elas interagem para formar uma experiência de comunicação coerente.