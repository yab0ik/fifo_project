import random
from collections import deque
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ReadOnly

async def reset_dut(dut):
    dut.rst_n.value = 0
    dut.wr_en.value = 0
    dut.rd_en.value = 0
    dut.wr_data.value = 0
    for _ in range(3):
        await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1

@cocotb.test()
async def test_fifo_randomized(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await reset_dut(dut)

    depth = int(dut.DEPTH.value)
    golden_queue = deque()

    for cycle in range(500):
        # 1. Drive inputs cleanly on the falling edge (well before setup time)
        await FallingEdge(dut.clk)
        try_write = random.choice([True, False])
        try_read  = random.choice([True, False])
        data_in   = random.randint(0, (1 << int(dut.DATA_WIDTH.value)) - 1)

        dut.wr_en.value   = 1 if try_write else 0
        dut.wr_data.value = data_in
        dut.rd_en.value   = 1 if try_read else 0

        # 2. Check combinational flags right before the rising clock edge
        await ReadOnly()
        is_full  = int(dut.full.value)
        is_empty = int(dut.empty.value)

        assert is_full == (len(golden_queue) == depth), \
            f"Cycle {cycle}: FULL mismatch! RTL={is_full}, Expected={len(golden_queue) == depth}"
        assert is_empty == (len(golden_queue) == 0), \
            f"Cycle {cycle}: EMPTY mismatch! RTL={is_empty}, Expected={len(golden_queue) == 0}"

        # 3. Advance to the rising edge where RTL samples inputs and updates flip-flops
        await RisingEdge(dut.clk)

        expected_rd_data = None
        if try_read and not is_empty:
            expected_rd_data = golden_queue.popleft()

        if try_write and not is_full:
            golden_queue.append(data_in)

        # 4. Verify registered rd_data after non-blocking assignments settle
        if expected_rd_data is not None:
            await ReadOnly()
            actual_rd_data = int(dut.rd_data.value)
            assert actual_rd_data == expected_rd_data, \
                f"Cycle {cycle}: Data mismatch! RTL={actual_rd_data:#x}, Expected={expected_rd_data:#x}"
