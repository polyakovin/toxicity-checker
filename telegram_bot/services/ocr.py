from io import BytesIO
from PIL import Image
import pytesseract
from loguru import logger


def extract_text_from_image(image_bytes: bytes) -> str:
    image = Image.open(BytesIO(image_bytes))

    width, height = image.size
    if max(width, height) > 3000:
        ratio = 3000 / max(width, height)
        image = image.resize((int(width * ratio), int(height * ratio)), Image.LANCZOS)

    try:
        text = pytesseract.image_to_string(image, lang="rus+eng", config="--psm 6")
    except Exception:
        logger.warning("Tesseract rus+eng failed, falling back to eng")
        text = pytesseract.image_to_string(image, lang="eng", config="--psm 6")

    return text.strip()
