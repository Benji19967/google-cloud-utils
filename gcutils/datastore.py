from typing import Any

from google.cloud.datastore import Client, Entity, Key

from gcutils.exceptions import EntityNotFound


class DSutils:
    def __init__(self, client: Client) -> None:
        self._client: Client = client
        if not self._client.project:
            raise ValueError("`project` needs to be set for Client")

    def get_entity(self, kind: str, id: int | str) -> Entity:
        key = self._client.key(kind, id)  # type: ignore
        return self.get_entity_by_key(key=key)

    def get_entity_by_key(self, key: Key) -> Entity:
        entity: Entity | None = self._client.get(key=key)  # type: ignore
        if not entity:
            raise EntityNotFound(f"Could not find entity with key: {key}")
        return entity

    def get_entities(
        self, keys: list[Key], missing: list[Any] | None = None
    ) -> list[Entity]:
        if missing != []:
            raise ValueError("Missing list must initially be empty")
        entites: list[Entity] = self._client.get_multi(keys=keys, missing=missing)  # type:ignore
        return entites

    def put(self, entity: Entity) -> None:
        self._client.put(entity=entity)  # type: ignore

    def put_multi(self, entities: list[Entity]) -> None:
        self._client.put_multi(entities=entities)  # type: ignore

    def delete(self, key: Key) -> None:
        self._client.delete(key=key)  # type: ignore

    def delete_multi(self, keys: list[Key]) -> None:
        self._client.delete_multi(keys=keys)  # type: ignore

    def create_complete_keys(self, incomplete_key: Key, num_keys: int) -> list[Key]:
        """
        Incomplete/Partial Key: a Key without an ID/name
        """
        complete_keys: list[Key] = self._client.allocate_ids(
            incomplete_key=incomplete_key, num_ids=num_keys
        )  # type: ignore
        return complete_keys
