from app.modules.core import ALL_18_MODULES


if __name__ == "__main__":
    print("Ruby YouTube Revenue Engine")
    print(f"Registered logic modules: {len(ALL_18_MODULES)}")
    for name in ALL_18_MODULES:
        print(f"- {name}")
