#On my honor, I have neither given nor received any unauthorized aid on this assignment.
import argparse
import collections
import sys
import subprocess
from collections import deque
parser = argparse.ArgumentParser(description="Process an input file")
parser.add_argument("input_file", help="Path to the input file")
args = parser.parse_args()

def twos_complement_to_decimal(binary_str):
    if binary_str[0] != '1':
        return int(binary_str, 2)
    inverted = ''.join('0' if bit == '1' else '1' for bit in binary_str)
    return -int(bin(int(inverted, 2) + 1)[2:], 2)
    
def binary_to_decimal(binary_str):
    return int(binary_str,2)

def format_after_brk_list(after_brk_list):
    formatted_string = f"Data\n{list(after_brk_list.keys())[0]}:\t"

    values_to_join = list(map(str, list(after_brk_list.values())))

    value_chunks = [values_to_join[i:i+8] for i in range(0, len(values_to_join), 8)]
    formatted_string += '\t'.join(value_chunks[0])

    if len(value_chunks) > 1:
        for chunk in value_chunks[1:]:
            formatted_string += f"\n{list(after_brk_list.keys())[8]}:\t"
            formatted_string += '\t'.join(chunk)

    formatted_string += "\n"

    return formatted_string

category = {'00' : {'00000':'beq',
                    '00001':'bne' ,
                    '00010':'blt' ,
                    '00011' :'sw'},

                '01' : {'00000': 'add',
                    '00001': 'sub',
                    '00010': 'and',
                    '00011' : 'or'},

                '10' : {'00000' : 'addi',
                    '00001' :'andi' ,
                    '00010' : 'ori',
                    '00011' :'sll',
                    '00100' :'sra',
                    '00101' : 'lw'}, 

                '11' : {'00000' : 'jal', '11111' : 'break'}   }

registers = {'x0' : 0,'x1': 0,'x2': 0,'x3':0,'x4':0,'x5':0,'x6':0,'x7':0,
       'x8' : 0,'x9': 0,'x10': 0,'x11':0,'x12':0,'x13':0,'x14':0,'x15':0,
       'x16' : 0,'x17': 0,'x18': 0,'x19':0,'x20':0,'x21':0,'x22':0,'x23':0,
       'x24' : 0,'x25': 0,'x26': 0,'x27':0,'x28':0,'x29':0,'x30':0,'x31':0,}

after_brk_list= {}
counter = 252 

counter_dict = {}

cycle = 0
hypen = "-"*20
flag = False

with open(args.input_file, "r") as input_file:
    for line in input_file:
        sample = line.strip()
        if not flag:
            value = (category[sample[-2:]][sample[-7:-2]])
            if value in [
                'add','addi','andi','ori','or','and','beq','bne','sll','sra','lw','blt',
                'sub','jal','sw',
            ]:
                counter +=4
            elif value == 'break':
                flag = True
                counter +=4
        else:
            counter +=4
            val = str(twos_complement_to_decimal(sample))
            after_brk_list[counter]= val

counter = 252

flag = False

