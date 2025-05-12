# Radiogram API

A **Radiogram API** é a API responsável pelo funcionamento do **Radiogram**. Como uma API, ela permite que múltiplas plataformas se conectem a ela, oferecendo funcionalidades essenciais para a comunicação no sistema.

## Funcionalidades

A API lida com várias operações, incluindo autenticação de usuários, registro, e comunicação via WebSocket. A comunicação via WebSocket é utilizada para enviar mensagens e documentos para o servidor. Além disso, a API oferece endpoints específicos para listar amigos, mensagens, e salas de chat.

### Principais Funcionalidades:

- **Autenticação e Registro de Usuários:**
    - `/login`: Endpoint para autenticação de usuários.
    - `/register`: Endpoint para registro de novos usuários.

- **Gestão de Amigos e Mensagens:**
    - `/friends` : é uma Subrota que engloba todas as outras rotas da API responsavel somente por operações envolvendo usuarios, grupos e amigos.
        - `/list`: Lista todos os amigos que o usuario tem de amigo.
            - `/selected`: Seleciona todas as mensagens relacioanadas ao amigo selecionado no frontend.
            - `/last`: lista as últimas mensagens de cada amigo, nesse caso literalmete a ultima mensagem enviada não importando se foi o amigo ou o usuario.
        - `/get`: É só uma Subrota para pegar informações especificas.
            - `/room`: Retorna o código da sala de chat, ex: "1234567890987654321".
        - `/insert`: Insere todas as mensagem enviada no banco de dados, EX: 
            - sender(1), receiver(2), text("Ola") 
            - sender(1), receiver(234), text("Eai mano, beleza?")`
        - `/add`: **(Em desenvolvimento)** Adiciona um novo amigo.
        - `/LA`: Lista todos os usuários registrados. OBS: vai ser retirado depois.

- **Rotas de conexão e testes.**
    - `/connection`
        - retorna o status da conexão
        - `/v2` retorna o status da conexão só que com um v2 no final
    - `/email`
        teste de envio de email. OBS: futuramente será usado para fins de recuperação de conta e etc.
    - `/helloworld`
        Retorna um hello, world! no frontend para fins de testar a conexão.

- **Futuras rotas**
    - Futuramente terá rotas na API dedicada para Dev's que a queiram usar.

## WebSocket

A API utiliza o **Socket.IO** para comunicação em tempo real. As principais ações do WebSocket incluem:

- **join**: Entrar em uma sala de chat.
- **leave**: Sair de uma sala de chat.
- **message**: Enviar mensagens para a sala de chat.

> **Nota:** Novos eventos poderão ser adicionados à medida que o desenvolvimento avança.

## Tecnologias Utilizadas

- **Backend**:
    - Flask: Framework web para criar a API.
    - bcrypt: Biblioteca para criptografar textos e outros, nesse contexto para criptografia de senhas dos usuarios.
    - gunicorn: Servidor WSGI para rodar a aplicação em produção.
    - flask-cors: Habilita o CORS (Cross-Origin Resource Sharing) para a API.
    -PyJWT: Biblioteca para trabalhar com tokens JWT (JSON Web Tokens).
    - python-dotenv: Carrega variáveis de ambiente a partir de um arquivo .env.
    - flask_socketio: Integração do Flask com o Socket.IO para comunicação em tempo real.
    - gevent>=1.4: Biblioteca para operações assíncronas e multitarefa.
    - flask_sqlalchemy: Extensão para integrar o SQLAlchemy ao Flask.
    - flask_jwt_extended: Extensão Flask para autenticação usando JWT.
    werkzeug: Utilitário para o Flask.

<!-- ## Como Contribuir

Se você deseja contribuir para o projeto, fique à vontade para fazer um fork e enviar pull requests. Qualquer contribuição será muito bem-vinda! -->

<!-- ## Mini mundo

Confira o projeto [Minimundo](https://github.com/Matheus07B/Radiogram.api/docs/mini-mundo/README.md), que é parte do mesmo ecossistema.

## Diagrama de classe - OK

Aqui vai estar o [diagrama de classe](https://github.com/Matheus07B/Radiogram.api/docs/diagrama-de-classes/README.md). -->
