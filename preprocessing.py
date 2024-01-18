from io import BytesIO
import base64

from PIL import Image


def preprocess_image(input: str | bytes) -> Image:
    """Converts base64 image (bytes or string) to PIL Image"""
    binary_data = base64.b64decode(input)
    output = Image.open(BytesIO(binary_data))
    return output
