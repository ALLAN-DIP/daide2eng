from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Iterable, List

from daide2eng.constants import *
from daide2eng.keywords.base_keywords import *
from daide2eng.keywords.daide_object import _DAIDEObject
from daide2eng.keywords.keyword_utils import and_items, or_items

@dataclass(eq=True, frozen=True)
class PCE(_DAIDEObject):
    powers: Tuple[Power]

    def __init__(self, *powers: Power):
        object.__setattr__(self, "powers", tuple(sorted(set(powers))))
        self.__post_init__()

    def __post_init__(self):
        super().__post_init__()
        if len(self.powers) < 2:
            raise ValueError("A peace must have at least 2 powers.")

    def __str__(self):
        return "peace between " + and_items(self.powers)


@dataclass(eq=True, frozen=True)
class CCL(_DAIDEObject):
    press_message: PressMessage

    def __str__(self):
        return f"cancel \"{self.press_message}\" "


@dataclass(eq=True, frozen=True)
class TRY(_DAIDEObject):
    try_tokens: Tuple[TryTokens]

    def __init__(self, *try_tokens):
        object.__setattr__(self, "try_tokens", tuple(sorted(set(try_tokens))))
        self.__post_init__()

    def __post_init__(self):
        super().__post_init__()
        if not self.try_tokens:
            raise ValueError("A TRY message must have at least 1 token.")

    def __str__(self):
        return "try the following tokens: " + " ".join(self.try_tokens) + " "


@dataclass(eq=True, frozen=True)
class HUH(_DAIDEObject):
    press_message: PressMessage

    def __str__(self):
        return f"not understand \"{self.press_message}\" "


@dataclass(eq=True, frozen=True)
class PRP(_DAIDEObject):
    arrangement: Arrangement

    def __str__(self):
        return f"propose {self.arrangement} "


@dataclass(eq=True, frozen=True)
class ALYVSS(_DAIDEObject):
    aly_powers: Tuple[Power]
    vss_powers: Tuple[Power]

    def __init__(self, aly_powers: Iterable[Power], vss_powers: Iterable[Power]):
        object.__setattr__(self, "aly_powers", tuple(sorted(set(aly_powers))))
        object.__setattr__(self, "vss_powers", tuple(sorted(set(vss_powers))))
        self.__post_init__()

    def __post_init__(self):
        super().__post_init__()
        if len(self.aly_powers) < 2:
            raise ValueError("An alliance must have at least 2 allies.")
        if len(self.vss_powers) < 1:
            raise ValueError("An alliance must have at least 1 enemy.")

    def __str__(self):
        return (
            "an alliance with "
            + and_items(self.aly_powers)
            + "against "
            + and_items(self.vss_powers)
        )


@dataclass(eq=True, frozen=True)
class SLO(_DAIDEObject):
    power: Power

    def __str__(self):
        return f"{self.power} solo"


@dataclass(eq=True, frozen=True)
class NOT(_DAIDEObject):
    arrangement_qry: Union[Arrangement, QRY]

    def __str__(self):
        return f"not {self.arrangement_qry} "


@dataclass(eq=True, frozen=True)
class NAR(_DAIDEObject):
    arrangement: Arrangement

    def __str__(self):
        return f"lack of arragement: {self.arrangement} "


@dataclass(eq=True, frozen=True)
class DRW(_DAIDEObject):
    powers: Tuple[Power]

    def __init__(self, *powers: Power):
        object.__setattr__(self, "powers", tuple(sorted(set(powers))))
        self.__post_init__()

    def __post_init__(self):
        super().__post_init__()
        if len(self.powers) == 1:
            raise ValueError("A draw cannot involve only a single power.")

    def __str__(self):
        if self.powers:
            return and_items(self.powers) + "draw "
        else:
            return f"draw"


@dataclass(eq=True, frozen=True)
class YES(_DAIDEObject):
    press_message: PressMessage

    def __str__(self):
        return f"accept {self.press_message} "


