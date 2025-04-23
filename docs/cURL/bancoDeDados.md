# Operação direta no banco de dados.

<h2 style="border: none">Inserir amizade</h2>

```sql
INSERT INTO friendships (user_id, friend_id) VALUES (2, 1);  -- João é amigo de Maria
SELECT * FROM friendships WHERE user_id = 2;
```

## Inserir mensagem na tabela de mensagens

```sql
INSERT INTO friendMessages (sender_id, receiver_id, message, room)
VALUES (1, 2, 'Tudo certo com você?', 'sala1');
```

<br/>