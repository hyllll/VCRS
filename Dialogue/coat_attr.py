import random
from coat_utils import *

gender_tag = {'0': ['00', '01', '02'],
              '1': ['10', '11']}

jacket_tag = {'0': ['00', '01', '02'],
              '1': ['10', '11'],
              '2': ['20'],
              '3': ['30']}

color_tag = {'0': ['00', '01', '02'],
              '1': ['10', '11'],
              '2': ['20'],
              '3': ['30']}

def index_attr_pattern(utterance_pattern, tags, pattern_mode=None):
    '''
    return:
       [
        {
            "tag":['00'],
            "nl": "Do you want coats for men or women?"
        },
        {
            "tag":['00'],
            "nl": "Do you want men's coats or women's coats?"
        },
       ]
    '''
    utterances = []
    if pattern_mode != None:
        tag = tags[str(pattern_mode)]
        for utterance in utterance_pattern:
            if set(utterance["tag"]) & set(tag):
                utterances.append(utterance)
    else:
        for utterance in utterance_pattern:
            if set(utterance["tag"]) & set(tags):
                utterances.append(utterance)

    return utterances


def generate_gender_dialogue(agent_pattern, user_pattern, gender_val, gender_all, gender_weight):
    gender_dialogue = {}
    pattern_mode = random.choices([0, 1], weights=[12, 88], k=1)[0]
    agent_pattern = index_attr_pattern(agent_pattern["gender"], gender_tag, pattern_mode)
    utterance = random.choice(agent_pattern)
    utterance_content = utterance['nl']
    utterance_tag = utterance['tag']
    if pattern_mode == 0:
        gender_dialogue['Q'] = utterance_content
        utterance = random.choice(index_attr_pattern(user_pattern["gender"], utterance_tag))
        utterance_content = utterance['nl']
        utterance_content = utterance_content.replace('$gender$', gender_val, 1)
        gender_dialogue['A'] = utterance_content[0].upper() + utterance_content[1:]
    elif pattern_mode == 1:
        gender_tmp = random.choices(sorted(gender_all), weights=gender_weight, k=1)
        gender_tmp = get_item_gender(gender_tmp[0])
        gender_dialogue['Q'] = utterance_content.replace('$gender$', gender_tmp, 1)
        if gender_tmp == gender_val:
            utterance = random.choice(index_attr_pattern(user_pattern["gender_pos"], utterance_tag))
        else:
            utterance = random.choice(index_attr_pattern(user_pattern["gender_neg"], utterance_tag))
        gender_dialogue['A'] = utterance['nl'].replace('$gender$', gender_tmp, 1)
        
    return gender_dialogue


def gen_pattern_mode_one(attr, u_content, u_tag, g_tag, other, info):
        '''
            u_content: Do you like $jacket$ coats?
            g_tag: 0 or 1, whether slot ground truth
        '''
        val = info[0]
        all = info[1]
        weight = info[2]
        user_pattern = info[3]
        dialogue = {}
        tmp_other = other
        slot = '$' + attr + '$'
        if attr == 'jacket':
            pos = "jacket_pos"
            neg = "jacket_neg"
            add_val = get_item_type_index(val)
            get_item_func = get_item_type
        elif attr == 'color':
            pos = "color_pos"
            neg = "color_neg"
            add_val = get_item_color_index(val)
            get_item_func = get_item_color
        if g_tag:
            dialogue['Q'] = u_content.replace(slot, val, 1)
            utterance = random.choice(index_attr_pattern(user_pattern[pos], u_tag))
            dialogue['A'] = utterance['nl']
            tmp = []
        else:
            tmp_other.append(add_val)

            while True:
                tmp = random.choices(sorted(all), weights=weight, k=1)
                if not set(tmp_other) & set(tmp):
                    break
            dialogue['Q'] = u_content.replace(slot, get_item_func(tmp[0]), 1)
            utterance = random.choice(index_attr_pattern(user_pattern[neg], u_tag))
            dialogue['A'] = utterance['nl'][0].upper() + utterance['nl'][1:]
        
        return dialogue['Q'], dialogue['A'], tmp


