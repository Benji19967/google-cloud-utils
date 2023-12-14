from typing import Any

from google.cloud.datastore import Client, Entity, Key

from gcutils.exceptions import EntityNotFound


class DSutils:
    def __init__(self, client: Client) -> None:
        self._client: Client = client
        if not self._client.project:
            raise ValueError("`project` needs to be set for Client")

    def get_entity_by_key(self, key: Key) -> Entity:
        entity: Entity | None = self._client.get(key=key)  # type: ignore
        if not entity:
            raise EntityNotFound(f"Could not find entity with key: {key}")
        return entity

    def get_entity(self, kind: str, id: int | str) -> Entity:
        key = self._client.key(kind, id)  # type: ignore
        return self.get_entity_by_key(key=key)

    def get_entities(
        self, keys: list[Key], missing: list[Any] | None = None
    ) -> list[Entity]:
        if missing != []:
            raise ValueError("Missing list must initially be empty")

        entites: list[Entity] = self._client.get_multi(keys=keys, missing=missing)  # type:ignore
        return entites