with open(args.input_file, "r") as input_file:
    output1 = "disassembly.txt"
    with open(output1,"w",encoding='utf-8') as output_file:
        for line in input_file:
            sample = line.strip()
            if not flag:
                value = (category[sample[-2:]][sample[-7:-2]])
                if value == 'add':
                    des = sample[-12:-7]
                    rd = f'x{str(binary_to_decimal(des))}'
                    src1 = sample[-19:-15]
                    rs1 = f'x{str(binary_to_decimal(src1))}'
                    src2 = sample[-24:-20]
                    rs2 = f'x{str(binary_to_decimal(src2))}'
                    registers[rd] = registers[rs1] + registers[rs2]
                    counter +=4
                    output_file.write(f"{sample}\t{counter}\t{value} {rd}, {rs1}, {rs2}\n")
                    counter_dict[counter] = (f"{value} {rd}, {rs1}, {rs2}")                    
                elif value == 'or':
                    des = sample[-12:-7]
                    rd = f'x{str(binary_to_decimal(des))}'
                    src1 = sample[-19:-15]
                    rs1 = f'x{str(binary_to_decimal(src1))}'
                    src2 = sample[-24:-20]
                    rs2 = f'x{str(binary_to_decimal(src2))}'
                    registers[rd] = (registers[rs1] | registers[rs2])
                    counter +=4
                    output_file.write(f"{sample}\t{counter}\t{value} {rd}, {rs1}, {rs2}\n")
                    counter_dict[counter] = (f"{value} {rd}, {rs1}, {rs2}") 
                elif value == 'and':
                    des = sample[-12:-7]
                    rd = f'x{str(binary_to_decimal(des))}'
                    src1 = sample[-19:-15]
                    rs1 = f'x{str(binary_to_decimal(src1))}'
                    src2 = sample[-24:-20]
                    rs2 = f'x{str(binary_to_decimal(src2))}'
                    registers[rd] = (registers[rs1] & registers[rs2])
                    counter +=4
                    output_file.write(f"{sample}\t{counter}\t{value} {rd}, {rs1}, {rs2}\n")
                    counter_dict[counter] = (f"{value} {rd}, {rs1}, {rs2}")  
                elif value == 'addi':
                    des = sample[-12:-7]
                    rd = f'x{str(binary_to_decimal(des))}'
                    src1 = sample[-19:-15]
                    rs1 = f'x{str(binary_to_decimal(src1))}'
                    imm_addr = sample[:-20]
                    imm = f'{str(twos_complement_to_decimal(imm_addr))}'
                    registers[rd] = registers[rs1] + int(imm)
                    counter +=4
                    output_file.write(f"{sample}\t{counter}\t{value} {rd}, {rs1}, #{imm}\n")
                    counter_dict[counter] = (f"{value} {rd}, {rs1}, #{imm}")  
                elif value == 'andi':
                    des = sample[-12:-7]
                    rd = f'x{str(binary_to_decimal(des))}'
                    src1 = sample[-19:-15]
                    rs1 = f'x{str(binary_to_decimal(src1))}'
                    imm_addr = sample[:-20]
                    imm = f'{str(twos_complement_to_decimal(imm_addr))}'
                    registers[rd] = (registers[rs1] & int(imm))
                    counter +=4
                    output_file.write(f"{sample}\t{counter}\t{value} {rd}, {rs1}, #{imm}\n")
                    counter_dict[counter] = (f"{value} {rd}, {rs1}, #{imm}") 
                elif value == 'ori':
                    des = sample[-12:-7]
                    rd = f'x{str(binary_to_decimal(des))}'
                    src1 = sample[-19:-15]
                    rs1 = f'x{str(binary_to_decimal(src1))}'
                    imm_addr = sample[:-20]
                    imm = f'{str(twos_complement_to_decimal(imm_addr))}'
                    registers[rd] = (registers[rs1] | int(imm))
                    counter +=4
                    output_file.write(f"{sample}\t{counter}\t{value} {rd}, {rs1}, #{imm}\n")
                    counter_dict[counter] = (f"{value} {rd}, {rs1}, #{imm}")    
                elif value == 'beq':
                    src1 = sample[-19:-15]
                    rs1 = f'x{str(binary_to_decimal(src1))}'
                    src2 = sample[-24:-20]
                    rs2 = f'x{str(binary_to_decimal(src2))}'
                    imm_addr1 = sample[-12:-7]
                    imm_addr2 = sample[:-25]
                    imm = str(twos_complement_to_decimal(imm_addr2 + imm_addr1))
                    counter +=4
                    output_file.write(f"{sample}\t{counter}\t{value} {rs1}, {rs2}, #{imm}\n")
                    counter_dict[counter] = (f"{value} {rs1}, {rs2}, #{imm}")
                elif value == 'bne':
                    src1 = sample[-19:-15]
                    rs1 = f'x{str(binary_to_decimal(src1))}'
                    src2 = sample[-24:-20]
                    rs2 = f'x{str(binary_to_decimal(src2))}'
                    imm_addr1 = sample[-12:-7]
                    imm_addr2 = sample[:-25]
                    imm = str(twos_complement_to_decimal(imm_addr2 + imm_addr1))
                    counter +=4
                    output_file.write(f"{sample}\t{counter}\t{value} {rs1}, {rs2}, #{imm}\n")
                    counter_dict[counter] = (f"{value} {rs1}, {rs2}, #{imm}")
                elif value == 'sll':
                    des = sample[-12:-7]
                    rd = f'x{str(binary_to_decimal(des))}'
                    src1 = sample[-19:-15]
                    rs1 = f'x{str(binary_to_decimal(src1))}'
                    imm_addr = sample[:-20]
                    imm = f'{str(twos_complement_to_decimal(imm_addr))}'
                    counter +=4
                    output_file.write(f"{sample}\t{counter}\t{value} {rd}, {rs1}, #{imm}\n")
                    counter_dict[counter] = (f"{value} {rd}, {rs1}, #{imm}")
                elif value == 'sra':
                    des = sample[-12:-7]
                    rd = f'x{str(binary_to_decimal(des))}'
                    src1 = sample[-19:-15]
                    rs1 = f'x{str(binary_to_decimal(src1))}'
                    imm_addr = sample[:-20]
                    imm = f'{str(twos_complement_to_decimal(imm_addr))}'
                    counter +=4
                    output_file.write(f"{sample}\t{counter}\t{value} {rd}, {rs1}, #{imm}\n")
                    counter_dict[counter] = (f"{value} {rd}, {rs1}, #{imm}")
                elif value == 'lw':
                    des = sample[-12:-7]
                    rd = f'x{str(binary_to_decimal(des))}'
                    src1 = sample[-19:-15]
                    rs1 = f'x{str(binary_to_decimal(src1))}'
                    imm_addr = sample[:-20]
                    imm = str(twos_complement_to_decimal(imm_addr))
                    counter +=4
                    output_file.write(f"{sample}\t{counter}\t{value} {rd}, {imm}({rs1})\n")
                    counter_dict[counter] = (f"{value} {rd}, {imm}({rs1})")
                elif value == 'blt':
                    src1 = sample[-19:-15]
                    rs1 = f'x{str(binary_to_decimal(src1))}'
                    src2 = sample[-24:-20]
                    rs2 = f'x{str(binary_to_decimal(src2))}'
                    imm_addr1 = sample[-12:-7]
                    imm_addr2 = sample[:-25]
                    imm = str(twos_complement_to_decimal(imm_addr2 + imm_addr1))
                    counter +=4
                    output_file.write(f"{sample}\t{counter}\t{value} {rs1}, {rs2}, #{imm}\n")
                    counter_dict[counter] = (f"{value} {rs1}, {rs2}, #{imm}")
                elif value == 'sub':
                    des = sample[-12:-7]
                    rd = f'x{str(binary_to_decimal(des))}'
                    src1 = sample[-19:-15]
                    rs1 = f'x{str(binary_to_decimal(src1))}'
                    src2 = sample[-24:-20]
                    rs2 = f'x{str(binary_to_decimal(src2))}'
                    registers[rd] = registers[rs1] - registers[rs2]
                    counter +=4
                    output_file.write(f"{sample}\t{counter}\t{value} {rd}, {rs1}, {rs2}\n")
                    counter_dict[counter] = (f"{value} {rd}, {rs1}, {rs2}")
                elif value == 'jal':
                    des = sample[-12:-7]
                    rd = f'x{str(binary_to_decimal(des))}'
                    imm_addr = sample[:-12]
                    imm = f'#{str(twos_complement_to_decimal(imm_addr))}'
                    counter +=4
                    output_file.write(f"{sample}\t{counter}\t{value} {rd}, {imm}\n")
                    counter_dict[counter] = (f"{value} {rd}, {imm}")
                elif value == 'sw':
                    src1 = sample[-19:-15]
                    rs1 = f'x{str(binary_to_decimal(src1))}'
                    src2 = sample[-24:-20]
                    rs2 = f'x{str(binary_to_decimal(src2))}'
                    imm_addr1 = sample[-12:-7]
                    imm_addr2 = sample[:-25]
                    imm = str(twos_complement_to_decimal(imm_addr2 + imm_addr1))
                    counter +=4
                    output_file.write(f"{sample}\t{counter}\t{value} {rs1}, {imm}({rs2})\n")
                    counter_dict[counter] = (f"{value} {rs1}, {imm}({rs2})")
                elif value == 'break':
                    flag = True
                    counter +=4
                    output_file.write(f"{sample}\t{counter}\t{value}\n")
                    counter_dict[counter] = (f"{value}")

            else:
                counter +=4
                val = str(twos_complement_to_decimal(sample))
                output_file.write(f"{sample}\t{counter}\t{val}\n")
                counter_dict[counter] = (f"{val}")

