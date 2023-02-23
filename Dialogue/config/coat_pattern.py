agent_pattern = {
    "gender":[
        {
            "tag":['00'],
            "nl": "Do you want coats for men or women?"
        },
        {
            "tag":['00'],
            "nl": "Do you want men's coats or women's coats?"
        },
        {
            "tag":['01'],
            "nl": "Do you prefer wearing men's or women's coats?"
        },
        {
            "tag":['01'],
            "nl": "Which do you prefer, men's or women's coats?"
        },
        {
            "tag":['02'],
            "nl": "Do you like men's or women's coats?"
        },
        {
            "tag":['10'],
            "slots":["gender"],
            "nl": "Are you looking for $gender$'s coats?"
        },
        {
            "tag":['10'],
            "slots":["gender"],
            "nl": "Are you finding $gender$'s coats?"
        },
        {
            "tag":['10'],
            "slots":["gender"],
            "nl": "Are you trying to find $gender$'s coats?"
        },
        {
            "tag":['11'],
            "slots":["gender"],
            "nl": "Do you need coats for $gender$?"
        },
        {
            "tag":['11'],
            "slots":["gender"],
            "nl": "Do you want to buy $gender$'s coats?"
        },
    ],
    "jacket":[
        {
            "tag":['00'],
            "nl": "What kind of coats do you like?"
        },
        {
            "tag":['00'],
            "nl": "What kind of coats do you have in mind?"
        },
        {
            "tag":['00'],
            "nl": "What kind of coats are interested in?"
        },
        {
            "tag":['00'],
            "nl": "What kind of coats interest you?"
        },
        {
            "tag":['00'],
            "nl": "What style of coats do you like?"
        },
        {
            "tag":['01'],
            "nl": "What kind of coats do you want?"
        },
        {
            "tag":['01'],
            "nl": "What style of coats do you want?"
        },
        {
            "tag":['01'],
            "nl": "What kind of coats do you need?"
        },
        {
            "tag":['01'],
            "nl": "What style of coats do you need?"
        },
        {
            "tag":['00'],
            "nl": "Which types of coats do you prefer?"
        },
        {
            "tag":['00'],
            "nl": "What styles of coats do you favor?"
        },
        {
            "tag":['00'],
            "nl": "Which fashions appeal to you?"
        },
        {
            "tag":['10'],
            "slots":["jacket"],
            "nl": "Do you like $jacket$ coats?"
        },
        {
            "tag":['10'],
            "slots":["jacket"],
            "nl": "Have you worn any $jacket$ coats?"
        },
        {
            "tag":['10'],
            "slots":["jacket"],
            "nl": "Do you favor $jacket$ coats?"
        },
        {
            "tag":['11'],
            "slots":["jacket"],
            "nl": "How about $jacket$ coats?"
        },
        {
            "tag":['11'],
            "slots":["jacket"],
            "nl": "What do you think of $jacket$ coats?"
        },
        {
            "tag":['20'],
            "slots":["jacket"],
            "nl": "Do you prefer $jacket$ or $jacket$ coats?"
        },
        {
            "tag":['20'],
            "slots":["jacket"],
            "nl": "What type of coats do you like? $jacket$ or $jacket$ coats."
        },
        {
            "tag":['20'],
            "slots":["jacket"],
            "nl": "What is better, $jacket$ or $jacket$?"
        },
        {
            "tag":['20'],
            "slots":["jacket"],
            "nl": "Do you like $jacket$ or $jacket$ coats?"
        },
        {
            "tag":['20'],
            "slots":["jacket"],
            "nl": "Do you like $jacket$ or $jacket$?"
        },
        {
            "tag":['30'],
            "slots":["jacket"],
            "nl": "Is the type of coats you want included in it? such as $jacket$, $jacket$ and $jacket$."
        },
        {
            "tag":['30'],
            "slots":["jacket"],
            "nl": "Are the coats styles you prefer included? such as $jacket$, $jacket$ and $jacket$."
        },
        {
            "tag":['30'],
            "slots":["jacket"],
            "nl": "Are the types of coats you like included? such as $jacket$, $jacket$ and $jacket$."
        },
    ],
    "color":[
        {
            "tag":['00'],
            "nl": "What color coats do you like?"
        },
        {
            "tag":['00'],
            "nl": "What color do you have in mind?"
        },
        {
            "tag":['00'],
            "nl": "What color are interested in?"
        },
        {
            "tag":['00'],
            "nl": "What color interest you?"
        },
        {
            "tag":['00'],
            "nl": "What color coats do you prefer?"
        },
        {
            "tag":['00'],
            "nl": "What colors do you prefer for coats?"
        },
        {
            "tag":['01'],
            "nl": "What color coats do you need?"
        },
        {
            "tag":['01'],
            "nl": "What color coats do you want?"
        },
        {
            "tag":['01'],
            "nl": "What colors do you want for your coats?"
        },
        {
            "tag":['02'],
            "nl": "Which colors suit you best in coats?"
        },
        {
            "tag":['10'],
            "slots":["color"],
            "nl": "Do you like $color$ coats?"
        },
        {
            "tag":['10'],
            "slots":["color"],
            "nl": "Do you favor $color$ coats?"
        },
        {
            "tag":['11'],
            "slots":["color"],
            "nl": "What do you think of $color$ coats?"
        },
        {
            "tag":['11'],
            "slots":["color"],
            "nl": "How about $color$ coats?"
        },
        {
            "tag":['20'],
            "slots":["color"],
            "nl": "Do you prefer $color$ or $color$?"
        },
        {
            "tag":['20'],
            "slots":["color"],
            "nl": "Do you prefer $color$ or $color$ coats?"
        },
        {
            "tag":['20'],
            "slots":["color"],
            "nl": "What color of coats do you like? $color$ or $color$ coats."
        },
        {
            "tag":['20'],
            "slots":["color"],
            "nl": "What is better, $color$ or $color$?"
        },
        {
            "tag":['20'],
            "slots":["color"],
            "nl": "Do you like $color$ or $color$?"
        },
        {
            "tag":['30'],
            "slots":["color"],
            "nl": "Is your favorite color included in them? such as $color$, $color$ and $color$."
        },
        {
            "tag":['30'],
            "slots":["color"],
            "nl": "Are the colors of coats you like included? such as $color$, $color$ and $color$."
        },
        {
            "tag":['30'],
            "slots":["color"],
            "nl": "Is your preferred color present? such as $color$, $color$ and $color$."
        },
    ]
}