@dataclass(eq=True, frozen=True)
class REJ(_DAIDEObject):
    press_message: PressMessage

    def __str__(self):
        return f"reject {self.press_message} "


@dataclass(eq=True, frozen=True)
class BWX(_DAIDEObject):
    press_message: PressMessage

    def __str__(self):
        return f"refuse answering to {self.press_message} "


@dataclass(eq=True, frozen=True)
class FCT(_DAIDEObject):
    arrangement_qry_not: Union[Arrangement, QRY, NOT]

    def __str__(self):
        return f"doing the following in the current round: \"{self.arrangement_qry_not}\" "


@dataclass(eq=True, frozen=True)
class FRM(_DAIDEObject):
    frm_power: Power
    recv_powers: Tuple[Power]
    message: Message

    def __init__(
        self, frm_power: Power, recv_powers: Iterable[Power], message: Message
    ):
        object.__setattr__(self, "frm_power", frm_power)
        object.__setattr__(self, "recv_powers", tuple(sorted(set(recv_powers))))
        object.__setattr__(self, "message", message)
        self.__post_init__()

    def __post_init__(self):
        super().__post_init__()
        if not self.recv_powers:
            raise ValueError("A FRM must have at least 1 receiving power.")

    def __str__(self):
        return (
            f"from {self.frm_power} to "
            + and_items(self.recv_powers)
            + f": \"{self.message}\" "
        )


@dataclass(eq=True, frozen=True)
class XDO(_DAIDEObject):
    order: Command

    def __str__(self):
        return f"an order {self.order} "


@dataclass(eq=True, frozen=True)
class DMZ(_DAIDEObject):
    """This is an arrangement for the listed powers to remove all units from, and not order to, support to, convoy to, retreat to, or build any units in any of the list of provinces. Eliminated powers must not be included in the power list. The arrangement is continuous (i.e. it isn't just for the current turn)."""

    powers: Tuple[Power]
    provinces: Tuple[Location]
    exhaustive_provinces: Tuple[Location] = field(init=False)

    def __init__(self, powers: Iterable[Power], provinces: Iterable[Location]):
        object.__setattr__(self, "powers", tuple(sorted(set(powers))))
        object.__setattr__(self, "provinces", tuple(sorted(set(provinces))))

        exhaustive_provinces: List[Location] = []
        for province in self.provinces:
            if province == Location(province="STP"):
                exhaustive_provinces.append(Location(province="STP"))
                exhaustive_provinces.append(Location(province="STP", coast="NCS"))
                exhaustive_provinces.append(Location(province="STP", coast="SCS"))
            elif province == Location(province="SPA"):
                exhaustive_provinces.append(Location(province="SPA"))
                exhaustive_provinces.append(Location(province="SPA", coast="NCS"))
                exhaustive_provinces.append(Location(province="SPA", coast="SCS"))
            elif province == Location(province="BUL"):
                exhaustive_provinces.append(Location(province="BUL"))
                exhaustive_provinces.append(Location(province="BUL", coast="ECS"))
                exhaustive_provinces.append(Location(province="BUL", coast="SCS"))
            else:
                exhaustive_provinces.append(province)

        object.__setattr__(
            self, "exhaustive_provinces", tuple(sorted(set(exhaustive_provinces)))
        )

        self.__post_init__()

    def __post_init__(self):
        super().__post_init__()
        if not self.powers:
            raise ValueError("A DMZ must involve at least 1 power.")
        if not self.provinces:
            raise ValueError("A DMZ must include at least 1 province.")

    def __str__(self):
        return (
            and_items(self.powers)
            + "demilitarize "
            + and_items(list(map(lambda x: str(x), self.provinces)))
        )


@dataclass(eq=True, frozen=True)
class AND(_DAIDEObject):
    arrangements: Tuple[Arrangement]

    def __init__(self, *arrangements: Arrangement):
        object.__setattr__(
            self, "arrangements", tuple(sorted(set(arrangements), key=str))
        )
        self.__post_init__()

    def __post_init__(self):
        super().__post_init__()
        if len(self.arrangements) < 2:
            raise ValueError("An AND must have at least 2 arrangements.")

    def __str__(self):
        return and_items(self.arrangements)


