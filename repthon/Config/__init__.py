from .zq_lo_config import Config


def detect_platform():
    if os.getenv("DYNO"):
        return "𝙷𝚎𝚛𝚘𝚔𝚞"
    if os.getenv("RAILWAY_STATIC_URL"):
        return "𝚁𝚊𝚒𝚕𝚠𝚊𝚢"
    if os.getenv("RENDER_SERVICE_NAME"):
        return "𝚁𝚎𝚗𝚍𝚎𝚛"
    if os.getenv("OKTETO_TOKEN"):
        return "okteto"
    if os.getenv("KUBERNETES_PORT"):
        return "qovery | kubernetes"
    if os.getenv("RUNNER_USER") or os.getenv("HOSTNAME"):
        return "codespace" if os.getenv("USER") == "codespace" else "github actions"
    if os.getenv("ANDROID_ROOT"):
        return "termux"
    return "fly.io" if os.getenv("FLY_APP_NAME") else "local"

HOSTED_ON = detect_platform()
