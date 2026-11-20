import cocotb
from cocotb.triggers import Timer
from cocotb.types import LogicArray


async def _apply(dut, d, sel):
    """Drive inputs and wait for combinational logic to settle."""
    dut.d.value = d
    dut.sel.value = sel
    await Timer(1, unit="ns")


@cocotb.test()
async def test_no_select_outputs_zero(dut):
    """Rule 2: sel=0000 must always output 0 regardless of d."""
    for d_val in range(16):
        await _apply(dut, d_val, 0b0000)
        assert int(dut.y.value) == 0, f"Expected 0 when sel=0, d={d_val:04b}"


@cocotb.test()
async def test_onehot_selects_individual_bits(dut):
    """Rule 1: Single active sel[i] routes d[i] to y."""
    for i in range(4):
        sel_val = 1 << i
        await _apply(dut, sel_val, sel_val)
        assert int(dut.y.value) == 1, f"Bit {i} failed to pass 1"

        await _apply(dut, ~sel_val & 0xF, sel_val)
        assert int(dut.y.value) == 0, f"Bit {i} failed to pass 0"


@cocotb.test()
async def test_full_256_combinations(dut):
    """Rules 1, 2, & 3: Exhaustive check of all 256 combinations."""
    for d_val in range(16):
        for sel_val in range(16):
            await _apply(dut, d_val, sel_val)
            expected = int((d_val & sel_val) != 0)
            actual = int(dut.y.value)
            assert actual == expected, (
                f"d={d_val:04b}, sel={sel_val:04b}: expected {expected}, got {actual}"
            )


@cocotb.test()
async def test_unselected_x_is_masked(dut):
    """Edge: Unknowns (X) on unselected data bits must not corrupt y."""
    await _apply(dut, LogicArray("XXX1"), 0b0001)
    assert dut.y.value.is_resolvable and int(dut.y.value) == 1

    await _apply(dut, LogicArray("XXX0"), 0b0001)
    assert dut.y.value.is_resolvable and int(dut.y.value) == 0


@cocotb.test()
async def test_selected_x_propagates(dut):
    """Edge: An X on a selected bit (when no other selected bit is 1) propagates."""
    await _apply(dut, LogicArray("000X"), 0b0001)
    assert not dut.y.value.is_resolvable