@dataclass(eq=True, frozen=True)
class ORR(_DAIDEObject):
    arrangements: Tuple[Arrangement]

    def __init__(self, *arrangements: Arrangement):
        object.__setattr__(
            self, "arrangements", tuple(sorted(set(arrangements), key=str))
        )
        self.__post_init__()

    def __post_init__(self):
        super().__post_init__()
        if len(self.arrangements) < 2:
            raise ValueError("An ORR must have at least 2 arrangements.")

    def __str__(self):
        return or_items(self.arrangements)


@dataclass(eq=True, frozen=True)
class PowerAndSupplyCenters:
    power: Power
    supply_centers: Tuple[Location]  # Supply centers

    def __init__(self, power, *supply_centers: Location):
        object.__setattr__(self, "power", power)
        object.__setattr__(self, "supply_centers", tuple(sorted(set(supply_centers))))
        self.__post_init__()

    def __post_init__(self):
        if not self.supply_centers:
            raise ValueError(
                "A PowerAndSupplyCenters must have at least 1 supply center."
            )

    def __str__(self):
        return f"{self.power} to have " + and_items(list(map(lambda x: str(x), self.supply_centers)))


@dataclass(eq=True, frozen=True)
class SCD(_DAIDEObject):
    power_and_supply_centers: Tuple[PowerAndSupplyCenters]

    def __init__(self, *power_and_supply_centers: PowerAndSupplyCenters):
        object.__setattr__(
            self,
            "power_and_supply_centers",
            tuple(sorted(set(power_and_supply_centers), key=str)),
        )
        self.__post_init__()

    def __post_init__(self):
        super().__post_init__()
        if not self.power_and_supply_centers:
            raise ValueError("An SCD must have at least 1 power and supply center.")

    def __str__(self):
        pas_str = [str(pas) + " " for pas in self.power_and_supply_centers]
        return f"an arragement of supply centre distribution as follows: " + and_items(pas_str)


@dataclass(eq=True, frozen=True)
class OCC(_DAIDEObject):
    units: Tuple[Unit]

    def __init__(self, *units: Unit):
        object.__setattr__(self, "units", tuple(sorted(set(units), key=str)))
        self.__post_init__()

    def __post_init__(self):
        super().__post_init__()
        if not self.units:
            raise ValueError("An OCC must have at least 1 unit.")

    def __str__(self):
        unit_str = [str(unit) for unit in self.units]
        return f"placing " + and_items(unit_str)


@dataclass(eq=True, frozen=True)
class CHO(_DAIDEObject):
    minimum: int
    maximum: int
    arrangements: Tuple[Arrangement]

    def __init__(self, minimum: int, maximum: int, *arrangements: Arrangement):
        object.__setattr__(self, "minimum", minimum)
        object.__setattr__(self, "maximum", maximum)
        object.__setattr__(
            self, "arrangements", tuple(sorted(set(arrangements), key=str))
        )
        self.__post_init__()

    def __post_init__(self):
        super().__post_init__()
        if not self.arrangements:
            raise ValueError("A CHO must have at least 1 arrangement.")

    def __str__(self):
        if self.minimum == self.maximum:
            return f"choosing {self.minimum} in " + and_items(self.arrangements)
        else:
            return f"choosing between {self.minimum} and {self.maximum} in " + and_items(self.arrangements)


@dataclass(eq=True, frozen=True)
class INS(_DAIDEObject):
    arrangement: Arrangement

    def __str__(self):
        return f"insist {self.arrangement} "


@dataclass(eq=True, frozen=True)
class QRY(_DAIDEObject):
    arrangement: Arrangement

    def __str__(self):
        return f"Is {self.arrangement} true? "


@dataclass(eq=True, frozen=True)
class THK(_DAIDEObject):
    arrangement_qry_not: Union[Arrangement, QRY, NOT, None]

    def __str__(self):
        return f"think {self.arrangement_qry_not} is true "


