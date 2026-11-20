import cocotb 
from cocotb.triggers import Timer

@cocotb.test()
async def test_and_gate(dut):

    for a_val in range (16):
        for b_val in range (16): 
            dut.a.value = a_val
            dut.b.value = b_val
    
            await Timer(1, unit="ns")
            expected_c = a_val & b_val
            actual_C = int(dut.c.value)
            assert actual_C == expected_c, (f"Expected {expected_c} but got {actual_C}")
   
    dut._log.info("PASS: All 256 4-bit bitwise AND combinations passed!")