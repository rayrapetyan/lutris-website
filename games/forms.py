"""Forms for the main app"""
# pylint: disable=W0232, R0903
import yaml
from django_jcrop.forms import JCropImageWidget
from django import forms
import models


class NewsForm(forms.ModelForm):
    class Meta:
        model = models.News
        exclude = ('slug', )

class GameForm(forms.ModelForm):
    title_logo = forms.ImageField(
        widget=JCropImageWidget
    )

    class Meta:
        model = models.Game
        exclude = ('slug', )


class ScreenshotForm(forms.ModelForm):

    class Meta:
        model = models.Screenshot
        exclude = ['game', 'uploaded_at', 'uploaded_by']

    def __init__(self, *args, **kwargs):
        self.game = models.Game.objects.get(pk=kwargs.pop('game_id'))
        super(ScreenshotForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance['game'] = self.game
        return super(ScreenshotForm, self).save(*args, **kwargs)


class InstallerForm(forms.ModelForm):
    """Form to create and modify installers"""

    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'code-editor',
                                     'spellcheck': 'false'})
    )

    class Meta:
        """Form configuration"""
        model = models.Installer
        exclude = ("user", "slug", "game")

    def clean_content(self):
        """Verify that the content field is valid yaml"""
        yaml_data = self.cleaned_data["content"]
        try:
            yaml_data = yaml.load(yaml_data)
        except yaml.scanner.ScannerError:
            raise forms.ValidationError("Invalid YAML data (scanner error)")
        except yaml.parser.ParserError:
            raise forms.ValidationError("Invalid YAML data (parse error)")
        return yaml.dump(yaml_data, default_flow_style=False)
