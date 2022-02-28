
from django import forms

from audio.models import AudioFile
from audio.validators import FileSizeValidator


class AudioFileForm(forms.ModelForm):
    file = forms.FileField(
        validators=[FileSizeValidator(val=200, byte_type="mb")],
        required=True,
    )
    meeting_uuid = forms.CharField(required=True)

    class Meta:
        model = AudioFile
        fields = ('file',)
