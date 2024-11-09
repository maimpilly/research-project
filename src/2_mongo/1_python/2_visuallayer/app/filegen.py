# Define a function to generate file names
import re
def convert_to_p_format(value):
    try:
        num = float(value)
        if num.is_integer():
            return str(int(num))
        else:
            return str(num).replace('.','p')
    except ValueError:
        return value

def generate_file_names(data):
    file_names = []

    for binding in data['results']['bindings']:
        condition = binding['condition']['value']
        gate_length = binding['gateLength']['value']
        voltage_gate_source = binding['voltageGateSource']['value']
        voltage_drain_source = binding['voltageDrainSource']['value']

        if voltage_gate_source == '':
            voltage_gate_source = 'nan'
        elif voltage_gate_source == 'open':
            voltage_gate_source = 'None'
        if voltage_drain_source == '':
            voltage_drain_source = 'nan'
        elif voltage_drain_source == 'open':
            voltage_drain_source = 'None'

        gate_length= convert_to_p_format(gate_length)
        voltage_gate_source = convert_to_p_format(voltage_gate_source)
        voltage_gate_source = convert_to_p_format(voltage_gate_source)

        # Create file names with different suffixes and extensions
        file_name_el = f"el_condition={condition}_lg={gate_length}_vgs={voltage_gate_source}_vds={voltage_drain_source}.tif"
        file_name_tdr = f"tdr_condition={condition}_lg={gate_length}_vgs={voltage_gate_source}_vds={voltage_drain_source}.mat"
        file_name_s11 = f"s11_condition={condition}_lg={gate_length}_vgs={voltage_gate_source}_vds={voltage_drain_source}.s1p"

        file_names.extend([file_name_el, file_name_tdr, file_name_s11])

    #return {'f:name': file_names}
    return {"f_name": "IN ('" + "', '".join(file_names) + "')"}

