from defs.json_data import save_raw_jsons
from defs.xml_data import download_resources, convert_dialog_xml_json
from defs.draw_data import download_images
from defs.path_data import create_path_data
from defs.telegram_data import create_month_htmls


async def main():
    await save_raw_jsons()
    await download_resources()
    await download_images()
    await convert_dialog_xml_json()
    await create_path_data()
    await create_month_htmls()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
