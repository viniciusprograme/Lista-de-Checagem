#!/usr/bin/env python3
"""
Debug helper: import and run `create_app()` to capture startup traceback and key env/config values.
Run locally: `python scripts/debug_create_app.py`
"""
import sys
import os
import traceback


def print_mod_version(name):
    try:
        m = __import__(name)
        ver = getattr(m, "__version__", None)
        print(f"{name}: OK, version={ver}")
    except Exception as e:
        print(f"{name}: import failed: {e}")


def main():
    print("Python:", sys.version)
    print("Working dir:", os.getcwd())
    try:
        print("Files:", ", ".join(sorted(os.listdir("."))[:50]))
    except Exception:
        pass

    # Config quick-inspect
    try:
        import config
        print("SQLALCHEMY_DATABASE_URI:", getattr(config, "SQLALCHEMY_DATABASE_URI", None))
        print("REDIS_URL:", getattr(config, "REDIS_URL", None))
        print("PORT:", getattr(config, "PORT", None))
    except Exception as e:
        print("Failed to import config:", e)
        traceback.print_exc()

    # Try creating the Flask app and list blueprints / url map
    try:
        from app import create_app
        app = create_app()
        print("create_app OK")
        print("Registered blueprints:", list(app.blueprints.keys()))
        try:
            rules = [str(r) for r in app.url_map.iter_rules()]
            print("URL map (sample):")
            for r in rules[:50]:
                print(" ", r)
        except Exception:
            pass
    except Exception:
        print("create_app raised exception:")
        traceback.print_exc()

    # Check important modules
    for mod in ("psycopg", "psycopg2", "flask_sqlalchemy", "flask", "sqlalchemy"):
        print_mod_version(mod)


if __name__ == "__main__":
    main()
