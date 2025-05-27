CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,    --
    nome TEXT NOT NULL,                      --
    email TEXT NOT NULL UNIQUE,              --
    telefone TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,                     --
    userUUID TEXT,                           -- UUID implementado.
    bio TEXT                                 --
);

CREATE TABLE IF NOT EXISTS friendships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    friend_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES usuarios (id),
    FOREIGN KEY (friend_id) REFERENCES usuarios (id)
);

CREATE TABLE IF NOT EXISTS friendMessages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    message TEXT,                               -- Mensagem pode ser nula se for imagem
    image TEXT,                                 -- Armazena a imagem como binário
    video TEXT,
    document TEXT,
    time TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES usuarios (id),
    FOREIGN KEY (receiver_id) REFERENCES usuarios (id)
);

CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,                 -- ID único da sala
    room_code TEXT NOT NULL UNIQUE,                       -- Código único da sala (pode ser um UUID ou um número)
    user1_id INTEGER NOT NULL,                            -- ID do primeiro usuário
    user2_id INTEGER NOT NULL,                            -- ID do segundo usuário
    FOREIGN KEY (user1_id) REFERENCES usuarios(id),
    FOREIGN KEY (user2_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS recoverCodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    code TEXT NOT NULL
)