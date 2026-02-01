import aiohttp
import os
import asyncio

async def download_catbox_file(url: str, save_path: str) -> bool:
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(save_path, 'wb') as f:
                        while True:
                            chunk = await response.content.read(8192)
                            if not chunk:
                                break
                            f.write(chunk)
                    return True
                else:
                    print(f"خطأ في التحميل: كود الحالة {response.status}")
                    return False
    except aiohttp.ClientError as e:
        print(f"خطأ في الاتصال: {e}")
        return False
    except Exception as e:
        print(f"خطأ غير متوقع: {e}")
        return False
