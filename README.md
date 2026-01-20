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
└── src/
    └── pegasus_framework/
        ├── api/       # componentes HTTP reutilizables
        ├── auth/      # autenticación y seguridad
        ├── business/  # módulos de negocio reutilizables
        ├── core/      # utilidades transversales
        ├── db/        # base de datos, repositorios, UoW
        └── wiring/    # providers y bootstrap
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

# 14. Limitaciones generales en la capa de middleware
 - AuthContextMiddleware: Extraer y normalizar identidad técnica del request para consumo por otros middlewares (rate-limit, logging, métricas). No es un middleware de autenticación (No autentica, no autoriza, no valida tokens).
 - Nunca validar sesión en middleware
 - Nunca acceder a DB desde middleware
 - Nunca usar user_id
 - Nunca loggear tokens
 - Solo hashes / fingerprints
 - Fallar rápido (429)
