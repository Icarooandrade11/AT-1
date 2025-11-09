# Cadeia de Responsabilidade para Autenticação

Implementação em Python de uma cadeia de responsabilidade (`Chain of Responsibility`) focada em autenticação, contemplando as etapas de login, verificação de permissões e validação de sessão.

## Estrutura

- `auth/chain.py`: classes que definem o manipulador abstrato (`AuthHandler`) e os manipuladores concretos (`LoginHandler`, `PermissionHandler`, `SessionValidationHandler`).
- `auth/stores.py`: implementações simples em memória de repositórios de credenciais e sessões.
- `docs/auth_cor_diagram.md`: diagrama de classes (Mermaid) com a arquitetura proposta.
- `docs/auth_cor_flow.md`: descrição textual do fluxo de processamento da cadeia.
- `examples/demo.py`: exemplo de uso mostrando a cadeia completa em execução.

## Executando o Exemplo

```bash
python examples/demo.py
```

A saída exibe o `AuthResult` final contendo o contexto enriquecido com dados do usuário e da sessão quando todas as etapas são validadas com sucesso.
