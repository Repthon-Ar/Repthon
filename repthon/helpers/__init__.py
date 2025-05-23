from . import fonts  # noqa F401
from . import memeshelper as catmemes  # noqa F401
from .aiohttp_helper import AioHttp  # noqa F401
from .utils import *

flag = True
check = 0
while flag:
    try:
        from .chatbot import *
        from .functions import *
        from .memeifyhelpers import *
        from .progress import *
        from .qhelper import *
        from .tools import *
        from .utils import _reputils, _reptools, _format  # noqa F401

        break
    except ModuleNotFoundError as e:
        install_pip(e.name)
        check += 1
        if check > 5:
            break
