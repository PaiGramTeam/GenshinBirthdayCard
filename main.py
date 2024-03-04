from defs.json_data import save_raw_jsons


async def main():
    await save_raw_jsons()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
