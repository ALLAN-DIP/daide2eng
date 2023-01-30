from daidepp import create_daide_grammar
from daidepp.daide_visitor import DAIDEVisitor
import parsimonious

def gen_English(daide: str, self_power: str, send_power: str) -> str:
    '''
    Generate English from DAIDE
    :param daide: DAIDE string, e.g. '(ENG FLT LON) BLD'
    :param self_power: power sending the message
    :param send_power: power to which the message is sent
    '''

    try:
        # create daide grammar
        grammar = create_daide_grammar(level=130, allow_just_arrangement=True, string_type='all')
        parse_tree = grammar.parse(daide)
        daide_visitor = DAIDEVisitor(self_power, send_power)
        output = str(daide_visitor.visit(parse_tree))

        return post_process(output, self_power, send_power)
        
    except parsimonious.exceptions.ParseError:
        return 'ERROR parsing ' + daide
    
def post_process(sentence: str, self_power, send_power) -> str:
    '''
    Make the sentence more grammatical and readable
    :param sentence: DAIDE string, e.g. '(ENG FLT LON) BLD'
    '''

    # remove extra spaces
    output = " ".join(sentence.split())
    # add period if needed
    if not output.endswith('.') or not output.endswith('?'):
        output += '.'

    # first & second person possessive
    pattern = send_power + "'s"
    output = output.replace('your', pattern)
    pattern = self_power + "'s"
    output = output.replace('my', pattern)

    # First & second person substitution
    output = output.replace('you', send_power)
    output = output.replace('I', self_power)

    # Third singular s

    return output