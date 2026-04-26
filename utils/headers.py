def clean_heading(name, lang):
    # 17/04/2026. Some of the field names in the database don't make
    # good column headers on the reference tables. This function provides
    # more fitting substitutes.
    # 18/04/2026. Expanded dictionary.
    
    replacements = {
        'gender_name': 'gender',
        'lemma': get_language(lang),
        'masculine_form': 'masculine',
        'feminine_form': 'feminine',
        'neuter_form': 'neuter',
        'plural_form': 'plural',
        }
    return replacements.get(name,name)

def get_language(code):
    language_dict = {
        "DE": "German",
        "ES": "Spanish",
        "FR": "French",
        "IT": "Italian"
    }
    return language_dict[code]
