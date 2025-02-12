import base64
from io import BytesIO
from PIL import Image


def convert_PIL_to_base64(image: Image, format="jpeg"):
    buffer = BytesIO()
    # Save the image to this buffer in the specified format
    image.save(buffer, format=format)
    # Get binary data from the buffer
    image_bytes = buffer.getvalue()
    # Encode binary data to Base64
    base64_encoded = base64.b64encode(image_bytes)
    # Convert Base64 bytes to string (optional)
    return base64_encoded.decode("utf-8")
