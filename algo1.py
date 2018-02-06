from qiskit import QuantumProgram, QISKitError #, RegisterSizeError
import json

class QuantumCircuitWithPositions:
    def __init__(self, qc, qr, count, delta):
        self.qc = qc
        self.qr = qr
        self.count = count
        self.positions = [0] * len(qr)
        self.delta = delta

    def make_noise_qbit_pair(self, qbit0, qbit1):
        self.qc.crz(2 * self.delta, self.qr[qbit0], self.qr[qbit1])
        self.qc.cu1(-self.delta, self.qr[qbit0], self.qr[qbit1])

        self.qc.crz(2 * self.delta, self.qr[qbit1], self.qr[qbit0])
        self.qc.cu1(-self.delta, self.qr[qbit1], self.qr[qbit0])

    def make_noise(self, count_steps):
        for step in range(0, count_steps):
            for i in range(0, len(self.qr) - 1):
                self.make_noise_qbit_pair(i, i + 1)

    def move_neighbor_qbits(self, i):
        dist = self.count - self.positions[i] - 1 + self.positions[i + 1]
        self.positions[i] = self.count - 1
        self.positions[i + 1] = 0
        return dist

    def count_swaps_for_pair_operation(self, i, j):
        if i > j:
            return self.count_swaps_for_pair_operation(j, i)

        if i == j:
            return 0

        dist = 0

        for ps in range(i, j):
            dist += self.move_neighbor_qbits(ps)

        for ps in range(j, i, -1):
            dist += self.move_neighbor_qbits(ps - 1)

        return dist + 2 * (j - i - 1)

    def h(self, qbit):
        self.qc.h(self.qr[qbit])
        return 1

    def w(self, qbits):
        count = 0
        for qbit in qbits:
            count = max(count, self.h(qbit))

        return count

    def cx(self, qbit, res):
        count = self.count_swaps_for_pair_operation(qbit, res) + 1
        self.qc.cx(self.qr[qbit], self.qr[res])
        return count


def add_xor(qcwp, args, res):
    for qbit in args:
        count = qcwp.cx(qbit, res)
        qcwp.make_noise(count)


def add_w(qcwp, args):
    count = qcwp.w(args)
    qcwp.make_noise(count)


def create_circut(program, args_count, count, delta, shots):
    # Creating Registers create your first Quantum Register called "qr" with 2 qubits
    qr = program.create_quantum_register("qr", args_count + 1)
    # create your first Classical Register called "cr" with 2 bits
    cr = program.create_classical_register("cr", args_count + 1)
    # Creating Circuits create your first Quantum Circuit called "qc" involving your Quantum Register "qr"
    # and your Classical Register "cr"
    qc = Q_program.create_circuit("xor", [qr], [cr])
    qcwp = QuantumCircuitWithPositions(qc, qr, count, delta)

    add_w(qcwp, list(range(0, args_count + 1)))
    add_xor(qcwp, list(range(0, args_count)), args_count)
    add_w(qcwp, list(range(0, args_count + 1)))
    qc.measure(qr, cr)

    result = Q_program.execute(["xor"], backend='local_qasm_simulator', shots=shots)

    return result


def work(program, args_count, count, delta, shots):
    print("Delta", delta, "shots", shots)
    result = create_circut(program, args_count, count, delta, shots)

    # Show the results
    print(result)
    print(result.get_data("xor"))

    return result

if __name__ == '__main__':
    # Creating Programs create your first QuantumProgram object instance.
    Q_program = QuantumProgram()

    file_name = 'log.txt'
    measures = []

    qbits = 6
    shots = 1024
    delta_base = 0.1

    #try:
    for dist in range(5, 10):
        delta = delta_base / (dist ** 3)
        stat = {
            'qbits': qbits,
            'shots': shots,
            'dist': dist,
            'delta': delta
        }
        res = work(Q_program, qbits, dist, delta, shots)
        stat['counts'] = res.get_data("xor")['counts']
        measures.append(stat)
        with open(file_name, 'w') as f:
            f.write(json.dumps(measures, indent=4, separators=(',', ': ')))

    #except QISKitError as ex:
    #  print('There was an error in the circuit!. Error = {}'.format(ex))
    #except RegisterSizeError as ex:
    #  print('Error in the number of registers!. Error = {}'.format(ex))




