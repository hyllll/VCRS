import random
from movie_utils import *

country_tag = {'0': ['00']}

genre_tag = {'0': ['00', '01'],
              '1': ['10', '11'],
              '2': ['20'],
              '3': ['30']}

director_tag = {'0': ['00', '01'],
              '1': ['10', '11', '12'],
              '2': ['20'],
              '3': ['30']}

actor_tag = {'0': ['00', '01'],
              '1': ['10', '11', '12'],
              '2': ['20'],
              '3': ['30']}

def check_repeat(tmp):
    tmp_set = set(tmp)
    if len(tmp) == len(tmp_set):
        return True
    else:
        return False

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

def gen_pattern_mode_one(attr, u_content, u_tag, g_tag, other, info):
        '''
            u_content: Do you like $genre$ movies?
            g_tag: 0 or 1, whether slot ground truth
        '''
        val = info[0]
        all = info[1]
        weight = info[2]
        user_pattern = info[3]
        dialogue = {}
        tmp_other = other
        slot = '$' + attr + '$'
        if attr == 'genre':
            pos = "genre_pos"
            neg = "genre_neg"
            add_val = val
        elif attr == 'director':
            pos = "director_pos"
            neg = "director_neg"
            add_val = val
        elif attr == 'actor':
            pos = "actor_pos"
            neg = "actor_neg"
            add_val = val
        if g_tag:
            if attr == 'genre' or attr == 'actor':
                val = random.choice(val)
            slot_val = val
            if attr == 'genre':
                slot_val = slot_val.lower()
            dialogue['Q'] = u_content.replace(slot, slot_val, 1)
            utterance = random.choice(index_attr_pattern(user_pattern[pos], u_tag))
            answer = utterance['nl']
            if '$genre$' in answer:
                answer = answer.replace('$genre$', slot_val, 1)
            dialogue['A'] = answer
            tmp = []
        else:
            if attr == 'genre' or attr == 'actor':
                tmp_other = tmp_other + add_val
            else:
                tmp_other.append(add_val)

            while True:
                tmp = random.choices(sorted(all), weights=weight, k=1)
                if not set(tmp_other) & set(tmp):
                    break
            slot_val = tmp[0]
            if attr == 'genre':
                slot_val = slot_val.lower()
            dialogue['Q'] = u_content.replace(slot, slot_val, 1)
            utterance = random.choice(index_attr_pattern(user_pattern[neg], u_tag))
            answer = utterance['nl']
            if '$genre$' in answer:
                answer = answer.replace('$genre$', slot_val, 1)
            dialogue['A'] = answer[0].upper() + answer[1:]
        
        return dialogue['Q'], dialogue['A'], tmp

def gen_pattern_mode_two(attr, u_content, u_tag, g_tag, other, info):
        '''
            u_content: Do you prefer $genre$ or $genre$ movies?
            g_tag: 0 or 1, whether slot ground truth
        '''
        val = info[0]
        all = info[1]
        weight = info[2]
        user_pattern = info[3]
        dialogue = {}
        tmp_other = other
        slot = '$' + attr + '$'
        if attr == 'genre':
            pos = "genre"
            neg = "genre_neg"
            add_val = val
        elif attr == 'director':
            pos = "director"
            neg = "director_neg"
            add_val = val
        elif attr == 'actor':
            pos = "actor"
            neg = "actor_neg"
            add_val = val
        if g_tag:
            if attr == 'genre' or attr == 'actor':
                tmp_other = tmp_other + add_val
            else:
                tmp_other.append(add_val)
            while True:
                tmp = random.choices(sorted(all), weights=weight, k=1)
                if not set(tmp_other) & set(tmp):
                    break
            order = random.randint(0, 1)
            if attr == 'genre' or attr == 'actor':
                val = random.choice(val)
            slot_val = val
            slot_tmp_val = tmp[0]
            if attr == 'genre':
                slot_val = slot_val.lower()
                slot_tmp_val = slot_tmp_val.lower()
            if order:
                u_content = u_content.replace(slot, slot_tmp_val, 1)
                u_content = u_content.replace(slot, slot_val, 1)
            else:
                u_content = u_content.replace(slot, slot_val, 1)
                u_content = u_content.replace(slot, slot_tmp_val, 1)
            dialogue['Q'] = u_content
            utterance = random.choice(index_attr_pattern(user_pattern[pos], u_tag))
            utterance_content = utterance['nl']
            utterance_content = utterance_content.replace(slot, val, 1)
            dialogue['A'] = utterance_content[0].upper() + utterance_content[1:]
        else:
            if attr == 'genre' or attr == 'actor':
                tmp_other = tmp_other + add_val
            else:
                tmp_other.append(add_val)
            while True:
                tmp = random.choices(sorted(all), weights=weight, k=2)
                if (not set(tmp_other) & set(tmp)) and (check_repeat(tmp)):
                    break
            random.shuffle(tmp)
            for v in tmp:
                if attr == 'genre':
                    v = v.lower()
                u_content = u_content.replace(slot, v, 1)
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

