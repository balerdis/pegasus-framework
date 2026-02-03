# pegasus_framework

## Descripción general

`pegasus_framework` es un **framework interno reusable** para la construcción de APIs en **FastAPI**, diseñado con principios de **Clean Architecture**, **Domain-Driven Design (DDD)** y el patrón **Unit of Work (UoW)**.

Su objetivo es proveer:

- Infraestructura común.
- Patrones arquitectónicos estables.
- Módulos de negocio reutilizables.
- Un modelo transaccional consistente.

El framework **no es una aplicación** y **no expone endpoints por sí mismo**.  
Está diseñado para ser **consumido por aplicaciones** que definan su propio contrato HTTP.

---

## Principio fundamental

> **El framework no depende de ninguna aplicación.**  
> Las aplicaciones dependen del framework, nunca al revés.

Esta regla es estricta y define todas las decisiones de diseño.

---

## Responsabilidad del framework

`pegasus_framework` provee:

- Infraestructura de base de datos (SQLAlchemy).
- Implementación del patrón Unit of Work.
- Repositorios base y contratos.
- Servicios de negocio reutilizables.
- DTOs de dominio (no HTTP).
- Wiring y providers de dependencias.
- Componentes comunes de API (middleware, excepciones, schemas genéricos).

No provee:

- Endpoints HTTP finales.
- Configuración específica de una aplicación.
- Reglas de negocio específicas de un dominio concreto.

---

## Arquitectura interna

El framework está organizado como un **monorepo modular**, con un único paquete publicado y un único namespace:

```text
pegasus_framework/
├── pyproject.toml                     # File dependencias para package del pegasus-framework
├── README.md                          # File de Documentacion del pegasus-framework
└── src                                # Directorio para estructura necesaria para exponer como package el proyecto
    └── pegasus_framework              # Directorio para estructura necesaria para exponer como package el proyecto
        ├── api                        # Directorio para todo lo que tenga que ver referido a la app api
        │   ├── exceptions             # Directorio para trabajar con exception de la app api
        │   │   ├── handlers           # Directorio para handlers de exception domain personalizadas y sus registries
        │   ├── middleware             # Directorio para establecer middleware de auth (ver documentacion sobre esto)
        │   ├── system                 # Directorio para endpoints del system pegasus-framework (vale para cualquier app)
        │   └── v1                     # Directorio para logica para exponer codigo utilizable por la app api v1
        │       └── schemas            # Directorio para los schemas DTOs utilización de la capa service de la app api v1
        ├── auth                       # Directorio para el sistema de Authentication y Authorization del framework
        │   ├── exceptions             # Directorio para las exceptions en el auth del framework (que luego seran registradas con registry)
        │   ├── models                 # Directorio para modelos de la base de datos que son cross a todas las apps
        │   ├── repositories           # Directorio para el patron repositories sobre tablas cross a todas las apps
        │   ├── security               # Directorio para los servicios "tecnicos" referidos a la seguridad en el Auth del pegasus-framework
        │   └── services               # Directorio para los domain service de Auth
        ├── business                   # Directorio para las clases "base" de todo service del framework y de la app
        ├── core                       # Directorio para la logica que no tiene que ver con la app api
        │   ├── config                 # Directorio para la configuracion centralizada del framework
        │   └── exceptions             # Directorio para las exceptions del framework (que luego seran manejadas por los handlers)
        │       └── domain             # Directorio para sectorizar las domain exceptions del framework
        ├── db                         # Directorio para la logica "base" referida a la base de datos
        │   ├── connection.py          # File central donde se define la conexion a la DB y pool de conexiones
        │   ├── models                 # Directorio para modelos genericos de base de datos cross a todas las apps
        │   ├── repositories           # Directorio para repositories de base de datos cross a todas las apps
        │   └── unit_of_work           # Directorio para implementar Unit of Work transaccional contra la base de datos
        └── wiring                     # Directorio para wiring con las apps que pueda utilizar la logica del framework con bajo acoplamiento

```


Todos los módulos viven bajo el namespace:

pegasus_framework.*


Los módulos internos **no son paquetes pip independientes**.  
El aislamiento es **arquitectónico**, no por repositorios.

---

## Módulos principales

### `business`

Contiene módulos de negocio **reutilizables** y autocontenidos.

Ejemplo:
```text
business/
└── users/
├── dto/
├── user_model.py
├── user_repository.py
└── user_service.py
```

Características:

- Encapsulan reglas de negocio.
- No dependen de FastAPI.
- No conocen el contrato HTTP.
- Operan siempre dentro de una Unit of Work.

