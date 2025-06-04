import os
import re

Instructions = {
    "ADD":   {"opcode": 0x18, "format": [3, 4]},
    "ADDF":  {"opcode": 0x58, "format": [3, 4]},
    "ADDR":  {"opcode": 0x90, "format": [2]},
    "AND":   {"opcode": 0x40, "format": [3, 4]},
    "CLEAR": {"opcode": 0xB4, "format": [2]},
    "COMP":  {"opcode": 0x28, "format": [3, 4]},
    "COMPF": {"opcode": 0x88, "format": [3, 4]},
    "COMPR": {"opcode": 0xA0, "format": [2]},
    "DIV":   {"opcode": 0x24, "format": [3, 4]},
    "DIVF":  {"opcode": 0x64, "format": [3, 4]},
    "DIVR":  {"opcode": 0x9C, "format": [2]},
    "FIX":   {"opcode": 0xC4, "format": [1]},
    "FLOAT": {"opcode": 0xC0, "format": [1]},
    "HIO":   {"opcode": 0xF4, "format": [1]},
    "J":     {"opcode": 0x3C, "format": [3, 4]},
    "JEQ":   {"opcode": 0x30, "format": [3, 4]},
    "JGT":   {"opcode": 0x34, "format": [3, 4]},
    "JLT":   {"opcode": 0x38, "format": [3, 4]},
    "JSUB":  {"opcode": 0x48, "format": [3, 4]},
    "LDA":   {"opcode": 0x00, "format": [3, 4]},
    "LDB":   {"opcode": 0x68, "format": [3, 4]},
    "LDCH":  {"opcode": 0x50, "format": [3, 4]},
    "LDF":   {"opcode": 0x70, "format": [3, 4]},
    "LDL":   {"opcode": 0x08, "format": [3, 4]},
    "LDS":   {"opcode": 0x6C, "format": [3, 4]},
    "LDT":   {"opcode": 0x74, "format": [3, 4]},
    "LDX":   {"opcode": 0x04, "format": [3, 4]},
    "LPS":   {"opcode": 0xD0, "format": [3, 4]},
    "MUL":   {"opcode": 0x20, "format": [3, 4]},
    "MULF":  {"opcode": 0x60, "format": [3, 4]},
    "MULR":  {"opcode": 0x98, "format": [2]},
    "NORM":  {"opcode": 0xC8, "format": [1]},
    "OR":    {"opcode": 0x44, "format": [3, 4]},
    "RD":    {"opcode": 0xD8, "format": [3, 4]},
    "RMO":   {"opcode": 0xAC, "format": [2]},
    "RSUB":  {"opcode": 0x4C, "format": [3, 4]},
    "SHIFTL": {"opcode": 0xA4, "format": [2]},
    "SHIFTR": {"opcode": 0xA8, "format": [2]},
    "SIO":   {"opcode": 0xF0, "format": [1]},
    "SSK":   {"opcode": 0xEC, "format": [3, 4]},
    "STA":   {"opcode": 0x0C, "format": [3, 4]},
    "STB":   {"opcode": 0x78, "format": [3, 4]},
    "STCH":  {"opcode": 0x54, "format": [3, 4]},
    "STF":   {"opcode": 0x80, "format": [3, 4]},
    "STI":   {"opcode": 0xD4, "format": [3, 4]},
    "STL":   {"opcode": 0x14, "format": [3, 4]},
    "STS":   {"opcode": 0x7C, "format": [3, 4]},
    "STSW":  {"opcode": 0xE8, "format": [3, 4]},
    "STT":   {"opcode": 0x84, "format": [3, 4]},
    "STX":   {"opcode": 0x10, "format": [3, 4]},
    "SUB":   {"opcode": 0x1C, "format": [3, 4]},
    "SUBF":  {"opcode": 0x5C, "format": [3, 4]},
    "SUBR":  {"opcode": 0x94, "format": [2]},
    "SVC":   {"opcode": 0xB0, "format": [2]},
    "TD":    {"opcode": 0xE0, "format": [3, 4]},
    "TIO":   {"opcode": 0xF8, "format": [1]},
    "TIX":   {"opcode": 0x2C, "format": [3, 4]},
    "TIXR":  {"opcode": 0xB8, "format": [2]},
    "WD":    {"opcode": 0xDC, "format": [3, 4]},
}
RegisterNumbers = {
    'A' : "0000", 
    'X' : "0001",
    'L' : "0010",
    'B' : "0011",
    'S' : "0100",
    'T' : "0101",
    'PC' : "1000", 
    'SW' : "1001"
}
SYMTable = {

}
BaseAddress = 0x0000

