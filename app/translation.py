from modeltranslation.translator import TranslationOptions, register
from inventory.models import Unit

# @register(Unit)
class NameTranslationOptions(TranslationOptions):
	fields = ('name',)

class NameDescriptionTranslationOptions(TranslationOptions):
	fields = ('name', 'description', )