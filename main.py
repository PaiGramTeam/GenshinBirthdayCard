from defs.json_data import save_raw_jsons
from defs.xml_data import download_resources


async def main():
    # await save_raw_jsons()
    await download_resources()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
