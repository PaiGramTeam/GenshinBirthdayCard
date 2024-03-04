from defs.json_data import save_raw_jsons
from defs.xml_data import download_resources
from defs.draw_data import download_images


async def main():
    await save_raw_jsons()
    await download_resources()
    await download_images()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
