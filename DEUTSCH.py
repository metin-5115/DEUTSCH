import numpy as np
from qiskit import IBMQ, Aer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, assemble, transpile
from qiskit.visualization import plot_histogram
n=3
dj_circuit = QuantumCircuit(n+1, n)

# Apply H-gates
for qubit in range(n):
    dj_circuit.h(qubit)

# Put qubit in state |->
dj_circuit.x(n)
dj_circuit.h(n)
dj_circuit.draw()

def dj_oracle(case, n):
    # Bu devre n+1 kubite sahip: girdi kubit boyutu,
    # ve bir de cikti kubit
    oracle_qc = QuantumCircuit(n+1)
    
    # Dengeli oracle isteniyor ise:
    if case == "balanced":
        b = np.random.randint(1,2**n)
        # Ikili stringi formatlayalim.
        b_str = format(b, '0'+str(n)+'b')
        
        # Sonra, ilk X kapilarini koyalim. Ikili stringteki her rakam bir
        # kubite denk geldigi için, string 1 ise X kapisi gerekir.
        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                oracle_qc.x(qubit)
        
        # Cikti qubiti hedef olacak sekilde,
        # tum kubitler ile CNOT
        for qubit in range(n):
            oracle_qc.cx(qubit, n)
            
        # Sonra, son X kapilarini koyalim.
        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                oracle_qc.x(qubit)

    # Sabit oracle isteniyor ise:
    if case == "constant":
        # Ilk olarak hangi sabit cikti isteniyor rastgele secelim.
        output = np.random.randint(2)
        
        # Rasgele 1 gelirse, son kubite X uygulayalim.
        if output == 1:
            oracle_qc.x(n)
    
    # Devreyi kapi yapar.
    oracle_gate = oracle_qc.to_gate()
    oracle_gate.name = "Oracle"
    return oracle_gate


dj_circuit.append(dj_oracle("balanced", n), range(n+1))
dj_circuit.draw()


for qubit in range(n):
    dj_circuit.h(qubit)
dj_circuit.draw()

for i in range(n):
    dj_circuit.measure(i, i)
dj_circuit.draw()


aer_sim = Aer.get_backend('aer_simulator')
transpiled_dj_circuit = transpile(dj_circuit, aer_sim)
qobj = assemble(transpiled_dj_circuit)
results = aer_sim.run(qobj).result()
answer = results.get_counts()
plot_histogram(answer)


