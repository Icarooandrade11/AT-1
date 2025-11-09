# Fluxo da Cadeia de Autenticação

1. **Recepção da Requisição**: um `AuthRequest` é criado com as credenciais de login, o conjunto de permissões exigidas e (quando já houver uma sessão estabelecida) o token de sessão do cliente.
2. **Inicialização do Contexto**: um `AuthContext` encapsula a requisição e fornece espaço para que os manipuladores escrevam dados compartilhados, como o registro do usuário, as permissões agregadas e os metadados da sessão.
3. **LoginHandler**:
   - Recupera o usuário a partir do `CredentialStore`.
   - Valida as credenciais informadas.
   - Popula o contexto com o registro do usuário e as permissões disponíveis.
   - Em caso de falha (usuário inexistente ou senha incorreta), interrompe a cadeia retornando um `AuthResult` com `success=False`.
4. **PermissionHandler**:
   - Lê do contexto o conjunto de permissões concedidas ao usuário.
   - Compara com as permissões requeridas na requisição.
   - Se alguma permissão estiver ausente, encerra o fluxo com erro indicando quais estão faltando.
5. **SessionValidationHandler**:
   - Verifica se existe um token de sessão na requisição.
   - Consulta o `SessionStore` para validar a sessão e garantir que não esteja expirada.
   - Em caso de sucesso, anexa os dados da sessão ao contexto para consumo posterior (ex.: rotas protegidas).
6. **Resultado Final**: se todos os manipuladores concluírem com `success=True`, o resultado final é retornado ao chamador com o contexto completo, permitindo que camadas superiores (como um controlador HTTP ou um serviço de domínio) prossigam com a lógica de negócios.

> **Observação**: novos manipuladores especializados — por exemplo, para MFA, logging ou auditoria — podem ser conectados utilizando `set_next`, mantendo a extensibilidade sem alterar a implementação dos manipuladores existentes.
