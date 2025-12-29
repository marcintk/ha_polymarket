import logging
import pytest

from ..utils import parse_str, parse_float, parse_float_from_list

@pytest.mark.parametrize(
    ("attr_type", "attr_name", "attr_value", "required", "expected_type", "expected_value", "expected_message"),
    [
        (str,   'value', 'text', False, str, 'text', None),
        (str,   'value', '', False, str, '', None),
        (str,   'not-present', '', False, str, 'n/a', None),
        (str,   'not-present', '', True, str, 'n/a', "Attribute 'not-present' not found for 'n/a', returning default=n/a."),
        (float, 'value', '3.14', False, float, 3.14, None),
        (float, 'value', 'text', False, float, 0.0, "Failed to convert attribute 'value', returning default=0.0."),
        (float, 'not-present', '', False, float, 0.0, None),
        (float, 'not-present', '', True, float, 0.0, "Attribute 'not-present' not found for 'n/a', returning default=0.0."),
        (list,  'value', '[3.14]', False, float, 3.14, None),
        (list,  'value', '[3.14,2.28]', False, float, 3.14, None),
        (list,  'value', '3.14]', False, float, 0.0, "List attribute 'value' exceptioned: Extra data: line 1 column 5 (char 4)!"),
        (list,  'value', '', False, float, 0.0, "List attribute 'value' exceptioned: Expecting value: line 1 column 1 (char 0)!"),
        (list,  'value', '[]', False, float, 0.0, "List attribute 'value' has no valid number of items in '[]'!"),
        (list,  'not-present', '', False, float, 0.0, None),
        (list,  'not-present', '', True, float, 0.0, "List attribute 'not-present' not found for 'n/a'!"),
    ],
)
def test_parse(attr_type, attr_name:str, attr_value:str, required:False, expected_type, expected_value:float, expected_message: str, caplog) -> None:
    result = _run_parse(attr_type, attr_name, attr_value, required)

    assert isinstance(result, expected_type)
    assert result == expected_value

    any_logging = expected_message is not None
    assert len(caplog.records) == (1 if any_logging else 0)

    if any_logging:
        record = caplog.records[0]
        assert record.message == expected_message

def _run_parse(attr_type, attr_name:str, attr_value:str, required:False) -> float | str:
    holder = {'value': attr_value}

    if attr_type == str:
        return parse_str(holder, attr_name, required=required)

    if attr_type == float:
        return parse_float(holder, attr_name, required=required)

    if attr_type == list:
        return parse_float_from_list(holder, attr_name, required=required)

    assert False
