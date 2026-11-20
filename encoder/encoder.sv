module encoder (
    input  logic       en,
    input  logic [7:0] a,
    output logic       valid,
    output logic [2:0] out
);
    localparam S_1 =8'b0000_0001;
    localparam S_2 =8'b0000_0010;
    localparam S_3 =8'b0000_0100;
    localparam S_4 =8'b0000_1000;
    localparam S_5 =8'b0001_0000;
    localparam S_6 =8'b0010_0000;
    localparam S_7 =8'b0100_0000;
    localparam S_8 =8'b1000_0000;

    always_comb begin
        valid = '0;
        out = '0;

        if (|a) begin
            valid = 1'b1;
        end

        if (en)
            case(a)

            S_1 : out = 3'b000;
            S_2 : out = 3'b001;
            S_3 : out = 3'b010;
            S_4 : out = 3'b011;
            S_5 : out = 3'b100;
            S_6 : out = 3'b101;
            S_7 : out = 3'b110;
            S_8 : out = 3'b111;
            default : out = 3'b000;

            endcase 

    end  
    
endmodule
