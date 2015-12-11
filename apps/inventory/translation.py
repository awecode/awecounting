from modeltranslation.translator import translator

from apps.inventory.models import Unit, Item, Party
from awecounting.utils.translation import NameDescriptionTranslationOptions, NameTranslationOptions

translator.register(Unit, NameTranslationOptions)
translator.register(Item, NameDescriptionTranslationOptions)
translator.register(Party, NameTranslationOptions)

