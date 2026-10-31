$env:VAULT_ADDR  = if ($env:VAULT_ADDR)  { $env:VAULT_ADDR }  else { "http://127.0.0.1:8200" }
$env:VAULT_TOKEN = if ($env:VAULT_TOKEN) { $env:VAULT_TOKEN } else { "dev-only-token" }

vault kv put secret/gateway `
    backend_shared_secret="gateway-api-secret-456" `
    auth_introspection_secret="gateway-auth-secret-789"

vault kv get secret/gateway
