from datetime import datetime
from typing import TypedDict


type DatasetName = str
"""The name of the dataset in the Fivetran target"""

type DatetimeCursor = datetime
"""The datetime that Fivetran will use to increment the next fetch"""

type AttributeName = str
"""The name of the attribute in the Fivetran target"""

type JSON = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None
"""
A JSON serializable value

This recursive type definition is derived from this PEP discussion post:
https://github.com/python/typing/issues/182#issuecomment-1320974824
"""

type DataRecords = list[dict[AttributeName, JSON]]
"""The set of records to perform ingestion operations on"""

class PrimaryKeyDefinition(TypedDict):
    """
    The schema value to pass to define the primary key for a dataset
    """

    primary_key: list[AttributeName]
    """The attribute(s) that make up the primary key"""

type Schema = dict[DatasetName, PrimaryKeyDefinition]
"""The primary key specification for each entity"""


class FivetranResponse:
    """
    An HTTP response in the format of Fivetran's function connector response

    :param state: the updated state value(s)
    :type state: dict[DatasetName, DatetimeCursor]
    :param has_more: boolean indicator for Fivetran to make a follow-up call
    :type has_more: bool
    :param insert: the entities and records to be inserted
    :type insert: dict[DatasetName, DataRecords]
    :param delete: the entities and records to be marked as deleted
    :type delete: dict[DatasetName, DataRecords] | None
    :param schema: specifies primary key columns for each entity
    :type schema: Schema | None
    :param soft_delete: specifies the list of entities to be soft deleted
    :type soft_delete: list[DatasetName] | None
    """

    def __init__(
        self,
        state: dict[DatasetName, DatetimeCursor],
        has_more: bool,
        insert: dict[DatasetName, DataRecords] = {},
        delete: dict[DatasetName, DataRecords] | None = None,
        schema: Schema | None = None,
        soft_delete: list[DatasetName] | None = None
    ) -> None:
        """Initializes the `FivetranResponse` class"""

        self.state = state
        self.has_more = has_more
        self.insert = insert
        self.delete = delete
        self.schema = schema
        self.soft_delete = soft_delete


    def _construct_body(self) -> None:
        body = {
            'state': self.state,
            'hasMore': self.has_more,
            'insert': self.insert
        }

        if self.delete:
            body['delete'] = self.delete
        if self.schema:
            body['schema'] = self.schema
        if self.soft_delete:
            body['softDelete'] = self.soft_delete
        
        self.body = body