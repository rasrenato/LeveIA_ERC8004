-- SCRIPT PARA CRIAR CONTAS DOS 9 TESTERS
-- Rodar: psql -h localhost -U leveclaw_user -d leveclaw -f CRIAR_CONTAS_TESTERS.sql

-- Inserir testers na tabela de usuários
INSERT INTO leveclaw.users (email, password_hash, name, role, created_at)
VALUES 
  ('weberson18@yahoo.com.br', '$2b$10$AlphaTest2026HashHere', 'Weberson Lopes', 'tester', NOW()),
  ('joelson.samora1977@gmail.com', '$2b$10$AlphaTest2026HashHere', 'Joelson', 'tester', NOW()),
  ('helciojose@hotmail.com', '$2b$10$AlphaTest2026HashHere', 'Helcio', 'tester', NOW()),
  ('joao_pereira1963@hotmail.com', '$2b$10$AlphaTest2026HashHere', 'João', 'tester', NOW()),
  ('samuelmonteirodesousa663@gmail.com', '$2b$10$AlphaTest2026HashHere', 'Sam', 'tester', NOW()),
  ('rnader2@yahoo.com.br', '$2b$10$AlphaTest2026HashHere', 'Ronaldo', 'tester', NOW()),
  ('santosreinaldo04958@gmail.com', '$2b$10$AlphaTest2026HashHere', 'Reinaldo', 'tester', NOW()),
  ('lucianorobsonm@gmail.com', '$2b$10$AlphaTest2026HashHere', 'Luciano', 'tester', NOW())
ON CONFLICT (email) DO NOTHING;

-- Verificar inserção
SELECT id, email, name, role, created_at FROM leveclaw.users WHERE role = 'tester';
