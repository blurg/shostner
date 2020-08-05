from typing import List

def id_to_str(value: dict) -> dict:
    value["id"] = str(value.pop("_id"))
    return value

async def clean_ids_from_list(value: List[dict]) -> List[dict]:
    return [id_to_str(doc) async for doc in value]