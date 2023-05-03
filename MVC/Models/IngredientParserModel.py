import ast
import re
import string

import nltk
import unidecode
from nltk.stem import WordNetLemmatizer

class IngredientParserModel:
    def __init__(self):
        # list of measures for ingredients
        self.measures = ['teaspoon', 't', 'tsp.', 'tablespoon', 'T', 'tbl.', 'tb', 'tbsp.', 'fluid ounce', 'fl oz', 'gill',
                'cup', 'c', 'pint', 'p', 'pt', 'fl pt', 'quart', 'q', 'qt', 'fl qt', 'gallon', 'g', 'gal', 'ml',
                'milliliter', 'millilitre', 'cc', 'mL', 'l', 'liter', 'litre', 'L', 'dl', 'deciliter', 'decilitre',
                'dL', 'bulb', 'level', 'heaped', 'rounded', 'whole', 'pinch', 'medium', 'slice', 'pound', 'lb', '#',
                'ounce', 'oz', 'mg', 'milligram', 'milligramme', 'g', 'gram', 'gramme', 'kg', 'kilogram', 'kilogramme',
                'x', 'of', 'mm', 'millimetre', 'millimeter', 'cm', 'centimeter', 'centimetre', 'm', 'meter', 'metre',
                'inch', 'in', 'milli', 'centi', 'deci', 'hecto', 'kilo']
        # list of words to remove from ingredient strings
        self.words_to_remove = ['fresh', 'oil', 'a', 'red', 'bunch', 'and', 'clove', 'or', 'leaf', 'chilli', 'large', 'extra',
                       'sprig', 'ground', 'handful', 'free', 'small', 'pepper', 'virgin', 'range', 'from', 'dried',
                       'sustainable', 'black', 'peeled', 'higher', 'welfare', 'seed', 'for', 'finely', 'freshly', 'sea',
                       'quality', 'white', 'ripe', 'few', 'piece', 'source', 'to', 'organic', 'flat', 'smoked',
                       'ginger', 'sliced', 'green', 'picked', 'the', 'stick', 'plain', 'plus', 'mixed', 'mint', 'bay',
                       'basil', 'your', 'cumin', 'optional', 'fennel', 'serve', 'mustard', 'unsalted', 'baby',
                       'paprika', 'fat', 'ask', 'natural', 'skin', 'roughly', 'into', 'such', 'cut', 'good', 'brown',
                       'grated', 'trimmed', 'oregano', 'powder', 'yellow', 'dusting', 'knob', 'frozen', 'on',
                       'deseeded', 'low', 'runny', 'balsamic', 'cooked', 'streaky', 'nutmeg', 'sage', 'rasher', 'zest',
                       'pin', 'groundnut', 'breadcrumb', 'turmeric', 'halved', 'grating', 'stalk', 'light', 'tinned',
                       'dry', 'soft', 'rocket', 'bone', 'colour', 'washed', 'skinless', 'leftover', 'splash', 'removed',
                       'dijon', 'thick', 'big', 'hot', 'drained', 'sized', 'chestnut', 'watercress', 'fishmonger',
                       'english', 'dill', 'caper', 'raw', 'worcestershire', 'flake', 'cider', 'cayenne', 'tbsp', 'leg',
                       'pine', 'wild', 'if', 'fine', 'herb', 'almond', 'shoulder', 'cube', 'dressing', 'with', 'chunk',
                       'spice', 'thumb', 'garam', 'new', 'little', 'punnet', 'peppercorn', 'shelled', 'saffron',
                       'other''chopped', 'salt', 'olive', 'taste', 'can', 'sauce', 'water', 'diced', 'package',
                       'italian', 'shredded', 'divided', 'parsley', 'vinegar', 'all', 'purpose', 'crushed', 'juice',
                       'more', 'coriander', 'bell', 'needed', 'thinly', 'boneless', 'half', 'thyme', 'cubed',
                       'cinnamon', 'cilantro', 'jar', 'seasoning', 'rosemary', 'extract', 'sweet', 'baking', 'beaten',
                       'heavy', 'seeded', 'tin', 'vanilla', 'uncooked', 'crumb', 'style', 'thin', 'nut', 'coarsely',
                       'spring', 'chili', 'cornstarch', 'strip', 'cardamom', 'rinsed', 'honey', 'cherry', 'root',
                       'quartered', 'head', 'softened', 'container', 'crumbled', 'frying', 'lean', 'cooking', 'roasted',
                       'warm', 'whipping', 'thawed', 'corn', 'pitted', 'sun', 'kosher', 'bite', 'toasted', 'lasagna',
                       'split', 'melted', 'degree', 'lengthwise', 'romano', 'packed', 'pod', 'anchovy', 'rom',
                       'prepared', 'juiced', 'fluid', 'floret', 'room', 'active', 'seasoned', 'mix', 'deveined',
                       'lightly', 'anise', 'thai', 'size', 'unsweetened', 'torn', 'wedge', 'sour', 'basmati',
                       'marinara', 'dark', 'temperature', 'garnish', 'bouillon', 'loaf', 'shell', 'reggiano', 'canola',
                       'parmigiano', 'round', 'canned', 'ghee', 'crust', 'long', 'broken', 'ketchup', 'bulk', 'cleaned',
                       'condensed', 'sherry', 'provolone', 'cold', 'soda', 'cottage', 'spray', 'tamarind', 'pecorino',
                       'shortening', 'part', 'bottle', 'sodium', 'cocoa', 'grain', 'french', 'roast', 'stem', 'link',
                       'firm', 'asafoetida', 'mild', 'dash', 'boiling']
        # create a translation table to remove all punctuation from the string
        self.translator = str.maketrans('', '', string.punctuation)
        # create a WordNetLemmatizer object for lemmatization
        self.lemmatizer = WordNetLemmatizer()
        # create a set of stop words from the nltk library
        self.stop_words = set(nltk.corpus.stopwords.words('english'))

    def parse(self, ingredients):
        # check if ingredients is already a list, if not convert from string to list
        if isinstance(ingredients, list):
            ingredients = ingredients
        else:
            ingredients = ast.literal_eval(ingredients)
        # create an empty list to store cleaned ingredient names
        ingred_list = []
        # iterate through each ingredient
        for i in ingredients:
            # translate any special characters using self.translator
            i.translate(self.translator)
            # split ingredient name into individual words, using either spaces or hyphens as delimiters
            items = re.split(' |-', i)
            # keep only words that consist entirely of letters
            items = [word for word in items if word.isalpha()]
            # convert all words to lowercase
            items = [word.lower() for word in items]
            # remove any accents from letters
            items = [unidecode.unidecode(word) for word in items]
            # lemmatize all words (i.e. reduce them to their base form)
            items = [self.lemmatizer.lemmatize(word) for word in items]
            # remove any stop words (i.e. common words that are unlikely to be useful for recipe searches)
            items = [word for word in items if word not in self.stop_words]
            # remove any measure words (e.g. "teaspoon", "cup", etc.)
            items = [word for word in items if word not in self.measures]
            # remove any other words that the user has specified should be removed
            items = [word for word in items if word not in self.words_to_remove]
            # if there are any words left in the list, join them together with spaces and add to the final list of cleaned ingredient names
            if items:
                ingred_list.append(' '.join(items))
        # return the final list of cleaned ingredient names
        return ingred_list
