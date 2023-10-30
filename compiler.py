import sys
import os

instructions_file_path = sys.argv[1]
compiled_file_path = sys.argv[2]

if (os.path.exists(compiled_file_path)):
    os.remove(compiled_file_path)

instructions_file = open(instructions_file_path, 'r')
compiled_file = open(compiled_file_path, 'a')

empty_nibble = '0000'

op_codes = {
    'arithmetic': {
        'g6_addscal': '0000'
    },
        'arithmetic_vectorial': {
        'g6_add': '0001',
        'g6_sub': '0010',
        'g6_exp': '0011',
        'g6_mul': '0100',
        'g6_cmp': '0101'
    },
    'mov': {
        'g6_movi': '0110',
        'g6_movr': '0111'
    },
    'vectorial': {
        'g6_idx': '1000',
        'g6_append': '1001'
    },
    'branch': {
        'g6_beq': '1010',
        'g6_b': '1011'
    },
    'control': {
        'g6_ldr': '1100',
        'g6_str': '1101'
    }
}
# registros vectoriales
registers = {
    'r0': '0000',
    'r1': '0001',
    'r2': '0010',
    'r3': '0011',
    'r4': '0100',
    'r5': '0101',
    'r6': '0110',
    'r7': '0111',
    'r8': '1000',
    'r9': '1001',
    'r10': '1010',
    'r11': '1011',
}


def to_binary_string(number, width):
    if (number < 0):
        return f'{number % (1 << width):0{width}b}'
    else:
        return f'{number:0{width}b}'


def split_nibbles(binary_string):
    result = []
    for i in range(int(len(binary_string)/4)):
        result.append(f'{binary_string[i*4:(i+1)*4]}')
    return result


def get_op_code(op_code_key):
    for inst_type in op_codes:
        if op_code_key in op_codes[inst_type]:
            op_code = op_codes[inst_type][op_code_key]
            return inst_type, op_code

    raise Exception(f'Error: invalid operation "{op_code_key}"')


def get_register_operand(operand):
    try:
        return registers[operand]
    except KeyError:
        raise Exception(f'Error: invalid operand "{operand}"')


def get_immediate_operand(operand, width):
    try:
        int_operand = int(operand.replace('#0x', ''), 16)
        binary_operand = to_binary_string(int_operand, width)

        if (width % 4 != 0):
            raise Exception(
                f'Error: immediate operand width must be a multiple of 4. Got {width}.')
        if (int_operand > 2**width - 1):
            max_hex_value = f'{(2**width - 1):x}'
            raise Exception(
                f'Error: immediate operand "{operand}" is too large. Max value is {max_hex_value}.')

        return split_nibbles(binary_operand)
    except Exception as error:
        raise Exception(str(error))


def arith_scalar_instruction(op_code_key, op_code, operands):
    if (op_code_key == 'g6_cmp'):
        operand_1 = get_register_operand(operands[0])
        operand_2 = get_register_operand(operands[1])
        return [op_code, operand_1, operand_2, empty_nibble]
    else:
        operand_1 = get_register_operand(operands[0])
        operand_2 = get_register_operand(operands[1])
        operand_3 = get_register_operand(operands[2])
        return [op_code, operand_1, operand_2, operand_3]


def mov_instruction(op_code_key, op_code, operands):
    if (op_code_key == 'g6_movi'):
        operand_1 = get_register_operand(operands[0])
        operand_2_nibbles = get_immediate_operand(operands[1], 8)
        return [op_code, operand_1, operand_2_nibbles[0], operand_2_nibbles[1]]
    else:
        operand_1 = get_register_operand(operands[0])
        operand_2 = get_register_operand(operands[1])
        return [op_code, operand_1, operand_2, empty_nibble]


def branch_instruction(op_code, operands, current_pc, labels):
    for label in labels:
        if (label['label_name'] == operands[0]):
            label_pc = label['pc']
            branch_pc = label_pc - current_pc

            branch_operand = to_binary_string(branch_pc, 12)
            branch_nibbles = split_nibbles(branch_operand)

            return [op_code, branch_nibbles[0], branch_nibbles[1], branch_nibbles[2]]

    raise Exception(
        f'Error: label "{operands[0]}" not found in program.')


def memory_instruction(op_code, operands):
    operand_1 = get_register_operand(operands[0])
    operand_2 = get_register_operand(operands[1])
    return [op_code, operand_1, operand_2, empty_nibble]


def decode_instruction(op_code_key, operands, current_pc, labels):
    try:
        inst_type, op_code = get_op_code(op_code_key)

        if (inst_type == 'arithmetic'):
            return arith_logic_instruction(op_code_key, op_code, operands)
        elif (inst_type == 'arithmetic_vectorial'):
            return arith_logic_instruction(op_code_key, op_code, operands)
        elif (inst_type == 'mov'):
            return mov_instruction(op_code_key, op_code, operands)
        elif (inst_type == 'branch'):
            return branch_instruction(op_code, operands, current_pc, labels)
        elif (inst_type == 'control'):
            return memory_instruction(op_code, operands)
    except Exception as error:
        raise Exception(str(error))


instruction_memory_size = 400
pc = 0
labels = []
instructions = []
for instruction in instructions_file:
    instruction = instruction.strip().lower()

    if (instruction == '' or instruction[0] == ';'):
        continue
    elif (instruction[-1] == ':'):
        label = {'label_name': instruction[:-1], 'pc': pc}
        labels.append(label)
        continue

    instructions.append(instruction)
    pc += 4

pc = 0
try:
    for instruction in instructions:
        instruction = instruction.split(' ', 1)

        op_code_key = instruction[0]
        operands = instruction[1].replace(' ', '').split(',')

        instruction_nibbles = decode_instruction(
            op_code_key, operands, pc, labels)

        print(f'PC: {pc}')
        print(instruction)
        print(instruction_nibbles)
        print('-------------------------------------')

        for nibble in instruction_nibbles:
            compiled_file.write(f'{nibble}\n')
            pc += 1

    while pc < instruction_memory_size:
        compiled_file.write(f'{empty_nibble}\n')
        pc += 1

except Exception as error:
    print(str(error))
    os.remove(compiled_file_path)
    sys.exit(1)
