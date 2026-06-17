from rtt.platform.linux_env import detect_linux_env

def run_doctor():
    print("=== rtt doctor ===")
    env = detect_linux_env()
    print(f"Session type  : {env.session_type}")
    print(f"Compositor    : {env.compositor}")
    print(f"PipeWire      : {env.pipewire_available}")
    print(f"Portal backend: {env.portal_backend}")
    print(f"Layer shell   : {env.layer_shell_available}")