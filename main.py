from defs.json_data import save_raw_jsons
from defs.xml_data import download_resources
from defs.draw_data import download_images
from defs.path_data import create_path_data


async def main():
    await save_raw_jsons()
    await download_resources()
    await download_images()
    await create_path_data()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
