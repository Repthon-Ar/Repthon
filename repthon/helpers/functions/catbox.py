import aiohttp
import os

async def catbox_upload(file_path):
    """
    Repthon
    """
    try:
        url = "https://catbox.moe/user/api.php"
        
        data = aiohttp.FormData()
        data.add_field('reqtype', 'fileupload')
        
        with open(file_path, 'rb') as file:
            data.add_field('fileToUpload', file, filename=os.path.basename(file_path))
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    return None
                    
    except Exception as e:
        print(f"Error uploading to Catbox: {e}")
        return None
