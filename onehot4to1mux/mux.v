module mux (
    input [3:0] d,
    input [3:0] sel,
    output y


);

    assign y = |(d & sel);

endmodule