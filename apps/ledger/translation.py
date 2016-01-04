from modeltranslation.translator import translator

from .models import Party
from awecounting.utils.translation import NameTranslationOptions

translator.register(Party, NameTranslationOptions)
