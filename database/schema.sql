CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    bio TEXT
);

CREATE TABLE IF NOT EXISTS friendships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    user_name TEXT NOT NULL,
    friend_id INTEGER NOT NULL,
    friend_name TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES usuarios (id),
    FOREIGN KEY (friend_id) REFERENCES usuarios (id)
);

CREATE TABLE IF NOT EXISTS friendMessages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,                           -- ID do usuário que enviou a mensagem
    receiver_id INTEGER NOT NULL,                         -- ID do usuário que recebeu a mensagem
    message TEXT NOT NULL,                                -- Conteúdo da mensagem
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,         -- Data e hora do envio
    room TEXT NOT NULL,                                   -- Sala de chat (opcional para identificar grupos/privados)
    FOREIGN KEY (sender_id) REFERENCES usuarios (id),
    FOREIGN KEY (receiver_id) REFERENCES usuarios (id)
);

CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
);