@dataclass(eq=True, frozen=True)
class IDK(_DAIDEObject):
    qry_exp_wht_prp_ins_sug: Union[QRY, EXP, WHT, PRP, INS, SUG]

    def __str__(self):
        return f"don't know about {self.qry_exp_wht_prp_ins_sug} "


@dataclass(eq=True, frozen=True)
class SUG(_DAIDEObject):
    arrangement: Arrangement

    def __str__(self):
        return f"suggest {self.arrangement} "


@dataclass(eq=True, frozen=True)
class WHT(_DAIDEObject):
    unit: Unit

    def __str__(self):
        return f"What do you think about {self.unit} ? "


@dataclass(eq=True, frozen=True)
class HOW(_DAIDEObject):
    province_power: Union[Location, Power]

    def __str__(self):
        return f"How do you think we should attack {self.province_power} ? "


@dataclass(eq=True, frozen=True)
class EXP(_DAIDEObject):
    turn: Turn
    message: Message
    power: str

    def __str__(self):
        return f"The explanation for what {self.power} did in {self.turn} is {self.message} "


@dataclass(eq=True, frozen=True)
class SRY(_DAIDEObject):
    exp: EXP

    def __str__(self):
        return f"I'm sorry about {self.exp} "


@dataclass(eq=True, frozen=True)
class FOR(_DAIDEObject):
    start_turn: Turn
    end_turn: Optional[Turn]
    arrangement: Arrangement

    def __str__(self):
        if not self.end_turn:
            return f"{self.arrangement} in {self.start_turn} "
        else:
            return f"{self.arrangement} from {self.start_turn} to {self.end_turn} "


@dataclass(eq=True, frozen=True)
class IFF(_DAIDEObject):
    arrangement: Arrangement
    press_message: PressMessage
    els_press_message: Optional[PressMessage] = None

    def __str__(self):
        if not self.els_press_message:
            return f"if {self.arrangement} then \"{self.press_message}\" "
        else:
            return f"if {self.arrangement} then \"{self.press_message}\" else \"{self.els_press_message}\" "


@dataclass(eq=True, frozen=True)
class XOY(_DAIDEObject):
    power_x: Power
    power_y: Power

    def __str__(self):
        return f"{self.power_x} owes {self.power_y} "


@dataclass(eq=True, frozen=True)
class YDO(_DAIDEObject):
    power: Power
    units: Tuple[Unit]

    def __init__(self, power, *units):
        object.__setattr__(self, "power", power)
        object.__setattr__(self, "units", tuple(sorted(set(units), key=str)))
        self.__post_init__()

    def __str__(self):
        unit_str = [str(unit) for unit in self.units]
        return f"giving {self.power} the control of" + and_items(unit_str)


@dataclass(eq=True, frozen=True)
class SND(_DAIDEObject):
    power: Power
    recv_powers: Tuple[Power]
    message: Message

    def __init__(self, power: Power, recv_powers: Iterable[Power], message: Message):
        object.__setattr__(self, "power", power)
        object.__setattr__(self, "recv_powers", tuple(sorted(set(recv_powers))))
        object.__setattr__(self, "message", message)
        self.__post_init__()

    def __post_init__(self):
        super().__post_init__()
        if not self.recv_powers:
            raise ValueError("A SND must have at least 1 receiving power.")

    def __str__(self):

        return (
            f"{self.power} sending {self.message} to "
            + and_items(self.recv_powers)
        )


@dataclass(eq=True, frozen=True)
class FWD(_DAIDEObject):
    powers: Tuple[Power]
    power_1: Power
    power_2: Power

    def __init__(self, powers: Iterable[Power], power_1: Power, power_2: Power):
        object.__setattr__(self, "powers", tuple(sorted(set(powers))))
        object.__setattr__(self, "power_1", power_1)
        object.__setattr__(self, "power_2", power_2)
        self.__post_init__()

    def __post_init__(self):
        super().__post_init__()
        if not self.powers:
            raise ValueError("A FWD must have at least 1 receiving power.")

    def __str__(self):
        return (
            f"forwarding to {self.power_2} if {self.power_1} receives message from "
            + and_items(self.powers)
        )