def generate_country_dialogue(agent_pattern, user_pattern, country_val):
    country_dialogue = {}
    pattern_mode = 0
    agent_pattern = index_attr_pattern(agent_pattern["country"], country_tag, pattern_mode)
    utterance = random.choice(agent_pattern)
    utterance_content = utterance['nl']
    utterance_tag = utterance['tag']
    country_dialogue['Q'] = utterance_content
    utterance = random.choice(index_attr_pattern(user_pattern["country"], utterance_tag))
    utterance_content = utterance['nl']
    utterance_content = utterance_content.replace('$country$', country_val, 1)
    country_dialogue['A'] = utterance_content[0].upper() + utterance_content[1:]

    return country_dialogue

def generate_genre_dialogue(agent_pattern, user_pattern, genre_val, genre_all, genre_weight):
    '''
        genre_val (List): ['thriller', 'commedy', 'action']
    '''
    genre_dialogue = {}
    genre_info = (genre_val, genre_all, genre_weight, user_pattern)
    genre_other = []
    pattern_mode = random.choices([0, 1, 2, 3], weights=[5, 45, 45, 5], k=1)[0]
    utterance_content, utterance_tag = get_agent_content_tag("genre", agent_pattern, pattern_mode, genre_tag)
    if pattern_mode == 0:
        genre_dialogue['Q'] = utterance_content
        utterance = random.choice(index_attr_pattern(user_pattern["genre"], utterance_tag))
        utterance_content = utterance['nl']
        genre_val = random.choice(genre_val).lower()
        utterance_content = utterance_content.replace('$genre$', genre_val, 1)
        genre_dialogue['A'] = utterance_content[0].upper() + utterance_content[1:]
    elif pattern_mode == 1 or pattern_mode == 2:
        rounds = random.randint(1,3)
        gen_func = select_gen_pattern(pattern_mode)
        if rounds == 1:
            genre_dialogue['Q'], genre_dialogue['A'], _ = gen_func('genre', utterance_content, utterance_tag, 1, genre_other, genre_info)
        elif rounds >= 2:
            genre_dialogue['Q'], genre_dialogue['A'], added_attr = gen_func('genre', utterance_content, utterance_tag, 0, genre_other, genre_info)
            pattern_mode = random.randint(1,2)
            gen_func = select_gen_pattern(pattern_mode)
            genre_other = genre_other + added_attr
            if rounds == 2:
                g_tag = 1
            else:
                g_tag = 0
            utterance_content, utterance_tag = get_agent_content_tag("genre", agent_pattern, pattern_mode, genre_tag)
            genre_dialogue['Q1'], genre_dialogue['A1'], added_attr = gen_func('genre', utterance_content, utterance_tag, g_tag, genre_other, genre_info)
            if rounds == 3:
                g_tag = 1
                pattern_mode = random.randint(1,2)
                gen_func = select_gen_pattern(pattern_mode)
                genre_other = genre_other + added_attr
                utterance_content, utterance_tag = get_agent_content_tag("genre", agent_pattern, pattern_mode, genre_tag)
                genre_dialogue['Q2'], genre_dialogue['A2'], _ = gen_func('genre', utterance_content, utterance_tag, g_tag, genre_other, genre_info)
        elif pattern_mode == 3:
            rounds = random.randint(1,2)
            while True:
                added_attr = random.choices(sorted(genre_all), weights=genre_weight, k=3)
                if (not set(genre_other) & set(added_attr)) and (check_repeat(added_attr)):
                    break
            random.shuffle(added_attr)
            for v in added_attr:
                utterance_content = utterance_content.replace('$genre$', v, 1)
            genre_dialogue['Q'] = utterance_content
            utterance = random.choice(index_attr_pattern(user_pattern['genre_neg'], utterance_tag))
            genre_dialogue['A'] = utterance['nl'][0].upper() + utterance['nl'][1:]
            if rounds == 2:
                pattern_mode = random.randint(1,3)
                utterance_content, utterance_tag = get_agent_content_tag("genre", agent_pattern, pattern_mode, genre_tag)
                genre_other = genre_other + added_attr
                if pattern_mode != 3:
                    gen_func = select_gen_pattern(pattern_mode)
                    genre_dialogue['Q1'], genre_dialogue['A1'], _ = gen_func('genre', utterance_content, utterance_tag, 0, genre_other, genre_info)
            else:
                while True:
                    added_attr = random.choices(sorted(genre_all), weights=genre_weight, k=3)
                    if (not set(genre_other) & set(added_attr)) and (check_repeat(added_attr)):
                        break
                random.shuffle(added_attr)
                for v in added_attr:
                    utterance_content = utterance_content.replace('$genre$', v, 1)
                genre_dialogue['Q1'] = utterance_content
                utterance = random.choice(index_attr_pattern(user_pattern['genre_neg'], utterance_tag))
                genre_dialogue['A1'] = utterance['nl'][0].upper() + utterance['nl'][1:]
    
    return genre_dialogue

