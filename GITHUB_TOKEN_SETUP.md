# 🔐 GitHub Token - Configuração Segura

**Data de Criação:** 2026-03-12  
**Expira em:** 2026-06-10 (90 dias)  
**Token:** `[REDACTED_GITHUB_TOKEN]`

---

## 📍 Onde Está Guardado

### **1. Git Credentials (para push automático)**
```
/root/openclaw/.git-credentials
Permissões: 600 (só root lê)
```

### **2. Environment Secrets (para scripts)**
```
/root/openclaw/.env.secrets
Permissões: 600 (só root lê)
```

### **3. Git Ignore (para não commitar sem querer)**
```
/root/openclaw/.gitignore
Contém: .env.secrets
```

---

## ⏰ Lembrete Automático

**Cron Job Criado:** `GitHub Token Expiry Reminder`

**Quando:** 2026-06-05 às 10:00 UTC (5 dias antes de expirar)

**O que faz:** Envia alerta no chat lembrando de girar o token

---

## 🔄 Como Girar o Token (Daqui a 90 Dias)

### **Passo 1: Criar Novo Token**
1. Acessar: https://github.com/settings/tokens
2. Click: "Generate new token (classic)"
3. Permissions: repo, workflow, admin:repo_hook
4. Copiar novo token

### **Passo 2: Atualizar Configuração**
```bash
# Editar .env.secrets
nano /root/openclaw/.env.secrets
# Atualizar GITHUB_TOKEN=SEU_TOKEN_AQUI

# Editar .git-credentials
nano /root/openclaw/.git-credentials
# Atualizar https://rasrenato:SEU_TOKEN_AQUI@github.com

# Testar push
cd /root/openclaw/alpha_signals
git push origin master
```

### **Passo 3: Deletar Token Antigo**
1. GitHub → Settings → Developer settings → Personal access tokens
2. Delete token antigo (`[REDACTED_GITHUB_TOKEN]`)

---

## 📊 Repositórios Configurados

| Repositório | URL | Status |
|-------------|-----|--------|
| LeveIA_ERC8004 | https://github.com/rasrenato/LeveIA_ERC8004 | ✅ Configurado |

---

## 🔒 Segurança

- ✅ Token guardado em arquivo com permissão 600
- ✅ Arquivo no .gitignore (não é commitado)
- ✅ Lembrete automático 5 dias antes de expirar
- ✅ Só o assistente tem acesso a esses arquivos

---

## 📝 Notas

- Token criado exclusivamente para push automático de Alpha Signals
- Válido por 90 dias (política de segurança)
- Após expirar, criar novo e seguir processo acima

---

**Última atualização:** 2026-03-12  
**Próxima ação:** 2026-06-05 (lembrete automático)
