SIM ?= verilator
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += $(PWD)/../rtl/sync_fifo.v
TOPLEVEL = sync_fifo
MODULE = test_fifo

# Enable FST waveform generation for Surfer
EXTRA_ARGS += --trace --trace-fst --trace-structs

# Optional: Set the output waveform filename explicitly
PLUSARGS += +trace

include $(shell cocotb-config --makefiles)/Makefile.sim
