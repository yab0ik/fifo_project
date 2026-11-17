`timescale 1ns / 1ps
module  sync_fifo #(
    parameter DATA_WIDTH = 8,
    parameter DEPTH = 8
)(
    input wire clk,
    input wire rst_n,

    // write 
    input wire wr_en,
    input wire [DATA_WIDTH - 1 : 0] wr_data,
    output wire full,

    //read
    input wire rd_en,
    output reg [DATA_WIDTH - 1 :0] rd_data,
    output wire empty

);

    localparam ADDR_WIDTH = $clog2(DEPTH);
    //The memory array (bit width_name_depth )
    reg [DATA_WIDTH - 1 : 0] mem [0 : DEPTH - 1];   

    // 4 bits but the extra 1 MSB to know when full/empty wrap around detection 
    reg [ADDR_WIDTH : 0] wr_ptr;
    reg [ADDR_WIDTH : 0] rd_ptr; 

    // Status Flags 
    assign empty = (wr_ptr == rd_ptr); //write pointer (wr_ptr) points to the next slot to write to, and the read pointer (rd_ptr) points to the slot holding the next piece of data to read so if wr_ptr == rd_ptr there is no unread data 

    assign full = (wr_ptr[ADDR_WIDTH] != rd_ptr[ADDR_WIDTH]) && (wr_ptr[ADDR_WIDTH - 1 : 0] == rd_ptr[ADDR_WIDTH - 1 : 0]);

    //write functionality 
    always@(posedge clk)begin 
        if(!rst_n)begin 
            wr_ptr <= 0;
        end 
        else if (wr_en && !full)begin 
            mem[wr_ptr[ADDR_WIDTH -1 : 0]]<= wr_data;
            wr_ptr <= wr_ptr + 1'b1;
        end
    end 

    // read functionality 
    always@(posedge clk)begin 
        if(!rst_n) begin 
            rd_ptr <=0;
            rd_data <=0;
        end 
        else if (rd_en && !empty)begin
            rd_data <= mem[rd_ptr[ADDR_WIDTH -1 : 0]];
            rd_ptr <= rd_ptr + 1'b1;
        end 
    end 
endmodule 
