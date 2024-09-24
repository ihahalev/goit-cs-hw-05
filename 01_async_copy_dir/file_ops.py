from aiopath import AsyncPath
from aioshutil import copyfile
from logger import logging

async def read_folder(from_dir: AsyncPath, dest_dir: AsyncPath):
    """reads content of folder and checks all if file or directory

    Args:
        from_dir (AsyncPath): folder being looke in
        dest_dir (AsyncPath): folder, where extention folders are created and files are copied by extention
    """
    try:
        if (not await from_dir.exists()
            or not await from_dir.is_dir()):
            logging.error("Not directory or does not exitsts")
            return
        async for path in from_dir.iterdir():
            if await path.is_dir():
                await read_folder(path, dest_dir)
            elif await path.is_file():
                await copy_file(path, dest_dir)
            else:
                logging.error(f"In {from_dir.name} unknown entity: {path.name}")
    except Exception as e:
        logging.error(f"Error while file/directory read operation: {e}")

async def copy_file(file: AsyncPath, dest_dir: AsyncPath):
    """creates if needed extention folder and copies file to there

    Args:
        file (AsyncPath): file to be copied
        dest_dir (AsyncPath): folder, where extention folders are created and files are copied by extention
    """
    try:
        ext = file.suffix[1:]
        if not ext:
            logging.warning(f"File '{file.name}' has no extention, will be copies in root")
        # even file has no extention, no changes needed, it will use only dest_dir
        ext_dir = dest_dir/ext
        await ext_dir.mkdir(parents=True, exist_ok=True)
        await copyfile(file, ext_dir / file.name)
        logging.info(f"File '{file.name}' has been copied to '{dest_dir.name}/{ext}'")
    except Exception as e:
        logging.error(f"Error while file copy operation: {e}")
