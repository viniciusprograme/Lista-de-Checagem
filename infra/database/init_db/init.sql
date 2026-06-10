-- initial schema for checklist_db

CREATE TABLE IF NOT EXISTS usuarios (
  id SERIAL PRIMARY KEY,
  nome TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  senha_hash TEXT NOT NULL,
  perfil TEXT NOT NULL,
  criado_em TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS checklists (
  id SERIAL PRIMARY KEY,
  data TIMESTAMP DEFAULT now(),
  tecnico TEXT,
  equipamento TEXT,
  local TEXT,
  perguntas JSONB,
  respostas JSONB
);

CREATE TABLE IF NOT EXISTS imagens (
  id SERIAL PRIMARY KEY,
  checklist_id INTEGER REFERENCES checklists(id) ON DELETE CASCADE,
  filename TEXT NOT NULL,
  mime TEXT,
  criado_em TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS assinaturas (
  id SERIAL PRIMARY KEY,
  checklist_id INTEGER REFERENCES checklists(id) ON DELETE CASCADE,
  filename TEXT NOT NULL,
  criado_em TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS pdfs (
  id SERIAL PRIMARY KEY,
  checklist_id INTEGER REFERENCES checklists(id) ON DELETE CASCADE,
  filename TEXT NOT NULL,
  criado_em TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS envios_email (
  id SERIAL PRIMARY KEY,
  checklist_id INTEGER REFERENCES checklists(id) ON DELETE CASCADE,
  destinatarios TEXT,
  enviado_em TIMESTAMP
);

CREATE TABLE IF NOT EXISTS logs (
  id SERIAL PRIMARY KEY,
  tipo TEXT,
  mensagem TEXT,
  criado_em TIMESTAMP DEFAULT now(),
  meta JSONB
);
