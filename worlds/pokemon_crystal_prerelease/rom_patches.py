from dataclasses import dataclass

from .utils import convert_to_ingame_text


@dataclass
class RomPatchEntry:
    bank: int
    address: int
    data: list[int]

    @property
    def rom_offset(self) -> int:
        if self.bank == 0:
            return self.address
        return (self.bank * 0x4000) + (self.address - 0x4000)


@dataclass
class RomPatch:
    name: str
    entries: list[RomPatchEntry]


ROM_PATCHES: list[RomPatch] = [
    # QwilfishText in fish.asm is missing its "@" terminator. The byte after the string is the
    # FishGroups chance byte which gets randomized per-seed, so the string reads into garbage.
    # Fix: write a terminated copy to free space at end of bank 0x24, update all 3 pointers.
    RomPatch("Fix QwilfishText missing terminator", [
        RomPatchEntry(bank=0x24, address=0x7E8E,
                      data=convert_to_ingame_text("ROUTES 12, 13, 32", string_terminator=True)),
        RomPatchEntry(bank=0x24, address=0x67CF, data=[0x8E, 0x7E]),
        RomPatchEntry(bank=0x24, address=0x681C, data=[0x8E, 0x7E]),
        RomPatchEntry(bank=0x24, address=0x686A, data=[0x8E, 0x7E]),
    ]),
]