def gen_pattern_mode_two(attr, u_content, u_tag, g_tag, other, info):
        '''
            u_content: Do you prefer $jacket$ or $jacket$ coats?
            g_tag: 0 or 1, whether slot ground truth
        '''
        val = info[0]
        all = info[1]
        weight = info[2]
        user_pattern = info[3]
        dialogue = {}
        tmp_other = other
        slot = '$' + attr + '$'
        if attr == 'jacket':
            pos = "jacket"
            neg = "jacket_neg"
            add_val = get_item_type_index(val)
            get_item_func = get_item_type
        elif attr == 'color':
            pos = "color"
            neg = "color_neg"
            add_val = get_item_color_index(val)
            get_item_func = get_item_color
        if g_tag:
            tmp_other.append(add_val)
            while True:
                tmp = random.choices(sorted(all), weights=weight, k=1)
                if not set(tmp_other) & set(tmp):
                    break
            order = random.randint(0, 1)
            if order:
                u_content = u_content.replace(slot, get_item_func(tmp[0]), 1)
                u_content = u_content.replace(slot, val, 1)
            else:
                u_content = u_content.replace(slot, val, 1)
                u_content = u_content.replace(slot, get_item_func(tmp[0]), 1)
            dialogue['Q'] = u_content
            utterance = random.choice(index_attr_pattern(user_pattern[pos], u_tag))
            utterance_content = utterance['nl']
            utterance_content = utterance_content.replace(slot, val, 1)
            dialogue['A'] = utterance_content[0].upper() + utterance_content[1:]
        else:
            tmp_other.append(add_val)
            while True:
                tmp = random.choices(sorted(all), weights=weight, k=2)
                if not set(tmp_other) & set(tmp):
                    break
            random.shuffle(tmp)
            for v in tmp:
                u_content = u_content.replace(slot, get_item_func(v), 1)
            dialogue['Q'] = u_content
            utterance = random.choice(index_attr_pattern(user_pattern[neg], u_tag))
            dialogue['A'] = utterance['nl'][0].upper() + utterance['nl'][1:]
        
        return dialogue['Q'], dialogue['A'], tmp


def select_gen_pattern(mode):
    if mode == 1:
        func = gen_pattern_mode_one
    else:
        func = gen_pattern_mode_two
    
    return func


def get_agent_content_tag(attr, pattern, mode, tag):
    pattern = index_attr_pattern(pattern[attr], tag, mode)
    utterance = random.choice(pattern)
    utterance_content = utterance['nl']
    utterance_tag = utterance['tag']

    return utterance_content, utterance_tag


