import numpy as np

def age_map(age):
    if age == 0:
        age = 1
    elif age == 1:
        age = 2
    elif age == 2:
        age = 2
    elif age == 3:
        age = 2
    elif age == 4:
        age = 2
    elif age == 5:
        age = 0
    
    return age

def get_item_index(feature, user_id):
    item_feature = feature[user_id]
    index = np.where(item_feature == 1)[0][ : -1]
    gender = index[0]
    jacket = index[1] - 2
    color = index[2] - 18
    
    return gender, jacket, color

def get_user_age(age):
    if age == 0:
        age_str = 'under 20'
    elif age == 1:
        age_str = '20-30'
    elif age == 2:
        age_str = 'over 30'
    
    return age_str

def get_user_gender(gender):
    if gender == 0:
        gender_str = 'men'
    elif gender == 1:
        gender_str = 'women'
    return gender_str

def get_item_gender(gender):
    if gender == 0:
        gender_str = 'men'
    elif gender == 1:
        gender_str = 'women'
        
    return gender_str

def get_item_type(jacket):
    if jacket == 0:
        jacket_str = 'bomber'
    elif jacket == 1:
        jacket_str = 'cropped'
    elif jacket == 2:
        jacket_str = 'field'
    elif jacket == 3:
        jacket_str = 'fleece'
    elif jacket == 4:
        jacket_str = 'insulated'
    elif jacket == 5:
        jacket_str = 'motorcycle'
    elif jacket == 6:
        jacket_str = 'other'
    elif jacket == 7:
        jacket_str = 'packable'
    elif jacket == 8:
        jacket_str = 'parkas'
    elif jacket == 9:
        jacket_str = 'pea'
    elif jacket == 10:
        jacket_str = 'rain'
    elif jacket == 11:
        jacket_str = 'shells'
    elif jacket == 12:
        jacket_str = 'track'
    elif jacket == 13:
        jacket_str = 'trench'
    elif jacket == 14:
        jacket_str = 'vests'
    elif jacket == 15:
        jacket_str = 'waterproof'
    
    return jacket_str

def get_item_type_index(jacket_val):
    index_dict = {'bomber':0, 'cropped':1, 'field':2, 'fleece':3, 'insulated':4,
                'motorcycle':5, 'other':6, 'packable':7, 'parkas':8, 'pea':9,
                'rain':10, 'shells':11, 'track':12, 'trench':13, 'vests':14, 'waterproof':15}
    
    return index_dict[jacket_val]

def get_item_color(color):
    if color == 0:
        color_str = 'beige'
    elif color == 1:
        color_str = 'black'
    elif color == 2:
        color_str = 'blue'
    elif color == 3:
        color_str = 'brown'
    elif color == 4:
        color_str = 'gray'
    elif color == 5:
        color_str = 'green'
    elif color == 6:
        color_str = 'multi'
    elif color == 7:
        color_str = 'navy'
    elif color == 8:
        color_str = 'olive'
    elif color == 9:
        color_str = 'other'
    elif color == 10:
        color_str = 'pink'
    elif color == 11:
        color_str = 'purple'
    elif color == 12:
        color_str = 'red'
    
    return color_str

def get_item_color_index(color_val):
    index_dict = {'beige':0, 'black':1, 'blue':2, 'brown':3, 'gray':4,
                'green':5, 'multi':6, 'navy':7, 'olive':8, 'other':9,
                'pink':10, 'purple':11, 'red':12,}
    
    return index_dict[color_val]