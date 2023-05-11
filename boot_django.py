from pathlib import Path

import django
from django.conf import settings


BASE_DIR = Path(__file__).resolve().parent.parent


def boot_django():
    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        },
        INSTALLED_APPS=(
            "tracking",
        ),
        TIME_ZONE="UTC",
        USE_TZ=True,
    )
    django.setup()