def generate_director_dialogue(agent_pattern, user_pattern, director_val, director_all, director_weight, o_director):
    director_dialogue = {}
    director_info = (director_val, director_all, director_weight, user_pattern)
    director_other = o_director
    if director_val in director_other:
        pattern_mode = 3
    else:
        pattern_mode = random.choices([0, 1, 2], weights=[10, 45, 45], k=1)[0]
    utterance_content, utterance_tag = get_agent_content_tag("director", agent_pattern, pattern_mode, director_tag)
    if pattern_mode == 0:
        director_dialogue['Q'] = utterance_content
        utterance = random.choice(index_attr_pattern(user_pattern["director"], utterance_tag))
        utterance_content = utterance['nl']
        utterance_content = utterance_content.replace('$director$', director_val, 1)
        director_dialogue['A'] = utterance_content[0].upper() + utterance_content[1:]
    elif pattern_mode == 1 or pattern_mode == 2:
        rounds = random.randint(1,3)
        gen_func = select_gen_pattern(pattern_mode)
        if rounds == 1:
            director_dialogue['Q'], director_dialogue['A'], _ = gen_func('director', utterance_content, utterance_tag, 1, director_other, director_info)
        elif rounds >= 2:
            director_dialogue['Q'], director_dialogue['A'], added_attr = gen_func('director', utterance_content, utterance_tag, 0, director_other, director_info)
            pattern_mode = random.randint(1,2)
            gen_func = select_gen_pattern(pattern_mode)
            director_other = director_other + added_attr
            if rounds == 2:
                g_tag = 1
            else:
                g_tag = 0
            utterance_content, utterance_tag = get_agent_content_tag("director", agent_pattern, pattern_mode, director_tag)
            director_dialogue['Q1'], director_dialogue['A1'], added_attr = gen_func('director', utterance_content, utterance_tag, g_tag, director_other, director_info)
            if rounds == 3:
                g_tag = 1
                pattern_mode = random.randint(1,2)
                gen_func = select_gen_pattern(pattern_mode)
                director_other = director_other + added_attr
                utterance_content, utterance_tag = get_agent_content_tag("director", agent_pattern, pattern_mode, director_tag)
                director_dialogue['Q2'], director_dialogue['A2'], _ = gen_func('director', utterance_content, utterance_tag, g_tag, director_other, director_info)
    elif pattern_mode == 3:
        rounds = random.randint(1,2)
        while True:
            added_attr = random.choices(sorted(director_all), weights=director_weight, k=3)
            if (not set(director_other) & set(added_attr)) and (check_repeat(added_attr)):
                break
        random.shuffle(added_attr)
        for v in added_attr:
            utterance_content = utterance_content.replace('$director$', v, 1)
        director_dialogue['Q'] = utterance_content
        utterance = random.choice(index_attr_pattern(user_pattern['director_neg'], utterance_tag))
        director_dialogue['A'] = utterance['nl'][0].upper() + utterance['nl'][1:]
        if rounds == 2:
            pattern_mode = random.randint(1,3)
            utterance_content, utterance_tag = get_agent_content_tag("director", agent_pattern, pattern_mode, director_tag)
            director_other = director_other + added_attr
            if pattern_mode != 3:
                gen_func = select_gen_pattern(pattern_mode)
                director_dialogue['Q1'], director_dialogue['A1'], _ = gen_func('director', utterance_content, utterance_tag, 0, director_other, director_info)
            else:
                while True:
                    added_attr = random.choices(sorted(director_all), weights=director_weight, k=3)
                    if (not set(director_other) & set(added_attr)) and (check_repeat(added_attr)):
                        break
                random.shuffle(added_attr)
                for v in added_attr:
                    utterance_content = utterance_content.replace('$director$', v, 1)
                director_dialogue['Q1'] = utterance_content
                utterance = random.choice(index_attr_pattern(user_pattern['director_neg'], utterance_tag))
                director_dialogue['A1'] = utterance['nl'][0].upper() + utterance['nl'][1:]
    
    return director_dialogue

