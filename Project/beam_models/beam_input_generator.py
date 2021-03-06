def beam_input_generator(element_type, element_number, beam_size):
    """"
    Beam model input file generator for FEMSS4 project
    Alasdair Gray, S1208454
    November 2016
    This function takes 3 input parameters:
    element type: either 'B21', 'B22' or 'B23'
    element number: The number of elements along the beam
    beam size: either 'thin' or 'thick'
    The function then creates a subfolder in the directory it is being run from and writes an appropriate input file
    with the same name to the subfolder, the function outputs the filename as a string.
    """
    # First, define the element properties based on the chosen element type
    if element_type in ['B21', 'B23']:
        node_per_el = 2
        el_def = '1, 2'
    else:
        node_per_el = 3
        el_def = '1, 2, 3'
    # Define properties based on beam size
    if beam_size == 'thick':
        depth = 1.0
        load = -100000
    elif beam_size == 'thin':
        depth = 0.2
        load = -10000
    # Calculate the number of nodes required along the beam
    total_nodes = str(element_number*(node_per_el-1)+1)
    import inspect, os
    filename = element_type + '_' + beam_size + '_' + str(element_number) + 'EL'
    Parent = os.path.dirname(os.path.realpath(__file__)) # Get the location the function is being run in
    Child = Parent + '/' + filename # Create parameter specific subfolder name
    if not os.path.exists(Child): # Create subfolder if it doesn't already exist
        os.makedirs(Child)
    os.chdir(Child)
    output = open(filename+'.inp', 'w') # Define the inp file to write to
    template = """
    *******************************************************************
    ** FEMSS4 Project                                                **
    ** Alasdair Gray, S1208454                                       **
    ** Beam model input file generated by my wonderful python script **
    *******************************************************************
    *HEADING
    5m LONG SIMPLY SUPPORTED %(beam_size)s BEAM WITH %(load)s kN/m DISTRIBUTED LOAD, %(element_number)s ELEMENT
    %(element_type)s MESH
    ******************************
    *NODE
    ** DEFINE LOCATION OF END NODES
    1, 0.0, 0.0
    %(total_nodes)s, 5.0, 0.0
    ******************************
    *NGEN, NSET=NALL
    ** GENERATE NODES ALONG LENGTH AND DEFINE NODE SET 'NALL'
    1, %(total_nodes)s, 1
    ******************************
    **DEFINE THE FIRST 'MASTER ELEMENT' NUMBER 1 AS A %(element_type)s
    *ELEMENT, TYPE=%(element_type)s
    1, %(el_def)s
    ******************************
    ** GENERATE THE REST OF THE ELEMENTS BY COPYING ELEMENT 1, MAKE %(element_number)s ELEMENTS, ELEMENT NUMBER
    ** INCREMENT OF 1 AND NODE NUMBER INCREMENT OF %(node_shift)s, 1 ROW, ASSIGN TO ELSET 'EALL'
    *ELGEN, ELSET=EALL
    1,%(element_number)s,%(node_shift)s,1,1,1,1
    ******************************
    ** DEFINE MATERIAL CALLED 'STEEL'
    *MATERIAL,NAME=STEEL
    ******************************
    ** DEFINE ELASTIC MATERIAL PROPERTIES, E = 200*10^9 AND POISSON'S RATIO 0
    *ELASTIC
    200E9, 0.3
    ******************************
    ** DEFINE THE BEAM SECTION, ASSIGN IT TO THE ELEMENT SET 'EALL', ASSIGN IT WITH THE 'STEEL' MATERIAL AND DEFINE A
    ** 0.2 M THICK BY (depth)s M DEEP BEAM
    *BEAM SECTION, ELSET = EALL, MATERIAL = STEEL, SECTION = RECT
    0.2, %(depth)s
    ******************************
    **ASK FOR HISTORY AND MODEL DATA TO BE INCLUDED IN RESULTS FILE
    *PREPRINT, ECHO=YES, MODEL=YES, HISTORY=YES
    ******************************
    ** BEGIN LINEAR STEP
    *STEP, PERTURBATION
    ******************************
    ** DEFINE STEP AS STATIC
    *STATIC
    ******************************
    ** DEFINE FIXED BOUNDARY AT NODE 1 LOCKED IN X AND Y DIRECTION AND AT NODE %(total_nodes)s LOCKED IN Y DIRECTION
    *BOUNDARY
    1, 1, 2
    %(total_nodes)s, 2, 2
    ******************************
    ** DEFINE DISTRIBUTED LOAD OF %(load)s KN/M IN Y DIRECTION ON ELSET 'EALL'
    *DLOAD
    EALL, PY, %(load)s
    ******************************
    ** ASK ABAQUS TO PRINT COORDINATE, STRESS AND STRAIN FOR EACH ELEMENT (AT INTEGRATION POINTS INSIDE CELLS)
    *EL PRINT
    COORD
    S
    E
    ******************************
    ** ASK ABAQUS TO PRINT STRESS VALUES AT NODES
    *EL PRINT, POSITION=AVERAGED AT NODES
    S
    ******************************
    ** ASK ABAQUS TO PRINT FORCES AND DISPLACEMENTS AT NODES
    *NODE PRINT
    U
    RF
    ******************************
    ** END THE STEP
    *END STEP """
    # Now define the parameter based strings which will be inserted into the template string
    context = {
    "total_nodes":total_nodes,
    "element_type":element_type,
    "el_def":el_def,
    "element_number": str(element_number),
    "node_shift" : str(node_per_el-1),
    "depth" : str(depth),
    "load" : str(load),
    "beam_size" : beam_size
    }
    # Fill the template blanks with the parameter based strings and write to the input file
    output.write(template % context)
    output.close() # Close the input file
    return filename # Return the parameter specific filename to the caller

if __name__ == "__main__":
    beam_input_generator('B22', 2, 'thin')
