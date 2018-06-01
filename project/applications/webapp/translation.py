from modeltranslation.translator import TranslationOptions, translator
from modeltranslation.decorators import register

from applications.webapp.models import Category


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', )


# translator.register(Category, CategoryTranslationOptions)
