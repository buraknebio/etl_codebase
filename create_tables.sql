CREATE TABLE openwebui_user (
    id VARCHAR2(1024) PRIMARY KEY,
    name VARCHAR2(1024),
    email VARCHAR2(1024),
    role VARCHAR2(1024),
    created_at date,
    updated_at date,
    last_active_at date,
    reflected_at date
);

CREATE TABLE openwebui_chat (
    id VARCHAR2(1024) PRIMARY KEY,
    user_id VARCHAR2(1024),
    title VARCHAR2(1024),
    chat CLOB,
    created_at date,
    updated_at date,
    reflected_at date
);
