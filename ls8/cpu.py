"""CPU functionality."""

import sys
HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
ST = 0b10000100
JMP = 0b01010100
PRA = 0b01001000 
IRET = 0b00010011
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8 # register
        self.ram = [0] * 256 ## memory store
        self.pc = 0 # cpu aounting program
        self.halted = False # 
        self.reg[SP] = 0xF4 # stack pointer variable
        self.ir = 0
        self.flag = 0b00000000
    

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print('Usage: ls8.py filename')
            sys.exit(1)
        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    comment_split = line.strip().split("#")
                    value = comment_split[0].strip()
                    if value == "":
                        continue
                    try:
                        
                        instruction = int(value, 2)
                        # print(value)
                    except ValueError:
                        print(f"Invalid number '{value}'")
                        sys.exit(1)

                    self.ram[address] = instruction
                    address += 1
                
        except FileNotFoundError:
            print(f"{sys.argv[0]} {sys.argv[1]} file not found")
            sys.exit()


    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, val):
        self.ram[address] = val


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            sum = self.reg[reg_a] * self.reg[reg_b]
            self.reg[reg_a] = sum
        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001
            else:
                self.flag
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')
        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    # def push_val(self, value):
        
    #     self.reg[SP] -= 1
        
    #     top_stack_addr = self.reg[SP]
    #     self.ram[top_stack_addr] = value

    # def pop_val(self):
    #     top_stack_addr = self.reg[SP]
    #     # value is to put in the register
    #     value = self.ram[top_stack_addr]
    #     # reg_num = self.ram_read(self.pc + 1)
    #     # self.reg[reg_num] = value
    #     self.reg[SP] += 1
    #     return value

      
    def run(self):
        """Run the CPU."""

        halted = self.halted # false
        pc = self.pc # Program Counter, pointer tp the instruction we're executing
        while not halted:
            instruction = self.ram[pc]

            if instruction == HLT:
                halted = True
                pc += 1 

            elif instruction == PRN:
                reg_num = self.ram_read(pc + 1)
                print(self.reg[reg_num])
                pc += 2               
                 # save the register 
            
            elif instruction == LDI: 
                reg_num = self.ram_read(pc + 1)
                self.reg[reg_num] = self.ram_read(pc + 2)
                pc += 3

            elif instruction == MUL: # 
                reg_num = self.ram_read(pc + 1)
                reg_num2 = self.ram_read(pc + 2)
                self.reg[reg_num] = self.reg[reg_num] * self.reg[reg_num2]
                pc += 3   

            elif instruction == PUSH:
                # decrement the stack pointer

                self.reg[SP] -= 1
                reg_num = self.ram_read(pc + 1)
                # this is what we want to push to stack
                value = self.reg[reg_num] 
                # copy the value on the stack
                top_stack_addr = self.reg[SP]

                self.ram[top_stack_addr] = value
               
                pc += 2

            elif instruction == POP:
                # GEt value from top of stack
                top_stack_addr = self.reg[SP]
                # value is to put in the register
                value = self.ram_read(top_stack_addr)
                # Store in a register
                reg_num = self.ram_read(pc + 1)
                self.reg[reg_num] = value
                # Increment the SP by 1
                self.reg[SP] += 1
                # running pc by 2 
                pc += 2
     
            elif instruction == CALL:
                # Get address of the next instrcition after the Call
                reg_num = self.ram_read(pc + 1)
               
                return_addr = pc + 2
                self.reg[SP] -= 1
                memory_addr = self.reg[SP]
                self.ram[memory_addr] = return_addr
                sub_routine = self.reg[reg_num]
                pc = sub_routine
            elif instruction == RET:
                stack_addr = self.reg[SP]
                reg_val = self.ram[stack_addr]
                self.reg[SP] = self.reg[SP] +1
                pc = reg_val
            elif instruction == ADD:
                reg_num = self.ram_read(pc + 1)
                reg_num2 = self.ram_read(pc + 2)
                self.alu("ADD", reg_num, reg_num2)
                pc += 3
            elif instruction == PRA:
                reg_num = self.ram_read(pc + 1)
                print(self.reg[reg_num])
                pc += 2         
            elif instruction == ST:
                reg_num = self.ram_read(pc + 1)
                print(self.reg[reg_num])
                pc += 3     

            elif instruction == JMP:
                reg_num = self.ram_read(pc + 1)
                pc = self.reg[reg_num]  
                     
            elif instruction == CMP:
                reg_num = self.ram_read(pc + 1)
                reg_num2 = self.ram_read(pc + 2)
                self.alu("CMP", reg_num, reg_num2)
                pc += 3

            elif instruction == JEQ:
                if self.flag == 0b00000001: # if equal set flag  true and then
                    reg_num = self.ram_read(pc + 1) # set address stored in the given register
                    pc = self.reg[reg_num] # pc count jump to address that stored in given register
                else:
                    pc += 2
            
            elif instruction == JNE:
                if self.flag != 0b00000001: # if flag e (eqaul) not true then
                    reg_num = self.ram_read(pc + 1) # jump to address stored in the given register
                    pc = self.reg[reg_num] # where pc count jump to
                else: # other wise pc count by 2
                    pc += 2 
                     
                     
            else:
                print(f"unknow instruction {instruction} at address {pc} ")
                sys.exit(1)
