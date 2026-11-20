import cocotb
from cocotb.triggers import Timer
from cocotb.types import LogicArray

#arrange,act,assert
@cocotb.test()
async def test_encoder_init(dut):
    await Timer(1, units = "ns")
    assert (dut.out.value == 0)
    assert (dut.valid.value == 0)

@cocotb.test()
async def test_valid_init(dut):
    dut.a.value = 3
    await Timer(1, units = "ns")

    assert (dut.out.value == 0)
    assert (dut.valid.value == 1)

@cocotb.test()
async def test_out_init(dut):
    dut.en.value = 1
    dut.a.value = 4
    await Timer(1, units = "ns")


    assert (dut.out.value == 2)
    assert (dut.valid.value == 1)

@cocotb.test()
async def test_0_init(dut):
    dut.en.value = 0
    dut.a.value = 0
    await Timer(1, units = "ns")


    assert (dut.out.value == 0)
    assert (dut.valid.value == 0)

@cocotb.test()
async def test_all_values(dut):
    dut.en.value = 1
    for i in range (8):
        dut.a.value = 1 << i;        
        await Timer(1, unit = "ns")
        assert (dut.out.value == i)




