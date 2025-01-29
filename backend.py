##############################################################################
# Names: Justin Gajewski, Tyler Hackett
# Pledge: I pledge my honor that I have abided by the Stevens Honor System.
# CS382 Project 2
##############################################################################

# defined instructions and registers with their associated binary values
INSTRUCTIONS = {"ADD":"000", "SUB":"001", "LOAD":"010", "STORE":"011"}
REGISTER_MAP = {"X0":"00", "X1":"01", "X2":"10", "X3":"11"}

# reads through a file and splits the contents of text and data segments
def parse_assembly(file_name):
    textInstructions = []
    dataInstructions = []
    dataBool = False

    with open(file_name, "r") as file:
        for line in file:
            stripped = line.strip()
            if stripped == ".data":
                dataBool = True
                continue
            elif stripped == ".text":
                dataBool = False
                continue

            if dataBool:
                for value in stripped.split():
                    dataInstructions.append(int(value))
            else:
                if stripped:
                    textInstructions.append(stripped.split())
    return textInstructions, dataInstructions

# converts the contents of input file into binary (16 bit instructions w/ 8 bit immediate integer values)
def translate_to_machine_code(textInstructions, dataInstructions):
    machine_code = []
    data_code = []

    for instruction in textInstructions:
        mnemonic = instruction[0]
        ops = instruction[1:]

        mBinary = INSTRUCTIONS[mnemonic]

        binary_ops = []
        for op in ops:
            if op in REGISTER_MAP:
                binary_ops.append(REGISTER_MAP[op])
            else:
                binary_ops.append(format(int(op), '08b'))
        
        fullBinary = mBinary + ''.join(binary_ops)

        fullBinary = fullBinary.ljust(16, '0')[:16]
        machine_code.append(fullBinary)
    
    for num in dataInstructions:
        data_code.append(format(int(num), '08b'))
    
    return machine_code, data_code

# converts binary to hex and puts each hexadecimal in its respective image file
def write_machine_code(text_file, data_file, machine_code, data_code):
    with open(text_file, "w") as file:
        file.write("v3.0 hex words plain\n")
        for instruction in machine_code:
            hexDec = hex(int(instruction, 2))[2:].zfill(4).upper()
            file.write(hexDec + " ")
        file.close()
    with open(data_file, "w") as file:
        file.write("v3.0 hex words plain\n")
        for num in data_code:
            hexDec = hex(int(num, 2))[2:].zfill(4).upper()
            file.write(hexDec + " ")
        file.close()

def main():
    input_file = "assembly.txt"
    text_file = "ram.txt"
    data_file = "data.txt"

    textInstructions, dataInstructions = parse_assembly(input_file)
    machine_code, data_code = translate_to_machine_code(textInstructions, dataInstructions)
    write_machine_code(text_file, data_file, machine_code, data_code)

    print("Success!")

if __name__ == "__main__":
    main()