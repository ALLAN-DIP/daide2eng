# A modified version of DAIDE++
when using `daide_visitor.visit(parse_tree)`, instead of returning a daide string, it returns the English translation of that string.

## Usage

```python3
from daide2eng.utils import gen_English, pre_process, post_process

SELF_POWER = "ENG"
SEND_POWER = "TUR"
DAIDE = "PRP (ALY (ENG TUR) VSS (RUS ITA FRA))"

generated_English = pre_process(DAIDE)
generated_English = gen_English(generated_English, SELF_POWER, SEND_POWER)
generated_English = post_process(generated_English, SELF_POWER, SEND_POWER)
print(generated_English)

```

# modified output:
I propose ENG solo, GER solo, RUS solo, ENG solo, GER solo, and RUS solo  