@dataclass(eq=True, frozen=True)
class BCC(_DAIDEObject):
    power_1: Power
    powers: Tuple[Power]
    power_2: Power

    def __init__(self, power_1: Power, powers: Iterable[Power], power_2: Power):
        object.__setattr__(self, "power_1", power_1)
        object.__setattr__(self, "powers", tuple(sorted(set(powers))))
        object.__setattr__(self, "power_2", power_2)
        self.__post_init__()

    def __post_init__(self):
        super().__post_init__()
        if not self.powers:
            raise ValueError("A BCC must have at least 1 receiving power.")

    def __str__(self):
        return (
            f"forwarding to {self.power_2} if {self.power_1} sends message to "
            + and_items(self.powers)
        )


@dataclass(eq=True, frozen=True)
class WHY(_DAIDEObject):
    fct_thk_prp_ins: Union[FCT, THK, PRP, INS]

    def __str__(self):
        return f"Why do you believe \"{self.fct_thk_prp_ins}\" ? "


@dataclass(eq=True, frozen=True)
class POB(_DAIDEObject):
    why: WHY

    def __str__(self):
        return f"answer \"{self.why}\": the position on the board, or the previous moves, suggests/implies it "


@dataclass(eq=True, frozen=True)
class UHY(_DAIDEObject):
    press_message: PressMessage

    def __str__(self):
        return f"am unhappy that \"{self.press_message}\" "


@dataclass(eq=True, frozen=True)
class HPY(_DAIDEObject):
    press_message: PressMessage

    def __str__(self):
        return f"am happy that \"{self.press_message}\" "


@dataclass(eq=True, frozen=True)
class ANG(_DAIDEObject):
    press_message: PressMessage

    def __str__(self):
        return f"am angry that \"{self.press_message}\" "


@dataclass(eq=True, frozen=True)
class ROF(_DAIDEObject):
    def __str__(self):
        return f"requesting an offer"


@dataclass(eq=True, frozen=True)
class ULB(_DAIDEObject):
    power: Power
    float_val: float

    def __str__(self):
        return f"having a utility lower bound of float for {self.power} is {self.float_val} "


@dataclass(eq=True, frozen=True)
class UUB(_DAIDEObject):
    power: Power
    float_val: float

    def __str__(self):
        return f"having a utility upper bound of float for {self.power} is {self.float_val} "


Reply = Union[YES, REJ, BWX, HUH, FCT, THK, IDK, WHY, POB, UHY, HPY, ANG]
PressMessage = Union[
    PRP,
    CCL,
    FCT,
    TRY,
    FRM,
    THK,
    INS,
    QRY,
    SUG,
    HOW,
    WHT,
    EXP,
    IFF,
]
Message = Union[PressMessage, Reply]
Arrangement = Union[
    PCE,
    ALYVSS,
    DRW,
    XDO,
    DMZ,
    AND,
    ORR,
    SCD,
    CHO,
    FOR,
    XOY,
    YDO,
    SND,
    FWD,
    BCC,
    ULB,
    UUB,
    ROF,
]

AnyDAIDEToken = Union[
    RTO,
    DSB,
    BLD,
    REM,
    WVE,
    HLD,
    MTO,
    SUP,
    CVY,
    MoveByCVY,
    YES,
    REJ,
    BWX,
    HUH,
    WHY,
    POB,
    IDK,
    PRP,
    CCL,
    FCT,
    TRY,
    FRM,
    THK,
    INS,
    QRY,
    SUG,
    HOW,
    WHT,
    EXP,
    IFF,
    PCE,
    ALYVSS,
    DRW,
    XDO,
    DMZ,
    AND,
    ORR,
    SCD,
    CHO,
    FOR,
    XOY,
    YDO,
    SND,
    FWD,
    BCC,
    SLO,
    NOT,
    NAR,
    OCC,
    SRY,
    UHY,
    HPY,
    ANG,
    ROF,
    ULB,
    UUB,
]
