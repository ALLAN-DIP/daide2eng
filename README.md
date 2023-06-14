# A modified version of DAIDE++
when using `daide_visitor.visit(parse_tree)`, instead of returning a daide string, it returns the English translation of that string.

## Usage

```python3
from daide2eng.utils import gen_English

PROPOSER = "ENG"
RECIPIENT = "TUR"
PRP_DAIDE = "PRP (ALY (ENG TUR) VSS (RUS ITA FRA))"
YES_DAIDE = "YES (PRP (ALY (ENG TUR) VSS (RUS ITA FRA)))"

print(gen_English(YES_DAIDE, PROPOSER, RECIPIENT))

```

# Output:
I accept your proposal of an alliance with me and you against FRA, ITA, and RUS.
