# Invariantes de Autenticación: Refresh Tokens

## 1. Fuente de verdad

**La base de datos es la única fuente de verdad sobre la semántica y validez de los tokens.**

* Los JWT **no contienen información semántica de uso** (access vs refresh).
* El tipo de token (`access`, `refresh`) se determina exclusivamente mediante la tabla `auth_session_tokens`.
* Cualquier decisión de autorización depende de la verificación contra la base de datos.

---

## 2. Rol del JWT

El JWT cumple únicamente funciones criptográficas y de identidad:

* Verificación de firma
* Verificación de expiración (`exp`)
* Verificación de emisor (`iss`) y audiencia (`aud`)
* Transporte de identidad (`sub`) y unicidad (`jti`)

El JWT **no define intención ni permisos de uso**.

---

## 3. Separación de responsabilidades

* **JwtTokenService**

  * Decodifica y valida JWTs
  * No conoce sesiones, revocaciones ni tipos de token

* **AuthSessionService**

  * Valida semántica del token contra la base de datos
  * Gestiona revocación, expiración lógica y rotación
  * Implementa protección contra token reuse

* **AuthService**

  * Orquesta el flujo de autenticación
  * Genera nuevos tokens
  * Coordina JWT + sesiones persistentes

---

## 4. Validación de Refresh Tokens

Un refresh token es considerado válido **si y solo si**:

* Existe un registro en `auth_session_tokens`
* `token_type = 'refresh'`
* `expires_at > now`
* `revoked_at IS NULL`
* `replaced_by_token IS NULL`

Esta validación constituye el equivalente funcional de un `assert_token_type`, pero **centralizado en la base de datos**.

---

## 5. Refresh Token Rotation

El sistema implementa **refresh token rotation estricta**:

1. El refresh token recibido se valida contra la base de datos
2. Si el token ya fue reemplazado (`replaced_by_token IS NOT NULL`):

   * Se considera un intento de reuse
   * Se revoca la sesión completa
3. El refresh token válido se revoca
4. Se emite un nuevo par (access + refresh)
5. El refresh token antiguo queda enlazado al nuevo mediante `replaced_by_token`

---

## 6. Invariante clave

> **La intención de un token nunca se infiere del JWT, siempre se valida contra la base de datos.**

Este principio permite:

* Revocación inmediata
* Detección de robo de tokens
* Protección contra replay attacks
* Evolución futura de políticas sin cambiar el formato del JWT

---

## 7. Consecuencia arquitectónica

Cualquier endpoint que requiera autenticación debe:

1. Validar el JWT criptográficamente
2. Resolver el `jti`
3. Validar la semántica del token en la base de datos según el contexto del endpoint

No existen excepciones a esta regla.

> **El JWT es el medio de transporte de identidad y no define permisos de uso.**

## Autenticación y gestión de sesiones

El framework implementa un sistema de autenticación basado en **JWT stateless** combinado con **sesiones persistentes**, diseñado para ser reutilizable, seguro y desacoplado de cualquier framework HTTP.

### Principios generales

- El framework **no conoce HTTP**, FastAPI ni conceptos de transporte.
- Toda la lógica de autenticación vive en servicios de aplicación y dominio técnico.
- La persistencia se abstrae mediante repositorios y Unit of Work.
- El framework puede ser utilizado por múltiples aplicaciones sin cambios.

### Modelo de autenticación

- Se utilizan **JWT** como tokens de acceso (access token).
- Cada JWT posee un `jti` único que permite su vinculación con una sesión persistente.
- El `sub` del JWT representa el `user_id` autenticado.

### Sesiones persistentes (`AuthSession`)

- Cada login crea una **AuthSession** independiente.
- El sistema permite **múltiples sesiones activas por usuario** (multisession).
- Una sesión representa una autenticación lógica (por ejemplo, un dispositivo o navegador).

La sesión:
- Tiene una fecha de expiración alineada con el refresh token.
- Puede ser revocada explícitamente (logout) o implícitamente (seguridad).

### Tokens por sesión

Cada sesión posee múltiples tokens persistidos:

- **Access Token**
- **Refresh Token**

Los tokens se almacenan en `auth_session_tokens` con:
- `token_jti`
- `token_type` (`access` / `refresh`)
- `issued_at`
- `expires_at`
- `revoked_at`
- `replaced_by_token` (solo para refresh tokens)

### Refresh Token rotativo

El framework implementa **refresh token rotation**:

- Cada refresh:
  - invalida el refresh token recibido
  - emite un nuevo access token
  - emite un nuevo refresh token
- El refresh token anterior queda marcado con `replaced_by_token`.

### Detección de reutilización de refresh token (replay attack)

- Si un refresh token ya fue reemplazado y vuelve a utilizarse:
  - se considera un ataque
  - se revoca **toda la sesión**
  - se rechaza la operación

### Logout y revocación

- El logout revoca la sesión completa:
  - marca la sesión como revocada
  - revoca todos los tokens asociados
- El logout es **idempotente**.

### Separación de responsabilidades

- `AuthService`
  - Orquesta autenticación
  - Genera JWT
  - Coordina sesiones
- `AuthSessionService`
  - Aplica reglas de negocio sobre sesiones
  - No conoce JWT ni HTTP
- `JwtTokenService`
  - Genera y valida JWT
  - Es completamente stateless

Esta arquitectura permite:
- escalabilidad horizontal
- revocación efectiva de tokens
- auditoría de sesiones
- alta seguridad sin perder simplicidad

> **El JWT es el medio de transporte de identidad y no define permisos de uso.**