import os
import platform
from pathlib import Path

from dotenv import load_dotenv


def setup_tidy3d():

    print("=" * 55)
    print("Tidy3D / PhotonForge Environment Setup")
    print("=" * 55)

    # Locate .env alongside this script
    script_dir = Path(__file__).resolve().parent
    env_file = script_dir / ".env"

    if not env_file.is_file():
        raise FileNotFoundError(
            f".env file not found: {env_file}"
        )

    # Load environment variables
    load_dotenv(env_file, override=True)

    api_key = os.getenv("apikey") or os.getenv("SIMCLOUD_APIKEY")

    if not api_key:
        raise RuntimeError(
            "API key not found. Check that .env contains "
            "apikey=YOUR_API_KEY"
        )

    # Make key available to Tidy3D
    os.environ["SIMCLOUD_APIKEY"] = api_key

    print("API key loaded from .env")

    # Configure Tidy3D
    import tidy3d.web as web

    web.configure(api_key)

    # Create legacy configuration
    legacy_dir = Path.home() / ".tidy3d"
    legacy_dir.mkdir(parents=True, exist_ok=True)

    legacy_file = legacy_dir / "config"

    legacy_file.write_text(
        f'apikey = "{api_key}"\n',
        encoding="utf-8"
    )

    if platform.system() != "Windows":
        os.chmod(legacy_dir, 0o700)
        os.chmod(legacy_file, 0o600)

    print("Modern Tidy3D configuration updated.")
    print("Legacy Tidy3D configuration updated.")

    # Verify configuration
    from tidy3d import config

    # Authenticate
    print("Testing Tidy3D authentication...")

    web.test()

    print("\nSUCCESS: Tidy3D authentication passed.")

    # Check PhotonForge
    import photonforge as pf

    print("PhotonForge imported successfully.")

    print("\n" + "=" * 55)
    print("Environment ready for Jupyter simulations.")
    print("=" * 55)

    return True


if __name__ == "__main__":
    setup_tidy3d()