def generate_jacket_dialogue(agent_pattern, user_pattern, jacket_val, jacket_all, jacket_weight):
    jacket_dialogue = {}
    jacket_info = (jacket_val, jacket_all, jacket_weight, user_pattern)
    jacket_other = [6]
    if jacket_val == 'other':
        pattern_mode = 3
    else:
        pattern_mode = random.choices([0, 1, 2], weights=[10, 45, 45], k=1)[0]
    utterance_content, utterance_tag = get_agent_content_tag("jacket", agent_pattern, pattern_mode, jacket_tag)
    if pattern_mode == 0:
        jacket_dialogue['Q'] = utterance_content
        utterance = random.choice(index_attr_pattern(user_pattern["jacket"], utterance_tag))
        utterance_content = utterance['nl']
        utterance_content = utterance_content.replace('$jacket$', jacket_val, 1)
        jacket_dialogue['A'] = utterance_content[0].upper() + utterance_content[1:]
    elif pattern_mode == 1 or pattern_mode == 2:
        rounds = random.randint(1,3)
        gen_func = select_gen_pattern(pattern_mode)
        if rounds == 1:
            jacket_dialogue['Q'], jacket_dialogue['A'], _ = gen_func('jacket', utterance_content, utterance_tag, 1, jacket_other, jacket_info)
        elif rounds >= 2:
            jacket_dialogue['Q'], jacket_dialogue['A'], added_attr = gen_func('jacket', utterance_content, utterance_tag, 0, jacket_other, jacket_info)
            last_pm = pattern_mode
            pattern_mode = random.randint(1,2)
            gen_func = select_gen_pattern(pattern_mode)
            jacket_other = jacket_other + added_attr
            if rounds == 2:
                g_tag = 1
            else:
                g_tag = 0
            utterance_content, utterance_tag = get_agent_content_tag("jacket", agent_pattern, pattern_mode, jacket_tag)
            if last_pm == pattern_mode:
                jacket_dialogue['Q1'], jacket_dialogue['A1'], added_attr = gen_func('jacket', utterance_content, utterance_tag, g_tag, jacket_other, jacket_info)
            else:
                jacket_dialogue['Q1'], jacket_dialogue['A1'], added_attr = gen_func('jacket', utterance_content, utterance_tag, g_tag, jacket_other, jacket_info)
            if rounds == 3:
                g_tag = 1
                last_pm = pattern_mode
                pattern_mode = random.randint(1,2)
                gen_func = select_gen_pattern(pattern_mode)
                jacket_other = jacket_other + added_attr
                utterance_content, utterance_tag = get_agent_content_tag("jacket", agent_pattern, pattern_mode, jacket_tag)
                if last_pm == pattern_mode:
                    jacket_dialogue['Q2'], jacket_dialogue['A2'], _ = gen_func('jacket', utterance_content, utterance_tag, g_tag, jacket_other, jacket_info)
                else:
                    jacket_dialogue['Q2'], jacket_dialogue['A2'], _ = gen_func('jacket', utterance_content, utterance_tag, g_tag, jacket_other, jacket_info)
    elif pattern_mode == 3:
        rounds = random.randint(1,2)
        while True:
            added_attr = random.choices(sorted(jacket_all), weights=jacket_weight, k=3)
            if not set(jacket_other) & set(added_attr):
                break
        random.shuffle(added_attr)
        for v in added_attr:
            utterance_content = utterance_content.replace('$jacket$', get_item_type(v), 1)
        jacket_dialogue['Q'] = utterance_content
        utterance = random.choice(index_attr_pattern(user_pattern['jacket_neg'], utterance_tag))
        jacket_dialogue['A'] = utterance['nl'][0].upper() + utterance['nl'][1:]
        if rounds == 2:
            pattern_mode = random.randint(1,3)
            utterance_content, utterance_tag = get_agent_content_tag("jacket", agent_pattern, pattern_mode, jacket_tag)
            jacket_other = jacket_other + added_attr
            if pattern_mode != 3:
                gen_func = select_gen_pattern(pattern_mode)
                jacket_dialogue['Q1'], jacket_dialogue['A1'], _ = gen_func('jacket', utterance_content, utterance_tag, 0, jacket_other, jacket_info)
            else:
                while True:
                    added_attr = random.choices(sorted(jacket_all), weights=jacket_weight, k=3)
                    if not set(jacket_other) & set(added_attr):
                        break
                random.shuffle(added_attr)
                for v in added_attr:
                    utterance_content = utterance_content.replace('$jacket$', get_item_type(v), 1)
                jacket_dialogue['Q1'] = utterance_content
                utterance = random.choice(index_attr_pattern(user_pattern['jacket_neg'], utterance_tag))
                jacket_dialogue['A1'] = utterance['nl'][0].upper() + utterance['nl'][1:]
    
    return jacket_dialogue