---

### `db`

Responsable de la infraestructura de persistencia:

- Configuración de SQLAlchemy.
- Repositorios base.
- Implementación de Unit of Work.
- Integración con Alembic.

Principios clave:

- Una sesión por Unit of Work.
- Commit y rollback centralizados.
- Sin `update()` explícito en repositorios.

---

### `api`

Componentes HTTP **reutilizables**, pero no endpoints finales:

- Middleware.
- Manejo de excepciones.
- Schemas genéricos (status, health, respuestas comunes).

Las aplicaciones consumidoras deciden **qué endpoints exponer**.

---

### `wiring`

Responsable de:

- Proveer dependencias.
- Construir servicios con sus dependencias reales.
- Centralizar la inicialización del framework.

Este módulo es el único punto donde se “conecta” infraestructura con negocio.

---

## DTOs vs Schemas HTTP

El framework define **DTOs de negocio**, no schemas HTTP.

Características de los DTOs:

- Representan datos internos del dominio.
- No están acoplados a FastAPI.
- Pueden ser usados por múltiples aplicaciones.

Las aplicaciones consumidoras son responsables de definir:

- Schemas HTTP.
- Contratos de entrada y salida.
- Versionado de la API.

---

## Extensibilidad

El framework está diseñado para ser **extendido sin ser modificado**.

Las aplicaciones pueden:

- Reemplazar providers.
- Overridear servicios.
- Componer wiring alternativo.

Todo esto sin romper la dependencia unidireccional.

---

## Qué garantiza el framework

- Consistencia transaccional.
- Separación clara de responsabilidades.
- Aislamiento del ORM.
- Reglas de negocio testeables.
- Evolución controlada del sistema.

---

## Qué no garantiza

- Diseño de endpoints.
- Contratos HTTP estables.
- Reglas de negocio específicas.

Eso es responsabilidad de cada aplicación.

---

## Documentación adicional

Para entender cómo una aplicación consume este framework y cómo se organiza el sistema completo, consultar el README y la documentación de la aplicación correspondiente.

# Limitaciones generales en la capa de middleware
 - AuthContextMiddleware: Extraer y normalizar identidad técnica del request para consumo por otros middlewares (rate-limit, logging, métricas). No es un middleware de autenticación (No autentica, no autoriza, no valida tokens).
 - Nunca validar sesión en middleware
 - Nunca acceder a DB desde middleware
 - Nunca usar user_id
 - Nunca loggear tokens
 - Solo hashes / fingerprints
 - Fallar rápido (429)

## Invariantes de Dominio — Authentication

Las siguientes reglas son **invariantes del dominio de autenticación** y
**deben cumplirse en todas las implementaciones** que utilicen este framework.

Estas invariantes **no dependen del transporte (HTTP)** ni de detalles de
infraestructura, y se aplican exclusivamente en la capa de dominio.

---

### Revocación de sesión

> **Invariant:**  
> Revocar una `AuthSession` implica revocar **todos** los `AuthSessionToken`
> asociados a dicha sesión, independientemente de su tipo
> (`access`, `refresh`, u otros futuros).

Consecuencias:

- Ningún token asociado a una sesión revocada puede considerarse válido.
- La revocación de tokens es una **responsabilidad del dominio**, no de la capa HTTP.
- La operación debe ser **atómica** y ejecutarse dentro de una única Unit of Work.

---

### Logout

> **Invariant:**  
> `logout` es una **operación de dominio idempotente**.

Consecuencias:

- Ejecutar `logout` múltiples veces produce siempre el mismo estado final.
- Un logout sobre:
  - un token inválido,
  - una sesión inexistente,
  - o una sesión previamente revocada  
  **no debe producir error**.
- El dominio garantiza consistencia sin exponer estados intermedios a la aplicación.

---

### Responsabilidad de orquestación

- `AuthService` **orquesta** el caso de uso.
- `AuthSessionService` **encapsula** las reglas de dominio asociadas a sesiones.
- Ninguna aplicación consumidora debe:
  - revocar tokens manualmente,
  - interpretar estados de sesión,
  - ni duplicar estas reglas.

Estas invariantes son parte del contrato del framework.

### Evolución del modelo

Estas invariantes permanecen válidas incluso si:

- Se agregan nuevos tipos de token.
- Se introduce rotación de refresh tokens.
- Se incorporan múltiples dispositivos por sesión.
- Se implementa logout global o parcial.

Cualquier cambio que viole estas reglas constituye un **breaking change del dominio**.