def intermediate_file():
    path = os.path.abspath("testLecture.txt")
    i_lines = []
    with open(path ,"r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('.'):
                continue

            line = line.split(";")[0]
            line = line.split(".")[0]
            line = line.split()
            line = line[1:]

            if len(line) < 3:
                line = "\t".join(line)
                i_lines.append("\t" + line + "\n")
            else:
                line = "\t".join(line)
                i_lines.append(line + "\n")

    with open("intermediate.txt", "w") as i_file:
        for line in i_lines:
            i_file.write(line)             

def loc_counter():
    locc = 0x0000
    modified_line = []
    prev_locc = locc
    labelF=0
    global size

    with open("intermediate.txt", "r") as file:
        for line in file:
            if not line:
                continue
            original_line = line.strip()
            line = line.split()
            if len(line) == 3:
                instruction = line[1]
                labelF=1
            else:
                instruction = line[0]
            instruction = instruction.upper()

            match instruction:
                case "START" | "BASE" | "END":
                    modified_line.append(f"\t\t{original_line}")
                    continue
                case "BYTE":
                    operand = line[-1]
                    if operand.startswith('C'):
                        operand = re.findall(r"C'([A-Za-z]+)'", operand)
                        operand = list(''.join(operand))
                        number_of_char = len(operand)
                        prev_locc = locc
                        locc += number_of_char
                        modified_line.append(f"0x{prev_locc:04X}\t{original_line}")
                    elif operand.startswith('X'):
                        operand = re.findall(r"X'([0-9A-Fa-f]+)'", operand)
                        operand = list(''.join(operand))
                        number_of_hex = int(len(operand) / 2)
                        prev_locc = locc
                        locc += number_of_hex
                        modified_line.append(f"0x{prev_locc:04X}\t{original_line}")
                case "WORD":
                    operand = line[-1]
                    operand = operand.split(",")
                    number_of_int = len(operand)
                    prev_locc = locc
                    locc += number_of_int * 3
                    modified_line.append(f"0x{prev_locc:04X}\t{original_line}")
                case "RESB":
                    operand = line[-1]
                    prev_locc = locc
                    locc += int(operand)
                    modified_line.append(f"0x{prev_locc:04X}\t{original_line}")
                case "RESW":
                    operand = line[-1]
                    prev_locc = locc
                    locc += int(operand) * 3
                    modified_line.append(f"0x{prev_locc:04X}\t{original_line}")
                case _:
                    if instruction.startswith('+'):
                        prev_locc = locc
                        locc += Instructions[instruction.strip("+")]["format"][1]
                        modified_line.append(f"0x{prev_locc:04X}\t{original_line}")
                    else:
                        prev_locc = locc
                        locc += Instructions[instruction]["format"][0]
                        modified_line.append(f"0x{prev_locc:04X}\t{original_line}")
            
            if labelF:
                SYMTable.update({line[0]: prev_locc})
                labelF=0
            size = hex(locc)
    with open("out_pass1.txt", "w") as file:
        for line in modified_line:
            file.write(line + "\n")

def SymTable_file():
    with open("symTable.txt", "w") as file:
        for label, address in SYMTable.items():
            file.write(f"{label.upper()}    {hex(address)[2:].zfill(4).upper()}\n")
        
def pass_1():
    loc_counter()
    SymTable_file()

def check_format(instruction):
    if instruction in Instructions:
        return Instructions[instruction]["format"]
    else:
        return None
    
def check_indexed(operand):
    if ',' in operand:
        return True
    else:
        return False

def opcode_format1(instruction):
    opcode = Instructions[instruction]["opcode"]
    return hex(opcode)[2:].zfill(6).upper()
    
def opcode_format2(instruction, operand):
    opcode = Instructions[instruction]["opcode"]
    registers = operand.split(',')
    
    if len(registers) == 1:
        reg2 = "00"
        reg1 = RegisterNumbers[registers[0].strip()]
    else:
        reg1 = RegisterNumbers[registers[0].strip()]
        reg2 = RegisterNumbers[registers[1].strip()]
    
    return f"{opcode:02X}{int(reg1, 2):01X}{int(reg2, 2):01X}"

def opcode_format3(instruction, operand,pc):
    opcode = Instructions[instruction]["opcode"]
    x,b,p,e = 0,0,0,0
    disp = 0
    flags=0x00

    
    # Check Indexing
    if check_indexed(operand):
        x = 1
        operand = operand.split(',')[0].strip()

    # Immediate/Indirect/Simple
    if operand[0] == '#': #i = 1
        operand = operand[1:]
        opcode += 0x1

        flags = (x << 3) | (b << 2) | (p << 1) | e
        flags = hex(flags)
        if operand.isdigit():
            return f"{opcode:02X}{flags[2:]}{int(operand):03X}"
        elif operand in SYMTable:
            target = SYMTable[operand]
            if -0x800 <= target - pc <= 0x7FF:
                disp = target - pc
                p = 1
            elif BaseAddress is not None and 0x0 <= target - BaseAddress <= 0xFFF:
                disp = target - BaseAddress
                b = 1
            flags = (x << 3) | (b << 2) | (p << 1) | e
            flags = hex(flags)
            return f"{opcode:02X}{flags[2:]}{int(disp):03X}"

    elif operand[0] == '@': #n = 1
        opcode += 0x2
        operand = operand[1:]
    else: #n = 1 i = 1
        opcode += 0x3

    #Base/PC Relative
    if operand in SYMTable:
        target = SYMTable[operand]
        if -0x800 <= target - pc <= 0x7FF:
            disp = target - pc
            p = 1
        elif BaseAddress is not None and 0x0 <= target - BaseAddress <= 0xFFF:
            disp = target - BaseAddress
            b = 1
        else:
            if x:
                return opcode_format4(instruction, operand + ",x")
            else:
                return opcode_format4(instruction, operand)
    
   
        
        flags = (x << 3) | (b << 2) | (p << 1) | e
        flags = hex(flags).upper()
        return f"{opcode:02X}{flags[2:]}{disp & 0xFFF:03X}"
        
def opcode_format4(instruction, operand):
    opcode = Instructions[instruction]["opcode"]
    x,b,p,e = 0,0,0,1

    if check_indexed(operand):
        x = 1
        operand = operand.split(',')[0].strip()

    flags = (x << 3) | (b << 2) | (p << 1) | e
    flags = hex(flags)

    if operand[0] == '#': #i = 1
        operand = operand[1:]
        opcode += 0x1
        if operand.isdigit():
            return f"{opcode:02X}{flags[2:]}{int(operand):05X}"
        else:
            return f"{opcode:02X}{flags[2:]}{SYMTable[operand]:05X}"
    elif operand[0] == '@': #n = 1
        opcode += 0x2
        operand = operand[1:]
    else: #n = 1 i = 1
        opcode += 0x3

    return f"{opcode:02X}{flags[2:]}{SYMTable[operand]:05X}"

def opcode_variables(instruction, operand):
    if instruction == "BYTE":
        if operand.startswith('C'):
            operands = re.findall(r"C'([^']+)'", operand)
            return ','.join(''.join(f"{ord(char):02X}" for char in op) for op in operands)
        elif operand.startswith('X'):
            operands = re.findall(r"X'([0-9A-Fa-f]+)'", operand)
            return ','.join(''.join(op) for op in operands)
    elif instruction == "WORD":
        if ',' in operand: 
            values = operand.split(',')
            return ','.join(f"{int(value):06X}" for value in values)
        else:
            return f"{int(operand):06X}"
    else:
        return None

def opcode_gen():
    with open("out_pass1.txt", "r") as file:
        
        modified_line = [] 
        for line in file:
            opcode = 0x0000

            if not line:
                continue
            original_line = line.strip()
            line = line.split()
            
            if len(line) == 4:
                instruction = line[2]
            elif len(line) == 2: 
                if line[0] == "BASE" or line[0] == "END":
                    instruction = line[0]
                else:
                    instruction = line[1]
            else:
                instruction = line[1]
            instruction = instruction.upper()
            if instruction == "END" or instruction == "START" or instruction == "RESW" or instruction == "RESB":
                modified_line.append(f"{original_line}")
                continue
            elif instruction == "BASE":
                global BaseAddress
                BaseAddress = SYMTable[line[-1]]
                modified_line.append(f"\t\t{original_line}")
                continue
            elif instruction == "BYTE" or instruction == "WORD":
                opcode = opcode_variables(instruction, line[-1])
            elif instruction == "RSUB":
                modified_line.append(f"{original_line}  || F400000")
                continue
            else:
                format = check_format(instruction)
                if instruction.startswith('+'):
                    opcode = opcode_format4(instruction.strip("+"), line[-1])
                elif format == [1]:
                    opcode = opcode_format1(instruction)
                elif format == [2]:
                    opcode = opcode_format2(instruction, line[-1])
                elif format == [3, 4]:
                    pc = original_line.split()[0]
                    pc = int(pc, 16)
                    opcode = opcode_format3(instruction, line[-1],pc+0x03)  
            

            modified_line.append(f"{original_line}  || {opcode}")
        
        with open("out_pass2.txt", "w") as file:
            for line in modified_line:
                file.write(line + "\n")       
            
def HTME():
    H_Record = ""
    T_Record = []
    M_Record = []
    E_Record = ""
    
    with open("out_pass2.txt", "r") as file:
        line = file.readline()
        if not line:
            return
            
        parts = line.split()
        name = parts[0].rstrip()
        start_addr = parts[1][2:].zfill(6)  

        H_Record+= f"H{name.ljust(6, 'X')}{line.split()[2].zfill(6)}{size[2:].zfill(4)}\n"
        E_Record+= f"E{line.split()[2].zfill(6)}\n"

        currT = ""
        currSize = 0
        start_currT = 0
        
        for line in file:
            if not line:
                continue
            line = line.strip()

            if "||" in line:
                line = line.split("||")
                opcode = line[1].strip().replace(",", "")
                address = int(line[0].split()[0], 16)

                # M records 
                if len(opcode) == 8:
                    if '#' in line[0]:
                        operand = line[0].split('#', 1)[1].strip()
                        if operand.isnumeric:
                            continue
                    else:
                        M_Record.append(f"M{address+1:06X}05")

                #T records
                if currT == "":
                    start_currT = address
                    currT = opcode
                else:
                    currSize = address - start_currT 
                    if currSize+len(opcode)/2 > 30:
                        T_Record.append(f"T{start_currT:06X}{currSize:02X}{currT}")
                        currT = opcode
                        start_currT = address
                    else:
                        currT += opcode
            elif  ("RESW" in line or "RESB" in line) and currT != "":
                address = int(line.split()[0], 16)
                currSize = address - start_currT 
                T_Record.append(f"T{start_currT:06X}{currSize:02X}{currT}")
                currT=""

    
        if currT:
            currSize = address - start_currT + int(len(opcode)/2)
            T_Record.append(f"T{start_currT:06X}{currSize:02X}{currT}")

        
        with open("HTME.txt", "w") as obj_file:
            obj_file.write(H_Record)
            for t_record in T_Record:
                obj_file.write(t_record + "\n")
            for m_record in M_Record:
                obj_file.write(m_record + "\n")
            obj_file.write(E_Record)

def pass_2():
    opcode_gen()
    HTME()

if __name__ == "__main__":
    intermediate_file()
    pass_1()
    pass_2()

    
