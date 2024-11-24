from sc2.bot_ai import BotAI
from typing import Callable, Tuple, List, Dict, Optional

from managers import *
from sc2.data import Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit
from sc2.units import Units
from sharpy.combat.zerg import MicroZerglings
from sharpy.knowledges import KnowledgeBot
from sharpy.managers.core import ManagerBase
from sharpy.managers.extensions import ChatManager
from sharpy.plans import BuildOrder
from sharpy.combat import Action, MoveType, GenericMicro, CombatModel

class MicroEvade(GenericMicro):
    def __init__(self):
        self.surround_move = False
        super().__init__()

    def group_solve_combat(self, units: Units, current_command: Action) -> Action:
        self.surround_move = False

        return current_command

    def unit_solve_combat(self, unit: Unit, current_command: Action) -> Action:
        best_position = self.pather.find_low_inside_ground(self.center, self.closest_group.center, 8)
        return Action(best_position, False)


class EvadeDummy(KnowledgeBot):
    def __init__(self):
        super().__init__("EvadeDummy")
        self.realtime_split = False

    async def create_plan(self) -> BuildOrder:
        return BuildOrder([])

    def configure_managers(self) -> Optional[List[ManagerBase]]:
        self.roles.set_tag_each_iteration = True
        self.combat.default_rules.unit_micros[UnitTypeId.ZERGLING] = MicroEvade()
        self.combat.default_rules.unit_micros[UnitTypeId.ROACH] = MicroEvade()
        self.combat.default_rules.unit_micros[UnitTypeId.STALKER] = MicroEvade()
        self.combat.default_rules.unit_micros[UnitTypeId.ADEPT] = MicroEvade()
        self.combat.default_rules.unit_micros[UnitTypeId.MARINE] = MicroEvade()
        self.combat.default_rules.unit_micros[UnitTypeId.MARAUDER] = MicroEvade()
        self.combat.default_rules.unit_micros[UnitTypeId.REAPER] = MicroEvade()
        self.combat.default_rules.unit_micros[UnitTypeId.PROBE] = MicroEvade()
        self.combat.default_rules.unit_micros[UnitTypeId.DRONE] = MicroEvade()
        self.combat.default_rules.unit_micros[UnitTypeId.SCV] = MicroEvade()
        return []

    async def on_step(self, iteration: int):
        await super().on_step(iteration)

        for unit in self.units:
            self.combat.add_unit(unit)
            self.combat.execute(unit.position.towards(self.units.center, -1), MoveType.Push)

        # self.combat.add_units(self.units)
        #
        # if self.units:
        #     self.combat.execute(self.units.center)