def generate_color_dialogue(agent_pattern, user_pattern, color_val, color_all, color_weight):
    color_dialogue = {}
    color_info = (color_val, color_all, color_weight, user_pattern)
    color_other = [9]
    if color_val == 'other':
        pattern_mode = 3
    else:
        pattern_mode = random.choices([0, 1, 2], weights=[20, 40, 40], k=1)[0]
    utterance_content, utterance_tag = get_agent_content_tag("color", agent_pattern, pattern_mode, color_tag)
    if pattern_mode == 0:
        color_dialogue['Q'] = utterance_content
        utterance = random.choice(index_attr_pattern(user_pattern["color"], utterance_tag))
        utterance_content = utterance['nl']
        utterance_content = utterance_content.replace('$color$', color_val, 1)
        color_dialogue['A'] = utterance_content[0].upper() + utterance_content[1:]
    elif pattern_mode == 1 or pattern_mode == 2:
        rounds = random.randint(1,3)
        gen_func = select_gen_pattern(pattern_mode)
        if rounds == 1:
            color_dialogue['Q'], color_dialogue['A'], _ = gen_func('color', utterance_content, utterance_tag, 1, color_other, color_info)
        elif rounds >= 2:
            color_dialogue['Q'], color_dialogue['A'], added_attr = gen_func('color', utterance_content, utterance_tag, 0, color_other, color_info)
            last_pm = pattern_mode
            pattern_mode = random.randint(1,2)
            gen_func = select_gen_pattern(pattern_mode)
            color_other = color_other + added_attr
            if rounds == 2:
                g_tag = 1
            else:
                g_tag = 0
            utterance_content, utterance_tag = get_agent_content_tag("color", agent_pattern, pattern_mode, color_tag)
            if last_pm == pattern_mode:
                color_dialogue['Q1'], color_dialogue['A1'], added_attr = gen_func('color', utterance_content, utterance_tag, g_tag, color_other, color_info)
            else:
                color_dialogue['Q1'], color_dialogue['A1'], added_attr = gen_func('color', utterance_content, utterance_tag, g_tag, color_other, color_info)
            if rounds == 3:
                g_tag = 1
                last_pm = pattern_mode
                pattern_mode = random.randint(1,2)
                gen_func = select_gen_pattern(pattern_mode)
                color_other = color_other + added_attr
                utterance_content, utterance_tag = get_agent_content_tag("color", agent_pattern, pattern_mode, color_tag)
                if last_pm == pattern_mode:
                    color_dialogue['Q2'], color_dialogue['A2'], _ = gen_func('color', utterance_content, utterance_tag, g_tag, color_other, color_info)
                else:
                    color_dialogue['Q2'], color_dialogue['A2'], _ = gen_func('color', utterance_content, utterance_tag, g_tag, color_other, color_info)
    elif pattern_mode == 3:
        rounds = random.randint(1,2)
        while True:
            added_attr = random.choices(sorted(color_all), weights=color_weight, k=3)
            if not set(color_other) & set(added_attr):
                break
        random.shuffle(added_attr)
        for v in added_attr:
            utterance_content = utterance_content.replace('$color$', get_item_color(v), 1)
        color_dialogue['Q'] = utterance_content
        utterance = random.choice(index_attr_pattern(user_pattern['color_neg'], utterance_tag))
        color_dialogue['A'] = utterance['nl'][0].upper() + utterance['nl'][1:]
        if rounds == 2:
            pattern_mode = random.randint(1,3)
            utterance_content, utterance_tag = get_agent_content_tag("color", agent_pattern, pattern_mode, color_tag)
            color_other = color_other + added_attr
            if pattern_mode != 3:
                gen_func = select_gen_pattern(pattern_mode)
                color_dialogue['Q1'], color_dialogue['A1'], _ = gen_func('color', utterance_content, utterance_tag, 0, color_other, color_info)
            else:
                while True:
                    added_attr = random.choices(sorted(color_all), weights=color_weight, k=3)
                    if not set(color_other) & set(added_attr):
                        break
                random.shuffle(added_attr)
                for v in added_attr:
                    utterance_content = utterance_content.replace('$color$', get_item_color(v), 1)
                color_dialogue['Q1'] = utterance_content
                utterance = random.choice(index_attr_pattern(user_pattern['color_neg'], utterance_tag))
                color_dialogue['A1'] = utterance['nl'][0].upper() + utterance['nl'][1:]
    
    return color_dialogue


            


            
        
    





            






   
    
    
    



            

        


















