from pathlib import Path

from PIL import Image


SOURCE_IMAGE = Path("assets/logo.png")
OUTPUT_ICON = Path("assets/app.ico")
ICON_SIZES = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]


def main():
    if not SOURCE_IMAGE.exists():
        raise FileNotFoundError(
            "Salve a logo em assets/logo.png antes de gerar o icone."
        )

    OUTPUT_ICON.parent.mkdir(parents=True, exist_ok=True)
    image = Image.open(SOURCE_IMAGE).convert("RGBA")
    image.save(OUTPUT_ICON, sizes=ICON_SIZES)
    print(f"Icone gerado em {OUTPUT_ICON}")


if __name__ == "__main__":
    main()