def generate_actor_dialogue(agent_pattern, user_pattern, actor_val, actor_all, actor_weight, o_actor):
    actor_dialogue = {}
    actor_info = (actor_val, actor_all, actor_weight, user_pattern)
    actor_other = o_actor
    if set(actor_val) & set(o_actor):
        pattern_mode = 3
    else:
        pattern_mode = random.choices([0, 1, 2], weights=[10, 45, 45], k=1)[0]
    utterance_content, utterance_tag = get_agent_content_tag("actor", agent_pattern, pattern_mode, actor_tag)
    if pattern_mode == 0:
        actor_dialogue['Q'] = utterance_content
        utterance = random.choice(index_attr_pattern(user_pattern["actor"], utterance_tag))
        utterance_content = utterance['nl']
        actor_val = random.choice(actor_val).lower()
        utterance_content = utterance_content.replace('$actor$', actor_val, 1)
        actor_dialogue['A'] = utterance_content[0].upper() + utterance_content[1:]
    elif pattern_mode == 1 or pattern_mode == 2:
        rounds = random.randint(1,3)
        gen_func = select_gen_pattern(pattern_mode)
        if rounds == 1:
            actor_dialogue['Q'], actor_dialogue['A'], _ = gen_func('actor', utterance_content, utterance_tag, 1, actor_other, actor_info)
        elif rounds >= 2:
            actor_dialogue['Q'], actor_dialogue['A'], added_attr = gen_func('actor', utterance_content, utterance_tag, 0, actor_other, actor_info)
            pattern_mode = random.randint(1,2)
            gen_func = select_gen_pattern(pattern_mode)
            actor_other = actor_other + added_attr
            if rounds == 2:
                g_tag = 1
            else:
                g_tag = 0
            utterance_content, utterance_tag = get_agent_content_tag("actor", agent_pattern, pattern_mode, actor_tag)
            actor_dialogue['Q1'], actor_dialogue['A1'], added_attr = gen_func('actor', utterance_content, utterance_tag, g_tag, actor_other, actor_info)
            if rounds == 3:
                g_tag = 1
                pattern_mode = random.randint(1,2)
                gen_func = select_gen_pattern(pattern_mode)
                actor_other = actor_other + added_attr
                utterance_content, utterance_tag = get_agent_content_tag("actor", agent_pattern, pattern_mode, actor_tag)
                actor_dialogue['Q2'], actor_dialogue['A2'], _ = gen_func('actor', utterance_content, utterance_tag, g_tag, actor_other, actor_info)
    elif pattern_mode == 3:
        rounds = random.randint(1,2)
        while True:
            added_attr = random.choices(sorted(actor_all), weights=actor_weight, k=3)
            if (not set(actor_other) & set(added_attr)) and (check_repeat(added_attr)):
                break
        random.shuffle(added_attr)
        for v in added_attr:
            utterance_content = utterance_content.replace('$actor$', v, 1)
        actor_dialogue['Q'] = utterance_content
        utterance = random.choice(index_attr_pattern(user_pattern['actor_neg'], utterance_tag))
        actor_dialogue['A'] = utterance['nl'][0].upper() + utterance['nl'][1:]
        if rounds == 2:
            pattern_mode = random.randint(1,3)
            utterance_content, utterance_tag = get_agent_content_tag("actor", agent_pattern, pattern_mode, actor_tag)
            actor_other = actor_other + added_attr
            if pattern_mode != 3:
                gen_func = select_gen_pattern(pattern_mode)
                actor_dialogue['Q1'], actor_dialogue['A1'], _ = gen_func('actor', utterance_content, utterance_tag, 0, actor_other, actor_info)
            else:
                while True:
                    added_attr = random.choices(sorted(actor_all), weights=actor_weight, k=3)
                    if (not set(actor_other) & set(added_attr)) and (check_repeat(added_attr)):
                        break
                random.shuffle(added_attr)
                for v in added_attr:
                    utterance_content = utterance_content.replace('$actor$', v, 1)
                actor_dialogue['Q1'] = utterance_content
                utterance = random.choice(index_attr_pattern(user_pattern['actor_neg'], utterance_tag))
                actor_dialogue['A1'] = utterance['nl'][0].upper() + utterance['nl'][1:]
    
    return actor_dialogue