import aiohttp
import os

async def catbox_upload(file_path: str) -> str:
    """
    رفع ملف إلى Catbox (وظيفة احتياطية) @Repthon
    """
    try:
        if not os.path.exists(file_path):
            return None
        file_ext = os.path.splitext(file_path)[1].lower()
        content_types = {
            '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
            '.png': 'image/png', '.gif': 'image/gif',
            '.webp': 'image/webp', '.bmp': 'image/bmp'
        }
        content_type = content_types.get(file_ext, 'image/jpeg')
        url = "https://catbox.moe/user/api.php"
        with open(file_path, 'rb') as f:
            file_data = f.read()
        data = aiohttp.FormData()
        data.add_field('reqtype', 'fileupload')
        data.add_field('fileToUpload', file_data,
                      filename=os.path.basename(file_path),
                      content_type=content_type)
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, data=data) as response:
                if response.status == 200:
                    result = (await response.text()).strip()
                    
                    if result.startswith('http'):
                        return result
                    elif 'catbox.moe' in result:
                        return f"https://{result}" if not result.startswith('http') else result
                    elif result and '.' in result:
                        return f"https://files.catbox.moe/{result}"
                return None
    except Exception:
        return None
