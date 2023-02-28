import re


def get_user_age(age):
    if age < 20:
        age_str = 'under 20'
    elif age >= 20 and age <= 30:
        age_str = '20-30'
    elif age > 30:
        age_str = 'over 30'
    
    return age_str

def get_user_gender(gender):
    if gender == 'F':
        gender_str = 'women'
    elif gender == 'M':
        gender_str = 'men'
    
    return gender_str

def get_item_actor(actors):
    actors = actors.strip('[').strip(']').replace("'","").split(',')
    actors = [actor.strip().strip('"') for actor in actors]
    

    return actors

def get_item_genre(genre):
    genre = genre.split("|")
    genre = [gen.lower() for gen in genre]

    return genre

def modify_country(country):
    country_dict = {'Australia': 'Australian', 'United States': 'American',
                    'Japan': 'Japanese', 'United Kingdom': 'British',
                    'Mexico': 'Mexican', 'Italy': 'Italian',
                    'France': 'French', 'Germany': 'German',
                    'Brazil': 'Brazilian', 'Spain': 'Spanish',
                    'Netherlands': 'Dutch', 'Canada': 'Canadian',
                    'Hong Kong': 'Hong Kong', 'Cuba': 'Cuban',
                    'Monaco': 'Monaco', 'Belgium': 'Belgian',
                    'Czech Republic': 'Czech', 'West Germany': 'West German',
                    'Ireland': 'Irish', 'Soviet Union': 'Soviet Union',
                    'New Zealand': 'New Zealand', 'China': 'Chinese',
                    'Luxembourg': 'Luxembourg', 'Taiwan': 'Taiwanese',
                    'South Africa': 'South African', 'Sweden': 'Swedish',
                    'Switzerland': 'Swiss', 'Denmark': 'Danish',
                    'Argentina': 'Argentine', 'Russia': 'Russian',
                    'Aruba': 'Aruba', 'India': 'Indian',
                    'Norway':'Norwegian', 'Federal Republic of Yugoslavia': 'Yugoslav',
                    'Iran': 'Iranian', 'Bhutan': 'Bhutanese',
                    'Vietnam': 'Vietnamese', 'Dominican Republic': 'Dominican',
                    'Hungary': 'Hungarian', 'Poland': 'Polish'}
    
    return country_dict[country]


def check_in_english(utterance):
    for _, text in utterance.items():
        text = re.sub(r'[.,"\'-?:!;]', '', text)
        text = text.replace(' ','')
        if not text.encode('UTF-8').isalpha():
            return False
            
    return True