user_pattern = {
    "gender":[
        {
            "slots":["gender"],
            "tag":['00', '01'],
            "nl":"Coats that suit $gender$."
        },
        {
            "slots":["gender"],
            "tag":['00'],
            "nl":"I want $gender$ coats."
        },
        {
            "slots":["gender"],
            "tag":['00', '01', '02'],
            "nl":"$gender$."
        },
        {
            "slots":["gender"],
            "tag":['00'],
            "nl":"I need coats for $gender$."
        },
        {
            "slots":["gender"],
            "tag":['00'],
            "nl":"I need $gender$ coats."
        },
        {
            "slots":["gender"],
            "tag":['01'],
            "nl":"I prefer to $gender$'s coats."
        },
        {
            "slots":["gender"],
            "tag":['01'],
            "nl":"$gender$'s coats appeal to me."
        },
        {
            "slots":["gender"],
            "tag":['02'],
            "nl":"I'd like to $gender$'s coats."
        },
        {
            "slots":["gender"],
            "tag":['02'],
            "nl":"I like $gender$'s coats."
        },
        {
            "slots":["gender"],
            "tag":['02'],
            "nl":"I like coats for $gender$."
        },
    ],
    "gender_pos":[
        {
            "tag":['10', '11'],
            "nl":"Yes."
        },
        {
            "tag":['10', '11'],
            "nl":"Yes, I want it."
        },
        {
            "tag":['10'],
            "nl":"Yes, it is what I'm looking for."
        },
        {
            "tag":['10'],
            "nl":"Yeah, it is what I'm looking for."
        },
        {
            "tag":['10'],
            "nl":"It's ok."
        },
        {
            "tag":['11'],
            "nl":"Yes, I need it."
        },
    ],
    "gender_neg":[
        {
            "tag":['10', '11'],
            "nl":"No."
        },
        {
            "tag":['10'],
            "nl":"It's not my cup of tea."
        },
        {
            "tag":['10'],
            "nl":"It's not really my thing."
        },
        {
            "tag":['10', '11'],
            "nl":"No, I don't want $gender$'s coats."
        },
        {
            "tag":['10', '11'],
            "nl":"No, I don't need $gender$'s coats."
        },
    ],
    "jacket":[
        {
            "tag":['00', '01', '20', '30'],
            "slots":["jacket"],
            "nl":"$jacket$."
        },
        {
            "tag":['00', '01', '20', '30'],
            "slots":["jacket"],
            "nl":"I'm in the mood to $jacket$ coats."
        },
        {
            "tag":['00', '20', '30'],
            "slots":["jacket"],
            "nl":"I like coats that are $jacket$."
        },
        {
            "tag":['00', '20', '30'],
            "slots":["jacket"],
            "nl":"I love $jacket$ coats."
        },
        {
            "tag":['00', '20', '30'],
            "slots":["jacket"],
            "nl":"I do enjoy $jacket$."
        },
        {
            "tag":['00', '20', '30'],
            "slots":["jacket"],
            "nl":"I do enjoy $jacket$."
        },
        {
            "tag":['00', '20', '30'],
            "slots":["jacket"],
            "nl":"I enjoy most $jacket$ coats."
        },
        {
            "tag":['00', '20', '30'],
            "slots":["jacket"],
            "nl":"I'm really big on $jacket$ coats."
        },
        {
            "tag":['00', '20', '30'],
            "slots":["jacket"],
            "nl":"I enjoy $jacket$ coats."
        },
        {
            "tag":['00', '20', '30'],
            "slots":["jacket"],
            "nl":"I like wearing $jacket$ coats."
        },
        {
            "tag":['01'],
            "slots":["jacket"],
            "nl":"I want the style of $jacket$."
        },
        {
            "tag":['01'],
            "slots":["jacket"],
            "nl":"I need the style of $jacket$."
        },
        {
            "tag":['01'],
            "slots":["jacket"],
            "nl":"I want $jacket$ coats."
        },
        {
            "tag":['01'],
            "slots":["jacket"],
            "nl":"I need coats similar to $jacket$."
        },
        {
            "tag":['01'],
            "slots":["jacket"],
            "nl":"I want coats similar to $jacket$."
        },
        {
            "tag":['01'],
            "slots":["jacket"],
            "nl":"I want $jacket$."
        },
        {
            "tag":['20', '30'],
            "slots":["jacket"],
            "nl":"I prefer to $jacket$ coats."
        },
        {
            "tag":['20', '30'],
            "slots":["jacket"],
            "nl":"$jacket$ coats appeal to me."
        },
    ],
    "jacket_pos":[
        {
            "tag":['10'],
            "nl":"Yes."
        },
        {
            "tag":['10'],
            "nl":"Yes, I like it."
        },
        {
            "tag":['10'],
            "nl":"Yeah, definitely. I like that one."
        },
        {
            "tag":['10'],
            "nl":"Yeah, I'm fond of it."
        },
        {
            "tag":['10'],
            "nl":"Yeah, I'm really into it."
        },
        {
            "tag":['10'],
            "nl":"Yes, I'm fond of it."
        },
        {
            "tag":['10'],
            "nl":"Yes, I'm really into it."
        },
        {
            "tag":['10'],
            "nl":"Yes, I enjoy it."
        },
        {
            "tag":['10', '11'],
            "nl":"Great, I like it."
        },
        {
            "tag":['10', '11'],
            "nl":"Ooh that seems great!"
        },
        {
            "tag":['10', '11'],
            "nl":"That sounds great."
        },
        {
            "tag":['10', '11'],
            "nl":"Great, I enjoy it."
        },
        {
            "tag":['10', '11'],
            "nl":"It's pretty good."
        },
        {
            "tag":['10', '11'],
            "nl":"It's wonderful."
        },
        {
            "tag":['10', '11'],
            "nl":"It's ok."
        },
    ],
    "jacket_neg":[
        {
            "tag":['10'],
            "nl":"No."
        },
        {
            "tag":['10'],
            "nl":"No, I don't like it."
        },
        {
            "tag":['10'],
            "nl":"No, I do not like that kind of coats."
        },
        {
            "tag":['10'],
            "nl":"No, it does not appeal to me."
        },
        {
            "tag":['10', '11'],
            "nl":"I'm not fond of it."
        },
        {
            "tag":['10', '11'],
            "nl":"I don't like it."
        },
        {
            "tag":['10', '11'],
            "nl":"I dislike it."
        },
        {
            "tag":['11'],
            "nl":"It's not my cup of tea."
        },
        {
            "tag":['11'],
            "nl":"It's not my thing."
        },
        {
            "tag":['11'],
            "nl":"It's not really my thing."
        },
        {
            "tag":['11'],
            "nl":"It's not for me."
        },
        {
            "tag":['11'],
            "nl":"This type of coats doesn't suit me"
        },
        {
            "tag":['11'],
            "nl":"It does not appeal to me."
        },
        {
            "tag":['11'],
            "nl":"I'm not suited for this kind of coats."
        },
        {
            "tag":['20', '30'],
            "nl":"I don't like them."
        },
        {
            "tag":['20', '30'],
            "nl":"I'm not fond of them."
        },
        {
            "tag":['20', '30'],
            "nl":"They don't appeal to me."
        },
        {
            "tag":['20', '30'],
            "nl":"I dislike them."
        },
        {
            "tag":['20', '30'],
            "nl":"They are not my cup of tea."
        },
        {
            "tag":['20', '30'],
            "nl":"They are not my thing."
        },
        {
            "tag":['20', '30'],
            "nl":"They are not really my thing."
        },
        {
            "tag":['20', '30'],
            "nl":"They are not for me."
        },
        {
            "tag":['20', '30'],
            "nl":"They don't appeal to me."
        },
        {
            "tag":['20', '30'],
            "nl":"I'm not suited for these kind of coats."
        },
        {
            "tag":['20', '30'],
            "nl":"No."
        },
    ],

    "color":[
        {
            "tag":['00','01', '20', '30'],
            "slots":["color"],
            "nl":"$color$."
        },
       {
            "tag":['00', '01', '20', '30'],
            "slots":["color"],
            "nl":"The $color$."
        },
        {
            "tag":['00','20', '30'],
            "slots":["color"],
            "nl":"I like $color$."
        },
        {
            "tag":['00','20', '30'],
            "slots":["color"],
            "nl":"I'm in the mood to $color$."
        },
        {
            "tag":['00','20', '30'],
            "slots":["color"],
            "nl":"I love $color$ coats."
        },
        {
            "tag":['00','20', '30'],
            "slots":["color"],
            "nl":"I do enjoy $color$."
        },
        {
            "tag":['00','20', '30'],
            "slots":["color"],
            "nl":"I enjoy most $color$ coats."
        },
        {
            "tag":['00','20', '30'],
            "slots":["color"],
            "nl":"I'm really big on $color$ coats."
        },
        {
            "tag":['00', '01', '20', '30'],
            "slots":["color"],
            "nl":"$color$ is ok."
        },
        {
            "tag":['00','20', '30'],
            "slots":["color"],
            "nl":"I enjoy $color$ coats."
        },
        {
            "tag":['00','20', '30'],
            "slots":["color"],
            "nl":"I like wearing $color$ coats."
        },
        {
            "tag":['00','20', '30'],
            "slots":["color"],
            "nl":"The $color$ coats appeal to me."
        },
        {
            "tag":['01'],
            "slots":["color"],
            "nl":"I want the color of $color$."
        },
        {
            "tag":['01'],
            "slots":["color"],
            "nl":"I need the color of $color$."
        },
        {
            "tag":['01'],
            "slots":["color"],
            "nl":"I want $color$ coats."
        },
        {
            "tag":['01'],
            "slots":["color"],
            "nl":"I need $color$ coats."
        },
        {
            "tag":['02'],
            "slots":["color"],
            "nl":"$color$ coats suit me."
        },
    ],
    "color_pos":[
        {
            "tag":['10'],
            "nl":"Yes."
        },
        {
            "tag":['10'],
            "nl":"Yes, I like it."
        },
        {
            "tag":['10'],
            "nl":"Yeah, I'm fond of it."
        },
        {
            "tag":['10'],
            "nl":"Yeah, definitely. I like that one."
        },
        {
            "tag":['10'],
            "nl":"Yeah, I'm really into it."
        },
        {
            "tag":['10'],
            "nl":"Yes, I'm fond of it."
        },
        {
            "tag":['10'],
            "nl":"Yes, I'm really into it."
        },
        {
            "tag":['10'],
            "nl":"Yes, I enjoy it."
        },
        {
            "tag":['10', '11'],
            "nl":"Great, I like it."
        },
        {
            "tag":['10', '11'],
            "nl":"Ooh that seems great!"
        },
        {
            "tag":['10', '11'],
            "nl":"That sounds great."
        },
        {
            "tag":['10', '11'],
            "nl":"Great, I enjoy it."
        },
        {
            "tag":['11'],
            "nl":"It's pretty good."
        },
        {
            "tag":['11'],
            "nl":"It's wonderful."
        },
        {
            "tag":['11'],
            "nl":"It's ok."
        },
    ],
    "color_neg":[
        {
            "tag":['10'],
            "nl":"No."
        },
        {
            "tag":['10'],
            "nl":"No, I don't like it."
        },
        {
            "tag":['10'],
            "nl":"No, I do not like that color."
        },
        {
            "tag":['10'],
            "nl":"No, it does not appeal to me."
        },
        {
            "tag":['10', '11'],
            "nl":"I don't like it."
        },
        {
            "tag":['10', '11'],
            "nl":"I'm not fond of it."
        },
        {
            "tag":['10', '11'],
            "nl":"I dislike it."
        },
        {
            "tag":['11'],
            "nl":"It's not my cup of tea."
        },
        {
            "tag":['11'],
            "nl":"It's not my thing."
        },
        {
            "tag":['11'],
            "nl":"It's not really my thing."
        },
        {
            "tag":['11'],
            "nl":"It's not for me."
        },
        {
            "tag":['11'],
            "nl":"This color of coats doesn't suit me."
        },
        {
            "tag":['11'],
            "nl":"It does not appeal to me."
        },
        {
            "tag":['11'],
            "nl":"I don't suit this color coats."
        },
        {
            "tag":['20', '30'],
            "nl":"I don't like them."
        },
        {
            "tag":['20', '30'],
            "nl":"They don't appeal to me."
        },
        {
            "tag":['20', '30'],
            "nl":"I dislike them."
        },
        {
            "tag":['20', '30'],
            "nl":"They are not my cup of tea."
        },
        {
            "tag":['20', '30'],
            "nl":"They are not my thing."
        },
        {
            "tag":['20', '30'],
            "nl":"They are  not really my thing."
        },
        {
            "tag":['20', '30'],
            "nl":"They are not for me."
        },
        {
            "tag":['20', '30'],
            "nl":"They don't appeal to me."
        },
        {
            "tag":['20', '30'],
            "nl":"I'm not suited for these colors."
        },
        {
            "tag":['20', '30'],
            "nl":"I'm not fond of them."
        },
        {
            "tag":['20', '30'],
            "nl":"No."
        },
    ],
}

start_pattern = [
    "Hi, I'm looking for a coat.",
    "Can you recommend a coat?",
    "Can you help me find a coat?",
    "Can you find me a coat?",
    "Please help me find a coat.",
    "Hi, I'm going to buy a coat.",
    "Hello, I'm looking for a coat.",
    "Hi, I need a coat.",
    "Hi, I'm dying for a coat.",
    "Hi, I'm trying to find a coat.",
    "Hi there, I'm looking for coat recommendations.",
    "Hello, what coats would you suggest?",
    "Which coats do you suggest?",
    "Hi! I'm looking for some suggestions for good coats.What would you recommend?",
    "Hi! I am looking for a coat.",
    "Hi, do you have any coat suggestions for me?",
    "Hey, could you suggest some coats for me?",
    "Hi there. Do you think you could suggest some coats for me today?",
    "Hey could you help me find a coat?",
    "Hi, could you help me find a good coat?",
    "Could you please help me find a good coat?",
    "Hi I am looking for a good new coat."
]