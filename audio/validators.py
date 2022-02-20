from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile


class FileSizeValidator:
    def __init__(self, val: float, byte_type="mb"):
        assert byte_type in ["b", "kb", "mb"]
        if byte_type == "b":
            self._upper_byte_size = val
        elif byte_type == "kb":
            self._upper_byte_size = 1000 * val
        elif byte_type == "mb":
            self._upper_byte_size = (1000 ** 2) * val
        elif byte_type == "gb":
            self._upper_byte_size = (1000 ** 3) * val
        self._err_message = f"アップロードファイルは{val}{byte_type.upper()}未満にしてください"

    def __call__(self, file_val: UploadedFile):
        byte_size = file_val.size
        if byte_size > self._upper_byte_size:
            raise ValidationError(message=self._err_message)