counter = 256
cycle = 1
hypen = "-"*20

instructions = []  

for key in counter_dict.values():
    counter_dict.get(key)
    instructions.append(key)


pa_entry_0 = ""
pa_entry_1 = ""

pre_mem_queue = ""
post_mem_queue = ""
pre_alu2_queue = ""
post_alu2_queue = ""
pre_alu3_queue = ""
post_alu3_queue = ""

waiting_queue = ""
executed_queue = ""

pre_issue_queue = collections.deque(maxlen=4)
IF_queue = collections.deque(maxlen=2)
pre_alu1_queue = collections.deque(maxlen=2)

entry_0 = ""
entry_1 = ""
entry_2 = ""
entry_3 = ""

write_back_queue = collections.deque(maxlen=12)

    
def print_state(cycle, file):
    file.write('IF Unit:\n')    
    file.write('\tWaiting:')
    file.write(f' {waiting_queue}\n')
    file.write('\tExecuted:')
    file.write(f' {executed_queue}\n')
    
    file.write('Pre-Issue Queue:\n')
    file.write('\tEntry 0: ')
    file.write(f'{entry_0}\n')
    file.write('\tEntry 1: ')
    file.write(f'{entry_1}\n')
    file.write('\tEntry 2: ')
    file.write(f'{entry_2}\n')
    file.write('\tEntry 3: ')
    file.write(f'{entry_3}\n')

    file.write('Pre-ALU1 Queue:\n')
    file.write('\tEntry 0: ')
    file.write(f'{pa_entry_0}\n')
    file.write('\tEntry 1: ')
    file.write(f'{pa_entry_1}\n')
    
    file.write('Pre-MEM Queue: ')
    file.write(f'{pre_mem_queue}\n')
    
    file.write('Post-MEM Queue: ')
    file.write(f'{post_mem_queue}\n')
    
    file.write('Pre-ALU2 Queue: ')
    file.write(f'{pre_alu2_queue}\n')
    
    file.write('Post-ALU2 Queue: ')
    file.write(f'{post_alu2_queue}\n')
    
    file.write('Pre-ALU3 Queue: ')
    file.write(f'{pre_alu3_queue}\n')
    
    file.write('Post-ALU3 Queue: ')
    file.write(f'{post_alu3_queue}\n\n')

