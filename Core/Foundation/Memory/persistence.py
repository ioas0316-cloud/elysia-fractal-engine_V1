import json

from pathlib import Path

from typing import Any, Dict, Optional



import numpy as np

from scipy.sparse import csr_matrix



from world import World

from Legacy.Project_Sophia.wave_mechanics import WaveMechanics



STATE_PATH = Path("saves/world_state.json")





def _array_to_list(value: Optional[np.ndarray]) -> list:

    if value is None:

        return []

    return value.tolist()





def _list_to_array(value: Optional[list], dtype: Any) -> np.ndarray:

    if not value:

        return np.array([], dtype=dtype)

    return np.array(value, dtype=dtype)





def _csr_to_dict(matrix: csr_matrix) -> Dict[str, Any]:

    if matrix is None:

        return {"data": [], "indices": [], "indptr": [], "shape": (0, 0)}

    csr = matrix.tocsr()

    return {

        "data": csr.data.tolist(),

        "indices": csr.indices.tolist(),

        "indptr": csr.indptr.tolist(),

        "shape": tuple(csr.shape),

    }





def _csr_from_dict(data: Dict[str, Any]) -> csr_matrix:

    if not data:

        return csr_matrix((0, 0), dtype=np.float32)

    return csr_matrix(

        (data["data"], data["indices"], data["indptr"]),

        shape=tuple(data["shape"]),

    )





def save_world_state(world: World, path: Optional[str] = None) -> None:

    dest = Path(path or STATE_PATH)

    dest.parent.mkdir(parents=True, exist_ok=True)



    state: Dict[str, Any] = {

        "time_step": int(world.time_step),

        "day_length": world.day_length,

        "time_of_day": world.time_of_day,

        "oxygen_level": world.oxygen_level,

        "branch_id": world.branch_id,

        "parent_event_id": world.parent_event_id,

        "cell_ids": list(world.cell_ids),

        "id_to_idx": world.id_to_idx,

        "quantum_states": {

            k: v for k, v in getattr(world, "quantum_states", {}).items()

        },

        "arrays": {

            "is_alive_mask": _array_to_list(world.is_alive_mask),

            "hp": _array_to_list(world.hp),

            "max_hp": _array_to_list(world.max_hp),

            "ki": _array_to_list(world.ki),

            "max_ki": _array_to_list(world.max_ki),

            "mana": _array_to_list(world.mana),

            "max_mana": _array_to_list(world.max_mana),

            "faith": _array_to_list(world.faith),

            "max_faith": _array_to_list(world.max_faith),

            "strength": _array_to_list(world.strength),

            "agility": _array_to_list(world.agility),

            "intelligence": _array_to_list(world.intelligence),

            "vitality": _array_to_list(world.vitality),

            "wisdom": _array_to_list(world.wisdom),

            "hunger": _array_to_list(world.hunger),

            "temperature": _array_to_list(world.temperature),

            "satisfaction": _array_to_list(world.satisfaction),

            "connection_counts": _array_to_list(world.connection_counts),

            "element_types": list(world.element_types),

            "diets": list(world.diets),

            "growth_stages": _array_to_list(world.growth_stages),

            "mating_readiness": _array_to_list(world.mating_readiness),

            "age": _array_to_list(world.age),

            "max_age": _array_to_list(world.max_age),

            "is_injured": _array_to_list(world.is_injured),

            "is_meditating": _array_to_list(world.is_meditating),

            "positions": [list(row) for row in world.positions.tolist()]

            if world.positions.size

            else [],

            "labels": list(world.labels),

            "insight": _array_to_list(world.insight),

            "emotions": list(world.emotions),

            "continent": list(world.continent),

            "culture": list(world.culture),

            "affiliation": list(world.affiliation),

        },

        "adjacency": _csr_to_dict(world.adjacency_matrix),

    }



    with dest.open("w", encoding="utf-8") as f:

        json.dump(state, f, ensure_ascii=False, indent=2)





