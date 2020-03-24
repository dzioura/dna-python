from SequenceDbClass import SequenceDbClass


dbClass = SequenceDbClass()

exit = False

while(not exit):
    print("""
        1: GET
        2: INSERT
        3: FIND
        Anything else EXIT
    """)
    val = raw_input("Input please:")
    if val == '1':
        sequence_id = raw_input("Input sequence_id: ")
        try:
            print(dbClass.get(int(sequence_id)))
        except ValueError as ve:
            print(ve)
    elif val == '2':
        sequence = raw_input("Input sequence: ")
        try:
            print(dbClass.insert(sequence.upper()))
        except ValueError as ve:
            print(ve)
    elif val == '3':
        sample = raw_input("Input sample: ")
        print(dbClass.find(sample.upper()))
    else:
        exit = True
        print('Exit')