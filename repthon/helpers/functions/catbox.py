import aiohttp
import os

async def catbox_upload(file_path):
    """
    رفع ملف إلى Catbox (وظيفة احتياطية) @Repthon
    """
    import aiohttp
    import os
    
    try:
        if not os.path.exists(file_path):
            return None
        
        url = "https://catbox.moe/user/api.php"
        
        data = aiohttp.FormData()
        data.add_field('reqtype', 'fileupload')
        
        with open(file_path, 'rb') as f:
            data.add_field('fileToUpload', 
                          f.read(),
                          filename=os.path.basename(file_path),
                          content_type='image/jpeg')
        
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, data=data) as response:
                if response.status == 200:
                    result = await response.text()
                    result = result.strip()
                    if result.startswith('http'):
                        return result
                    elif 'catbox.moe' in result:
                        return result
                    elif len(result) > 0:
                        return f"https://files.catbox.moe/{result}"
                return None
                
    except Exception as e:
        print(f"خطأ في الرفع: {e}")
        return None
