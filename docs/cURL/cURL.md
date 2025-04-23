# Operação usando Postman ou cURL

<h2 style="border: none">Logar na conta</h2>

```bash
curl -X POST "http://127.0.0.1:5001/login" -H "Content-Type: application/json" -d "{\"email\": \"teste@gmail.com\", \"senha\": \"123456\"}"
```

**Resposta esperada:**

```json
{
  "mensagem": "Login realizado com sucesso!",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJlbWFpbCI6IjJAZ21haWwuY29tIiwiZXhwIjoxNzY5MzI2ODc4fQ.SsgJSsJKuAE7Ysvv9WtrjuAD_NZ4kXasn5unhwm3QBM"
}
```

## Listar amigos

```bash
curl -X GET "http://127.0.0.1:5000/friends/list" -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**Resposta esperada:**

```json
[
  {
    "email": "matheusveneski654@gmail.com",
    "id": 1,
    "nome": "Matheus"
  }
]
```

**Listar mensagens de um amigo específico**

```bash
curl -X GET "http://127.0.0.1:5000/friends/list/selected?friend_id=2" -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## Registrar usuários

```bash
curl -X POST "http://127.0.0.1:5001/register" -H "Content-Type: application/json" -d '{"nome":"Usuário Teste","email":"teste@gmail.com","senha":"123456"}'
```

**Resposta esperada:**

```json
{
  "mensagem": "Usuário registrado com sucesso!",
  "userUUID": "7275c7fc-9c53-48b8-b68f-49cb212f226a"
}
```

## Listar a ultima mensagem de um amigo.

```bash
curl -X GET "http://127.0.0.1:5001/friends/list/last?friend_id=SEU_FRIEND_ID" -H "Authorization: Bearer TOKEN_AQUi"
```

**Resposta esperada**

```json
{
  "lastMessage": "eai",
  "time": "11:37"
}
```