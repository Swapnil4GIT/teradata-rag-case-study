from dataclasses import dataclass, fields


@dataclass
class SchemaClass:
    pass

    @classmethod
    def from_dict(cls, raw_dict: dict[str, str]) -> "SchemaClass":
        return cls(
            **{k: v for k, v in raw_dict.items() if k in {f.name for f in fields(cls)}}
        )


@dataclass
class PredictRequest(SchemaClass):
    session_id: str
    query_id: str
    query: str
