from qiskit import QuantumProgram, QISKitError #, RegisterSizeError


def make_noise_qbit_pair(qc, qbit0, qbit1, delta):
    qc.crz(2 * delta, qbit0, qbit1)
    qc.cu1(-delta, qbit0, qbit1)

    qc.crz(2 * delta, qbit1, qbit0)
    qc.cu1(-delta, qbit1, qbit0)


def make_noise(qc, qr, delta):
    for i in range(0, len(qr) - 1):
        make_noise_qbit_pair(qc, qr[i], qr[i + 1], delta)


def add_xor(qc, qr, args, res, delta):
    for qbit in args:
        qc.cx(qbit, res)
        make_noise(qc, qr, delta)


def add_w(qc, qr, args, delta):
    for qbit in args:
        qc.h(qbit)
    make_noise(qc, qr, delta)


def create_circut(program, args_count, delta):
    # Creating Registers create your first Quantum Register called "qr" with 2 qubits
    qr = program.create_quantum_register("qr", args_count + 1)
    # create your first Classical Register called "cr" with 2 bits
    cr = program.create_classical_register("cr", args_count + 1)
    # Creating Circuits create your first Quantum Circuit called "qc" involving your Quantum Register "qr"
    # and your Classical Register "cr"
    qc = Q_program.create_circuit("xor", [qr], [cr])

    add_w(qc, qr, [qr[i] for i in range(0, args_count + 1)], delta)
    add_xor(qc, qr, [qr[i] for i in range(0, args_count)], qr[args_count], delta)
    add_w(qc, qr, [qr[i] for i in range(0, args_count + 1)], delta)
    qc.measure(qr, cr)

    result = Q_program.execute(["xor"], backend='local_qasm_simulator', shots=1024)

    # Show the results
    print(result)
    print(result.get_data("xor"))


def work(program, args_count, delta, repeats_count):
    for i in range(0, repeats_count):
        print("Delta", delta, "repeat", i + 1, "of", repeats_count)
        create_circut(program, args_count, delta)

if __name__ == '__main__':
    # Creating Programs create your first QuantumProgram object instance.
    Q_program = QuantumProgram()

    #try:
    for delta in [0, 0.1, 0.01, 0.001]:
        work(Q_program, 6, delta, 3)
    #except QISKitError as ex:
    #  print('There was an error in the circuit!. Error = {}'.format(ex))
    #except RegisterSizeError as ex:
    #  print('Error in the number of registers!. Error = {}'.format(ex))

