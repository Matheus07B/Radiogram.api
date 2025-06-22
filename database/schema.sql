-- Usuarios.
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    telefone TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    userUUID TEXT,
    bio TEXT,
    pic TEXT,
    public_key TEXT
);

CREATE TABLE IF NOT EXISTS friendships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT UNIQUE,
    user_id INTEGER NOT NULL,
    friend_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES usuarios (id),
    FOREIGN KEY (friend_id) REFERENCES usuarios (id)
);

CREATE TABLE IF NOT EXISTS friendMessages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    iv TEXT,
    uuid TEXT UNIQUE,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    message TEXT,
    image TEXT,
    video TEXT,
    document TEXT,
    time TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES usuarios(id),
    FOREIGN KEY (receiver_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_code TEXT NOT NULL UNIQUE,
    user1_id INTEGER NOT NULL,
    user2_id INTEGER NOT NULL,
    FOREIGN KEY (user1_id) REFERENCES usuarios(id),
    FOREIGN KEY (user2_id) REFERENCES usuarios(id)
);
-- Usuarios.

-- Grupos.
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT DEFAULT '',
    image_url TEXT DEFAULT '',
    creator_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS group_members (
    user_id INTEGER NOT NULL UNIQUE,
    group_id INTEGER,
    group_uuid TEXT,
    FOREIGN KEY(user_id) REFERENCES usuarios(id),
    FOREIGN KEY(group_id) REFERENCES groups(id)
);

CREATE TABLE IF NOT EXISTS group_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER,
    sender_id INTEGER,
    receiver_uuid TEXT,
    message TEXT,
    image TEXT,
    document TEXT,
    video TEXT,
    time TEXT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(group_id) REFERENCES groups(id),
    FOREIGN KEY(sender_id) REFERENCES usuarios(id)
);
-- Grupos.

-- Outros.
CREATE TABLE IF NOT EXISTS recoverCodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    code TEXT NOT NULL
)
-- Outros.

-- IMPLEMENTAR DOS

-- Adicionar coluna (se não existir)
-- ALTER TABLE recoverCodes ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- -- Query modificada
-- SELECT email FROM recoverCodes 
-- WHERE code = ? 
-- AND created_at > datetime('now', '-15 minutes')