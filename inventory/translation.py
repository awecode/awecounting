from modeltranslation.translator import translator
from inventory.models import Unit, Item, Party
from app.translation import NameDescriptionTranslationOptions, NameTranslationOptions

translator.register(Unit, NameTranslationOptions)
translator.register(Item, NameDescriptionTranslationOptions)
translator.register(Party, NameTranslationOptions)