def _apply_state(world: World, data: Dict[str, Any]) -> None:

    world.time_step = data.get("time_step", world.time_step)

    world.day_length = data.get("day_length", world.day_length)

    world.time_of_day = data.get("time_of_day", world.time_of_day)

    world.oxygen_level = data.get("oxygen_level", world.oxygen_level)

    world.branch_id = data.get("branch_id", world.branch_id)

    world.parent_event_id = data.get("parent_event_id", world.parent_event_id)

    cell_ids = data.get("cell_ids", [])

    world.cell_ids = list(cell_ids)

    world.id_to_idx = {cid: idx for idx, cid in enumerate(world.cell_ids)}

    world.quantum_states = data.get("quantum_states", {})



    arrays = data.get("arrays", {})

    world.is_alive_mask = _list_to_array(arrays.get("is_alive_mask", []), dtype=bool)

    world.hp = _list_to_array(arrays.get("hp", []), dtype=np.float32)

    world.max_hp = _list_to_array(arrays.get("max_hp", []), dtype=np.float32)

    world.ki = _list_to_array(arrays.get("ki", []), dtype=np.float32)

    world.max_ki = _list_to_array(arrays.get("max_ki", []), dtype=np.float32)

    world.mana = _list_to_array(arrays.get("mana", []), dtype=np.float32)

    world.max_mana = _list_to_array(

        arrays.get("max_mana", []), dtype=np.float32

    )

    world.faith = _list_to_array(arrays.get("faith", []), dtype=np.float32)

    world.max_faith = _list_to_array(

        arrays.get("max_faith", []), dtype=np.float32

    )

    world.strength = _list_to_array(arrays.get("strength", []), dtype=np.int32)

    world.agility = _list_to_array(arrays.get("agility", []), dtype=np.int32)

    world.intelligence = _list_to_array(

        arrays.get("intelligence", []), dtype=np.int32

    )

    world.vitality = _list_to_array(arrays.get("vitality", []), dtype=np.int32)

    world.wisdom = _list_to_array(arrays.get("wisdom", []), dtype=np.int32)

    world.hunger = _list_to_array(arrays.get("hunger", []), dtype=np.float32)

    world.temperature = _list_to_array(

        arrays.get("temperature", []), dtype=np.float32

    )

    world.satisfaction = _list_to_array(

        arrays.get("satisfaction", []), dtype=np.float32

    )

    world.connection_counts = _list_to_array(

        arrays.get("connection_counts", []), dtype=np.int32

    )

    world.element_types = np.array(arrays.get("element_types", []), dtype="<U20")

    world.diets = np.array(arrays.get("diets", []), dtype="<U10")

    world.growth_stages = _list_to_array(

        arrays.get("growth_stages", []), dtype=np.int8

    )

    world.mating_readiness = _list_to_array(

        arrays.get("mating_readiness", []), dtype=np.float32

    )

    world.age = _list_to_array(arrays.get("age", []), dtype=np.int32)

    world.max_age = _list_to_array(arrays.get("max_age", []), dtype=np.int32)

    world.is_injured = _list_to_array(arrays.get("is_injured", []), dtype=bool)

    world.is_meditating = _list_to_array(

        arrays.get("is_meditating", []), dtype=bool

    )

    positions = arrays.get("positions", [])

    world.positions = (

        np.array(positions, dtype=np.float32)

        if positions

        else np.zeros((0, 3), dtype=np.float32)

    )

    world.labels = np.array(arrays.get("labels", []), dtype="<U20")

    world.insight = _list_to_array(arrays.get("insight", []), dtype=np.float32)

    world.emotions = np.array(arrays.get("emotions", []), dtype="<U10")

    world.continent = np.array(arrays.get("continent", []), dtype="<U10")

    world.culture = np.array(arrays.get("culture", []), dtype="<U10")

    world.affiliation = np.array(arrays.get("affiliation", []), dtype="<U20")



    world.adjacency_matrix = _csr_from_dict(data.get("adjacency", {}))

    world.materialized_cells = {}

    world.graveyard = []





def load_world_state(

    path: Optional[str] = None,

    *,

    world: Optional[World] = None,

    primordial_dna: Optional[Dict[str, Any]] = None,

    wave_mechanics: Optional[WaveMechanics] = None,

    logger: Optional[Any] = None,

) -> World:

    source = Path(path or STATE_PATH)

    if not source.exists():

        raise FileNotFoundError(f"World save file not found: {source}")



    data = json.loads(source.read_text(encoding="utf-8"))



    if world is None:

        if wave_mechanics is None or primordial_dna is None:

            raise ValueError(

                "WaveMechanics and primordial_dna must be provided when creating a new world instance."

            )

        world = World(

            primordial_dna=primordial_dna,

            wave_mechanics=wave_mechanics,

            logger=logger,

        )

    elif wave_mechanics is not None:

        world.wave_mechanics = wave_mechanics



    _apply_state(world, data)

    return world

