"""Full hierarchical entity names for discovered PLC symbols."""

import pytest

from custom_components.ha_opcua.names import full_hierarchy_name, join_hierarchy


@pytest.mark.parametrize(
    ("node_id", "leaf", "expected"),
    [
        ('ns=4;s="HA_DATA"."Battery1"."Power"', "Power", "HA_DATA.Battery1.Power"),
        (
            'ns=4;s="HA_DATA"."Battery1"."CellVoltageArr"."[1]"',
            "[1]",
            "HA_DATA.Battery1.CellVoltageArr[1]",
        ),
        (
            "ns=2;s=|var|PLC.PlantRelay.astMeldungen[10].xAktiv",
            "xAktiv",
            "PLC.PlantRelay.astMeldungen[10].xAktiv",
        ),
        ("ns=2;i=42", "Power", "Power"),
        ('ns=4;s="Standalone"', "Standalone", "Standalone"),
    ],
)
def test_symbolic_name_contains_complete_hierarchy(node_id, leaf, expected):
    assert full_hierarchy_name(node_id, leaf) == expected


def test_browse_path_works_for_opaque_node_ids():
    assert join_hierarchy(("HA_DATA", "Battery1", "Power")) == "HA_DATA.Battery1.Power"
    assert join_hierarchy(("HA_DATA", "Battery1", "CellVoltageArr", "[1]")) == (
        "HA_DATA.Battery1.CellVoltageArr[1]"
    )
