import aiohttp
from loguru import logger

PUBCHEM_BASE = "https://pubchem.ncbi.nlm.nih.gov/rest"


async def search_substance(query: str) -> dict | None:
    url = f"{PUBCHEM_BASE}/pug/compound/name/{query}/JSON"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
    except Exception as e:
        logger.warning(f"PubChem search failed for '{query}': {e}")
        return None

    props = data.get("PC_Compounds", [])
    if not props:
        return None

    compound = props[0]
    result = {}

    for prop in compound.get("props", []):
        label = prop.get("urn", {}).get("label", "")
        value = prop.get("value", {})
        if label == "IUPAC Name" and "sval" in value:
            result["iupac_name"] = value["sval"]
        if label == "Molecular Formula" and "sval" in value:
            result["formula"] = value["sval"]
        if label == "Molecular Weight" and "fval" in value:
            result["molecular_weight"] = value["fval"]

    return result if result else None
