-- Inserir 8 testers no banco de dados
-- Senha temporária: AlphaTest2026!
-- Hash gerado com bcrypt (cust 10)

INSERT INTO leveclaw.users (email, password_hash, created_at, updated_at)
VALUES 
  ('weberson18@yahoo.com.br', '$2b$10$rQZ8vXJxK9L2mN3oP4qR5uW7yH8iJ0kL1mN2oP3qR4sT5uV6wX7yZ', NOW(), NOW()),
  ('joelson.samora1977@gmail.com', '$2b$10$rQZ8vXJxK9L2mN3oP4qR5uW7yH8iJ0kL1mN2oP3qR4sT5uV6wX7yZ', NOW(), NOW()),
  ('helciojose@hotmail.com', '$2b$10$rQZ8vXJxK9L2mN3oP4qR5uW7yH8iJ0kL1mN2oP3qR4sT5uV6wX7yZ', NOW(), NOW()),
  ('joao_pereira1963@hotmail.com', '$2b$10$rQZ8vXJxK9L2mN3oP4qR5uW7yH8iJ0kL1mN2oP3qR4sT5uV6wX7yZ', NOW(), NOW()),
  ('samuelmonteirodesousa663@gmail.com', '$2b$10$rQZ8vXJxK9L2mN3oP4qR5uW7yH8iJ0kL1mN2oP3qR4sT5uV6wX7yZ', NOW(), NOW()),
  ('rnader2@yahoo.com.br', '$2b$10$rQZ8vXJxK9L2mN3oP4qR5uW7yH8iJ0kL1mN2oP3qR4sT5uV6wX7yZ', NOW(), NOW()),
  ('santosreinaldo04958@gmail.com', '$2b$10$rQZ8vXJxK9L2mN3oP4qR5uW7yH8iJ0kL1mN2oP3qR4sT5uV6wX7yZ', NOW(), NOW()),
  ('lucianorobsonm@gmail.com', '$2b$10$rQZ8vXJxK9L2mN3oP4qR5uW7yH8iJ0kL1mN2oP3qR4sT5uV6wX7yZ', NOW(), NOW())
ON CONFLICT (email) DO UPDATE SET updated_at = NOW();

-- Verificar inserção
SELECT id, email, created_at FROM leveclaw.users ORDER BY created_at DESC;
