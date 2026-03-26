from BaseClasses import CollectionState
from test.bases import WorldTestBase
from ..data import data


class PokemonCrystalTestBase(WorldTestBase):
    game = data.manifest.game


def verify_region_access(test, items_dont_collect, regions, items_collect=None):
    if items_collect is None:
        items_collect = items_dont_collect

    test.collect_all_but(items_dont_collect)
    for region in regions:
        test.assertFalse(test.can_reach_region(region),
                         f"Region {region} reachable without items {items_dont_collect}.")
    test.collect_by_name(items_collect)
    for region in regions:
        test.assertTrue(test.can_reach_region(region), f"Region {region} unreachable with items {items_collect}.")


def verify_location_access(test, items_dont_collect, locations, items_collect=None):
    if items_collect is None:
        items_collect = items_dont_collect

    # Reset state to avoid interference from prior collect calls
    test.multiworld.state = CollectionState(test.multiworld)
    test.collect_all_but(items_dont_collect)
    for location in locations:
        test.assertFalse(test.can_reach_location(location),
                         f"Location {location} reachable without items {items_dont_collect}.")
    test.collect_by_name(items_collect)
    for location in locations:
        test.assertTrue(test.can_reach_location(location),
                        f"Location {location} unreachable with items {items_collect}.")