registers = {f'x{i}': 0 for i in range(32)}

registers_busy = {f'x{i}': False for i in range(32)}

counter_val = []
def operations(value,queue,counter):
    if value == "add":
        rd = queue.split()[1].replace(",","")
        rs1 = queue.split()[2].replace(",","")
        rs2 = queue.split()[3].replace("]","")
        registers[rd] = int(registers[rs1]) + int(registers[rs2])
        
    elif value == "or":
        rd = queue.split()[1].rstrip(',')
        rs1 = queue.split()[2].rstrip(',')
        rs2 = queue.split()[3].rstrip(',').replace("]","")
        registers[rd] = (registers[rs1] | registers[rs2])
        

    elif value == "and":
        rd = queue.split()[1].rstrip(',')
        rs1 = queue.split()[2].rstrip(',')
        rs2 = queue.split()[3].rstrip(',').replace("]","")
        registers[rd] = (int(registers[rs1]) & int(registers[rs2]))
        counter = counter + 4

    elif value == "jal":
        rd = queue.split()[1].rstrip(',')
        imm = queue.split()[2].lstrip('#').replace("]","")
        registers[rd] = counter + 8
        counter_val.append(counter + (2*int(imm)))

    elif value == "addi":
        rd = queue.split()[1].replace(",","")
        rs1 = queue.split()[2].replace(",","")
        imm = queue.split()[3].replace("#","").replace("]","")
        registers[rd] = int(registers[rs1]) + int(imm)            

    elif value == "andi":
        rd = queue.split()[1].rstrip(',')
        rs1 = queue.split()[2].rstrip(',')
        imm = queue.split()[3].lstrip('#').replace("]","")
        registers[rd] = (int(registers[rs1]) & int(imm))        

    elif value == "ori":
        rd = queue.split()[1].rstrip(',')
        rs1 = queue.split()[2].rstrip(',')
        imm = queue.split()[3].lstrip('#')
        registers[rd] = (int(registers[rs1]) | int(imm))             
        counter +=4

    elif value == 'beq':
        rs1 = queue.split()[1].rstrip(',')
        rs2 = queue.split()[2].rstrip(',')
        imm = queue.split()[3].lstrip('#').replace("]","")
        if int(registers[rs1]) == int(registers[rs2]):
            counter_val.append(counter + 2*(int(imm)))
        else:
            counter_val.append(counter + 4)

    elif value == 'bne':
        rs1 = queue.split()[1].rstrip(',')
        rs2 = queue.split()[2].rstrip(',')
        imm = queue.split()[3].lstrip('#').replace("]","")

        if int(registers[rs1]) != int(registers[rs2]):  
            counter_val.append(counter + 2*(int(imm)))
        else:
            counter_val.append(counter + 4)

    elif value == 'sll':
        rd = queue.split()[1].rstrip(',')
        rs1 = queue.split()[2].rstrip(',')
        imm = queue.split()[3].lstrip('#').replace(']',"")
        registers[rd] = registers[rs1] << int(imm)

    elif value == 'sra':
        rd = queue.split()[1].rstrip(',')
        rs1 = queue.split()[2].rstrip(',')
        imm = queue.split()[3].lstrip('#').replace("]","")
        registers[rd] = int(registers[rs1]) >> int(imm)
        counter +=4

    elif value == 'lw':
        rd = (queue.split()[1].rstrip(','))
        var_ = queue.split()[2].rstrip('(')
        var_ = var_.replace("(","")
        imm = var_[0:3]
        rs1 = (var_[3:5])
        if (registers[rs1])+ int(imm) in list(counter_dict.keys()):
            registers[rd] = int(counter_dict[(registers[rs1])+ int(imm)])

    elif value == 'blt':
        rs1 = queue.split()[1].rstrip(',')
        rs2 = queue.split()[2].rstrip(',')
        imm = queue.split()[3].lstrip('#').replace("]","")
        if registers[rs1] < registers[rs2]:
            counter_val.append(counter + int(imm)*2)
        else:
            counter_val.append(counter + 4)

    elif value == 'sub':
        rd = queue.split()[1].rstrip(',')
        rs1 = queue.split()[2].rstrip(',')
        rs2 = queue.split()[3].rstrip(',').replace("]","")
        registers[rd] = int(registers[rs1]) - int(registers[rs2])         
       
    elif value == 'sw':
        rd = queue.split()[1].rstrip(',')
        var_ = queue.split()[2].rstrip('(')
        var_ = var_.replace("(","")
        imm = var_[0:3]
        rs1 = (var_[3:5])
        counter_dict[(registers[rs1])+ int(imm)] = registers[rd]
        after_brk_list[(registers[rs1])+ int(imm)] = registers[rd]
        counter +=4

