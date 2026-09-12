from __future__ import annotations

import server_dynamic_maps as _dynamic
import server_pets as _pets
from pet_core_bridge import install_pet_core_bridge


def install_pet_system() -> None:
    """Install the phone-verified base pet bridge, then independent pet domains."""
    _pets.install_pet_support()
    install_pet_core_bridge()


def main() -> None:
    install_pet_system()
    _dynamic.main()


if __name__ == '__main__':
    main()
