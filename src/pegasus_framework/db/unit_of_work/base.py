# Copyright (c) 2025 balerdis
# pegasus_framework/db/unit_of_work/base.py
from abc import ABC, abstractmethod
from typing import Type, Dict

class UnitOfWork(ABC):
    _repo_bindings: Dict[Type, Type] = {}


    @classmethod
    def bind_repository(cls, abstraction: Type, implementation: Type) -> None:
        """Este metodo vincula una implementación con una abstraccion, aplica al caso 
        en el que el authSessionService requiere del repository que vive en la app y 
        eso rompe la regla arquitectonica de que el framework no debe depender de la app

        Para resolverlo, se utiliza en el wiring de la app, el vinculo bindding entre
        SessionRepository y SqlAlchemySessionRepository, donde SessionRepository es
        el contrato abstracto (eso vive en el framework y no hay problema de apuntarlo desde
        el framework), sin embargo SqlAlchemySessionRepository vive en la app, entonces 
        sin este vinculo, cuando authSessionService intenta utilizar el SessionRepository
        via la UnitOfWork, no puede funcionar porque SessionRepository es una abstraccion.

        La manera de resolverlo es, permitiendo a la UoW permitir hacer ese vinculo (ya que 
        es el encargado de generar instanciar los repositories) aprovechando esa responsabilidad
        que ya tiene, le delegamos el bind entre la abstraccion y la implementacion. Y si a eso
        le agregamos que al momento de iniciar la app se llame a bind_repository para vincular la
        abstraccion y la implementacion, entonces el vinculo ya estara hecho para cuando desde 
        el framework se llame a la abstraccion, la UoW que ya le dijeron en el boostrap de la app
        como es ese vinculo, cuando lo invoco con la abstraccion, la UoW me va a dar la implementacion.
        Todo esto funciona tanto cuando existe un bind en el wiring de la app como cuando no, 
        porque en el metodo resolve_repository, se utiliza el metodo get de los dict de python, 
        si la clave no esta en el diccionario, te devuelve el mismo valor que le pasaste, 
        es decir, la abstraccion. Y en el caso de se use este metodo en la app, te va a devolver 
        el mismo parametro que le pasaste., con lo cual funciona para ambos sentidos.

        Args:
            abstraction (Type): Abstraccion de un repository a vincular
            implementation (Type): Implementacion de un repository a vincular
        """
        cls._repo_bindings[abstraction] = implementation

    def resolve_repository(self, repo_cls: Type) -> Type:
        """Este metodo es clave para resolver tanto los casos en que el repository viva en la 
        app y el service en el framework (ya que el framework no depende de la app), como 
        tambien los casos en que el repository viva en el framework y el service en la app, como 
        tambien los casos en que tanto el repository y el service viven en el framework o en la app.
        usamos el metodo get de un dict, donde el segundo parametro te lo da si la clave no esta en el dict

        Args:
            repo_cls (Type): repository del que se quiere obtener una equivalencia en la UoW

        Returns:
            Type: equivalencia determinada por la UoW, que es la que se encarga de resolver
        """
        return self._repo_bindings.get(repo_cls, repo_cls)

    @abstractmethod
    def commit(self) -> None:
        ...

    @abstractmethod
    def rollback(self) -> None:
        ...

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type:
            self.rollback()