busy_flag = False
reg_update_wait = False
post_mem_wb = False
flag = False
temp_val = ""
pre_exec_queue = ""
prev_post_mem_val = ""
post_mem_Wait = False
post_queue_flag = False
post_mem_flag = False
exec_queue_flag = False
break_flag = False
single_check = False
output2 = "simulation.txt"
with open(output2,"w") as output_file2:
    while counter in list(counter_dict.keys()):
        if flag == False and busy_flag == False:
                if counter_dict[counter].split()[0] in ['add','addi','andi','ori','or','and','sll','sra','lw','sub','sw']:
                    if counter_dict[counter+4].split()[0] in ['jal']:
                        executed_queue = f"[{counter_dict[counter+4]}]"
                        exec_queue_flag = True
                        op_val = executed_queue.split()[0].replace("[","")
                        operations(op_val,executed_queue,counter)
                        registers_busy[executed_queue.split()[1].replace(",","")] = False

                        before_pre_issue_cycle = len(pre_issue_queue)
                        pre_issue_queue.append(counter_dict[counter])
                                        
                        
                        if before_pre_issue_cycle == 0:
                            flag = True
                        
                    elif (4- len(pre_issue_queue)) > 1:
                        before_pre_issue_cycle = len(pre_issue_queue)
                        pre_issue_queue.append(counter_dict[counter])
                        pre_issue_queue.append(counter_dict[counter+4])
                        # registers_busy[counter_dict[counter].split()[1].strip(', ')] = True
                        # registers_busy[counter_dict[counter+4].split()[1].strip(', ')] = True
                            
                        if before_pre_issue_cycle == 0:
                            flag = True
                        
                        counter += 8 

                    elif (4- len(pre_issue_queue)) == 1:
                        pre_issue_queue.append(counter_dict[counter])
                            
                        # if pre_alu1_queue == "" and pre_alu2_queue == "" and pre_alu3_queue == "":
                        single_check = True
                        
                        counter += 4

                elif counter_dict[counter].split()[0] in ['beq','bne','blt','jal']:
                    if counter_dict[counter].split()[0] in ['jal']:
                        executed_queue = f"[{counter_dict[counter]}]"
                        exec_queue_flag = True
                        op_val = executed_queue.split()[0].replace("[","")
                        counter -= 4
                        operations(op_val,executed_queue,counter)
                        
                    else:
                        IF_queue.append(counter_dict[counter])
                        
                        if len(IF_queue) > 0:
                            waiting_queue = f"[{IF_queue[0]}]"
                        else:
                            entry_0 = ""
                        counter += 4    

                elif counter_dict[counter].split()[0] == 'break':
                    executed_queue = f"[{counter_dict[counter]}]"
                    flag = True
                    break_flag = True
                else:
                    counter += 4  

        # Issue Function
        if flag == False:
            if len(pre_issue_queue) > 0 and pre_issue_queue[0].split()[0] in ["lw","sw"] and len(pre_alu1_queue) < 2 and pre_alu3_queue == "" and post_alu3_queue == "":
                before_pre_alu1_cycle = len(pre_alu1_queue)
                pre_alu1_queue.append(f"[{pre_issue_queue[0]}]")
                registers_busy[pre_issue_queue[0].split()[1].strip(',')] = True
                pre_issue_queue.popleft()
                if before_pre_alu1_cycle ==0:
                    flag = True 

            if len(pre_issue_queue) > 0 and pre_issue_queue[0].split()[0] in ["add","sub"] and pre_alu2_queue == "" and not (registers_busy[pre_issue_queue[0].split()[2].replace(",","")] or registers_busy[pre_issue_queue[0].split()[3].replace("]","")]):
                pre_alu2_queue = f"[{pre_issue_queue[0]}]"
                registers_busy[pre_alu2_queue.split()[1].strip(',')] = True
                pre_issue_queue.popleft()
                flag = True

            if len(pre_issue_queue) > 0 and pre_issue_queue[0].split()[0] in ["addi"] and pre_alu2_queue == "" and not (registers_busy[pre_issue_queue[0].split()[2].replace(",","")]):
                pre_alu2_queue = f"[{pre_issue_queue[0]}]"
                registers_busy[pre_alu2_queue.split()[1].strip(',')] = True
                pre_issue_queue.popleft()
                flag = True

            # print(cycle,flag,pre_issue_queue,pre_alu3_queue)
            if len(pre_issue_queue) > 0 and pre_issue_queue[0].split()[0] in ["and", "or"] and pre_alu3_queue == "" and not (registers_busy[pre_issue_queue[0].split()[2].replace(",","")] or registers_busy[pre_issue_queue[0].split()[3].replace("]","")]):
                pre_alu3_queue = f"[{pre_issue_queue[0]}]"
                registers_busy[pre_alu3_queue.split()[1].strip(',')] = True
                pre_issue_queue.popleft()
                flag = True

            if len(pre_issue_queue) > 0 and pre_issue_queue[0].split()[0] in ["andi", "ori", "sra","sll"] and pre_alu3_queue == "" and not (registers_busy[pre_issue_queue[0].split()[2].replace(",","")]):
                pre_alu3_queue = f"[{pre_issue_queue[0]}]"
                registers_busy[pre_alu3_queue.split()[1].strip(',')] = True
                pre_issue_queue.popleft()
                flag = True

        #ALU Function
        if flag == False:
            temp_val = pre_mem_queue
            if len(pre_alu1_queue) > 0:
                val = pre_alu1_queue[0].split()[0].replace("[","")
                if val in ["lw","sw"]:
                    pre_mem_queue = f"{pre_alu1_queue[0]}"
                    pre_alu1_queue.popleft()
                    flag = True  
                    post_mem_flag = True                
                    
            if len(pre_alu2_queue) > 2:
                val = f"{pre_alu2_queue[1]+pre_alu2_queue[2]+pre_alu2_queue[3]}"
                if val in ["add","addi","sub"] and post_alu2_queue == "":
                    post_alu2_queue = pre_alu2_queue
                    pre_alu2_queue = ""
                flag = True 
                post_queue_flag = True
            
            if len(pre_alu3_queue) > 2:
                val = f"{pre_alu3_queue[1]+pre_alu3_queue[2]+pre_alu3_queue[3]}"
                if val in ["and", "andi", "ori", "sll", "sra"] and post_alu3_queue == "":
                    post_alu3_queue = pre_alu3_queue
                    pre_alu3_queue = ""
                flag = True 
                post_queue_flag = True 

            if len(pre_alu3_queue) > 2:
                val = f"{pre_alu3_queue[1]+pre_alu3_queue[2]}"
                if val in ["or"] and post_alu3_queue == "":
                    post_alu3_queue = pre_alu3_queue
                    pre_alu3_queue = ""
                flag = True 
                post_queue_flag = True 

        #POST_MEM function:
        # print(pre_mem_queue,post_mem_queue,cycle)
        # if post_mem_flag == False:
        post_mem_queue = temp_val

        if post_mem_flag == False:
            if len(pre_mem_queue) > 2:
                val = f"{pre_mem_queue[1]+pre_mem_queue[2]}"
                if val in ["lw"]:
                    pre_mem_queue = ""  
                elif val in ["sw"]:
                    pre_mem_queue = ""
                    prev_post_mem_val = post_mem_queue
                    post_mem_queue = ""
                
        #WB Function
                    
        if flag == False and waiting_queue != "" and len(pre_issue_queue) ==0 and waiting_queue.split()[0].replace("[","") != 'jal' and not (registers_busy[waiting_queue.split()[1].replace(",","")] or registers_busy[waiting_queue.split()[2].replace(",","")]):
            # print(waiting_queue.split()[1].replace(",",""),waiting_queue.split()[2].replace(",",""))
            executed_queue = waiting_queue
            waiting_queue = ""
            IF_queue.popleft()
            flag = True
            
        if flag == False and executed_queue != "" and waiting_queue == "":
            pre_exec_queue = executed_queue
            write_back_queue.append(executed_queue)
            op_val = executed_queue.split()[0].replace("[","")
            operations(op_val,executed_queue,counter)
            executed_queue = ""
            busy_flag = False

        if waiting_queue != "":
            busy_flag = True
            flag = True            

        if post_queue_flag == False:
            if prev_post_mem_val != "":
                write_back_queue.append(post_mem_queue)
                op_val = prev_post_mem_val.split()[0].replace("[","")
                operations(op_val,prev_post_mem_val,counter)
                registers_busy[prev_post_mem_val.split()[1].replace(",","")] = False
                temp_val = ""
                flag = True

            if post_alu2_queue != "":
                write_back_queue.append(post_alu2_queue)
                op_val = post_alu2_queue.split()[0].replace("[","")
                operations(op_val,post_alu2_queue,counter)
                registers_busy[post_alu2_queue.split()[1].replace(",","")] = False
                post_alu2_queue = ""        
                flag = True

            if post_alu3_queue != "":
                write_back_queue.append(post_alu3_queue)
                op_val = post_alu3_queue.split()[0].replace("[","")
                operations(op_val,post_alu3_queue,counter)
                registers_busy[post_alu3_queue.split()[1].replace(",","")] = False
                post_alu3_queue = ""
                flag = True

        if flag == True or single_check == True:
            entry_0 = f"[{pre_issue_queue[0]}]" if len(pre_issue_queue) > 0 else ""
            entry_1 = f"[{pre_issue_queue[1]}]" if len(pre_issue_queue) > 1 else ""
            entry_2 = f"[{pre_issue_queue[2]}]" if len(pre_issue_queue) > 2 else ""
            entry_3 = f"[{pre_issue_queue[3]}]" if len(pre_issue_queue) > 3 else ""
            pa_entry_0 = f"{pre_alu1_queue[0]}" if len(pre_alu1_queue) > 0 else ""
            pa_entry_1 = f"{pre_alu1_queue[1]}" if len(pre_alu1_queue) > 1 else ""
            output_file2.write(f"{hypen}\nCycle {cycle}:\n\n")
            print_state(cycle,output_file2)
            output_file2.write(f"Registers\n"
            f"x00:\t{registers['x0']}\t{registers['x1']}\t{registers['x2']}\t{registers['x3']}\t{registers['x4']}\t{registers['x5']}\t{registers['x6']}\t{registers['x7']}\n"
            f"x08:\t{registers['x8']}\t{registers['x9']}\t{registers['x10']}\t{registers['x11']}\t{registers['x12']}\t{registers['x13']}\t{registers['x14']}\t{registers['x15']}\n"
            f"x16:\t{registers['x16']}\t{registers['x17']}\t{registers['x18']}\t{registers['x19']}\t{registers['x20']}\t{registers['x21']}\t{registers['x22']}\t{registers['x23']}\n"
            f"x24:\t{registers['x24']}\t{registers['x25']}\t{registers['x26']}\t{registers['x27']}\t{registers['x28']}\t{registers['x29']}\t{registers['x30']}\t{registers['x31']}\n"
            f"{format_after_brk_list(after_brk_list)}")
            cycle += 1
            
        flag = False
        post_queue_flag = False
        post_mem_flag = False
        post_mem_Wait = False
        post_mem_wb = False
        reg_update_wait = False
        prev_post_mem_val = post_mem_queue
        exec_queue_flag = False
        single_check = False

        if break_flag:
            break

        if len(executed_queue) > 1:
            if executed_queue.split()[0].replace("[","") == 'jal':
                registers_busy[executed_queue.split()[1].replace(",","")] = False
                executed_queue = ""
                counter = counter_val[0] + 4
                counter_val.pop()
            elif executed_queue.split()[0].replace("[","") == 'break':
                cycle = 'break'
                break
        if len(pre_exec_queue) > 1:    
            if pre_exec_queue.split()[0].replace("[","") in ['blt','bne','beq'] and len(counter_val)>0:
                registers_busy[pre_exec_queue.split()[1].replace(",","")] = False
                pre_exec_queue = ""
                counter = counter_val[0]
                counter -= 4
                counter_val.pop()