-- Inserir amizade
INSERT INTO friendships (user_id, friend_id) VALUES (2, 1);  -- João é amigo de Maria
sqlite> SELECT * FROM friendships WHERE user_id = 2

## Logar na conta.

curl -X POST `http://127.0.0.1:5000/login ` -H "Content-Type: application/json" ` -d "{\"email\": \"2@gmail.com\", \"senha\": \"1\"}"

curl -X POST "http://127.0.0.1:5000/login" -H "Content-Type: application/json" -d "{\"email\": \"2@gmail.com\", \"senha\": \"1\"}"
{"mensagem":"Login realizado com sucesso!","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJlbWFpbCI6IjJAZ21haWwuY29tIiwiZXhwIjoxNzY5MzI2ODc4fQ.SsgJSsJKuAE7Ysvv9WtrjuAD_NZ4kXasn5unhwm3QBM"}

## Listar mensagem de amigo.

curl -X GET "http://127.0.0.1:5000/friends/list" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJlbWFpbCI6IjJAZ21haWwuY29tIiwiZXhwIjoxNzY5MzI2ODc4fQ.SsgJSsJKuAE7Ysvv9WtrjuAD_NZ4kXasn5unhwm3QBM"
[{"email":"matheusveneski654@gmail.com","id":1,"nome":"Matheus"}]

curl -X GET "http://127.0.0.1:5000/friends/list" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJlbWFpbCI6IjJAZ21haWwuY29tIiwiZXhwIjoxNzY5MzI2ODc4fQ.SsgJSsJKuAE7Ysvv9WtrjuAD_NZ4kXasn5unhwm3QBM"

curl -X GET "http://seu-servidor.com/list/select?friend_id=2" \ -H "Authorization: Bearer SEU_TOKEN_AQUI"

curl -X GET "http://127.0.0.1:5000/friends/list/selected?friend_id=2" \ -H "Authorization: Bearer SEU_TOKEN_AQUI"

## Registrar usuarios.

C:\Users\mathe>curl -X POST "http://127.0.0.1:5001/register" -H "Content-Type: application/json" -d "{\"nome\":\"Usuário Teste\",\"email\":\"teste@gmail.com\",\"senha\":\"123456\"}"
{
  "mensagem": "Usu\u00e1rio registrado com sucesso!",
  "userUUID": "7275c7fc-9c53-48b8-b68f-49cb212f226a"
}

C:\Users\mathe>curl -X POST "http://127.0.0.1:5001/register" -H "Content-Type: application/json" -d "{\"nome\":\"2 dude\",\
"email\":\"2@gmail.com\",\"senha\":\"1\"}"
{
  "mensagem": "Usu\u00e1rio registrado com sucesso!",
  "userUUID": "e9687e40-2146-459a-b8df-d7a5946b2f7b"
}

C:\Users\mathe>curl -X POST "http://127.0.0.1:5001/register" -H "Content-Type: application/json" -d "{\"nome\":\"Matheus Fonseca\",\"email\":\"matheusveneski654@gmail.com\",\"senha\":\"123\"}"
{
  "mensagem": "Usu\u00e1rio registrado com sucesso!",
  "userUUID": "2bb50c70-d672-4871-b863-f23023ba47b5"
}

C:\Users\mathe>