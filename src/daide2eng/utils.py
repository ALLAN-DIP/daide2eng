from daide2eng import create_daide_grammar
from daide2eng import daide_visitor
from daide2eng.keywords.keyword_utils import power_dict, power_list
from typing import List
import parsimonious

# create daide grammar
grammar = create_daide_grammar(
    level=160,
)

def pre_process(daide: str) -> str:
    '''
        change the dipnet syntax to daidepp syntax
    '''
    # substitutions
    # case CTO province VIA (sea_province sea_province ...)

    # case RTO province

    # case DMZ (power power ...) (province province ...)

    # case HOW (province)

    # since 'ENG' is used both as a power and a location, we need to substitute
    # the location with 'ECH'.
    # and replace coast with SCS, NCS, ECS, WCS
    return daide.replace('BOT', 'GOB') \
                .replace('FLT ENG', 'FLT ECH') \
                .replace('AMY ENG', 'AMY ECH') \
                .replace('CTO LON', 'CTO ECH') \
                .replace('/SC', ' SCS') \
                .replace('/NC', ' NCS') \
                .replace('/EC', ' ECS') \
                .replace('/WC', ' WCS')


def gen_English(daide: str, sender="I", recipient="You", make_natural=True) -> str:
    '''
    Generate English from DAIDE. If make_natural is true, first and 
    second person pronouns/possessives will be used instead. We don't
    recommend passing in make_natural=False unless there is a
    specific reason to do so.

    :param daide: DAIDE string, e.g. '(ENG FLT LON) BLD'
    :param sender: power sending the message, e.g., 'ENG'
    :param recipient: power to which the message is sent, e.g., 'TUR'
    '''

    if not make_natural and (not sender or not recipient):
        return "ERROR: sender and recipient must be provided if make_natural is False"

    try:
        parse_tree = grammar.parse(pre_process(daide))
        return post_process(str(daide_visitor.visit(parse_tree)), sender, recipient, make_natural)

    except ValueError as e:
        return "ERROR value: " + str(e)
    except parsimonious.exceptions.ParseError:
        return "ERROR parsing " + daide


def post_process(sentence: str, sender: str, recipient: str, make_natural: bool) -> str:
    '''
    Make the sentence more grammatical and readable
    :param sentence: string, e.g. 'reject propose build fleet LON'
    '''

    # if sender or recipient is not provided, use first and second
    # person (default case).
    if make_natural:
        AGENT_SUBJECTIVE = 'I'
        RECIPIENT_SUBJECTIVE = 'you'
        AGENT_POSSESSIVE = 'my'
        RECIPIENT_POSSESSIVE = 'your'
        AGENT_OBJECTIVE = 'me'
        RECIPIENT_OBJECTIVE = RECIPIENT_SUBJECTIVE

    else:
        AGENT_SUBJECTIVE = sender
        RECIPIENT_SUBJECTIVE = recipient
        AGENT_POSSESSIVE = sender + "'s"
        RECIPIENT_POSSESSIVE = recipient + "'s"
        AGENT_OBJECTIVE = sender
        RECIPIENT_OBJECTIVE = recipient

    output = sentence.replace("in <location>", "")
    output = output.replace("<country>'s", "")

    # general steps that apply to all types of daide messages
    output = AGENT_SUBJECTIVE + ' ' + output

    # remove extra spaces
    output = " ".join(output.split())

    # add period if needed
    if not output.endswith('.') or not output.endswith('?'):
        output += '.'

    # substitute power names with pronouns
    if make_natural:
        output = output.replace(' ' + sender + ' ', ' ' + AGENT_OBJECTIVE + ' ')
        output = output.replace(' ' + recipient + ' ', ' ' + RECIPIENT_OBJECTIVE + ' ')

    # case-dependent handling

    # REJ/YES
    if "reject" in output or "accept" in output:
        output = output.replace(
            'propose', RECIPIENT_POSSESSIVE + ' proposal of', 1)



    return output


# remove punctuations
def tokenize(sentence: str) -> List[str]:
    def trim_all(token: str) -> str:
        if len(token) > 0:
            token = token.strip()
        while len(token) > 0 and token[0] == '"':
            token = token[1:]
        while len(token) > 0 and not token[-1].isalnum():
            token = token[:-1]
        return token

    tokens = list(map(lambda x: trim_all(x),
                      sentence.replace('(', ' ')
                              .replace(')', ' ')
                              .split(' ')
                      ))

    return list(filter(None, tokens))


def is_daide(sentence: str) -> bool:
    # change to catch value error
    '''
    Check if the tokens are three uppercase letters
    '''
    PRESS_TOKENS = ['PRP', 'YES', 'REJ', 'BWX', 'HUH', 'CCL', 'FCT', 'TRY',
                    'INS', 'QRY', 'THK', 'IDK', 'WHT', 'HOW', 'EXP', 'SRY',
                    'IFF', 'FRM', 'WHY', 'POB', 'UHY', 'HPY', 'ANG']

    tokens = tokenize(pre_process(sentence))

    for token in tokens:
        if not token.isupper() or len(token) != 3:
            return False

    if sentence[:3] in PRESS_TOKENS:
        return True
    return False
