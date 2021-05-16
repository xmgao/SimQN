from qns.quantum.node import QuantumNodeGenerationProtocol, QuantumNodeSwappingProtocol
from qns.schedular import Simulator, Protocol
from qns.quantum.link import QuantumChannel, GenerationProtocal
from qns.quantum import QuantumNode
from qns.quantum import QuantumNetwork
from qns.log import log

class PrintProtocol(Protocol):
    def handle(_self, simulator: Simulator, msg: object, source=None, event = None):
        self = _self.entity
        count = 0
        for e in self.registers:
            if n1 in e.nodes:
                count += 1
        log.debug("Distributed: {} {}", self, count)
        log.exp("Distributed: {} {}", self, count)


s = Simulator(0,10,10000)
log.set_debug(True)
log.install(s)

n1 = QuantumNode(name="n1")
ngp1 = QuantumNodeGenerationProtocol(n1)
nsp1 = QuantumNodeSwappingProtocol(n1)
n1.inject_protocol([ngp1, nsp1])

n2 = QuantumNode(name="n2")
ngp2 = QuantumNodeGenerationProtocol(n2)
nsp2 = QuantumNodeSwappingProtocol(n2)
n2.inject_protocol([ngp2, nsp2])

n3 = QuantumNode(name="n3")
ngp3 = QuantumNodeGenerationProtocol(n3)
nsp3 = QuantumNodeSwappingProtocol(n3)
n3.inject_protocol([ngp3, nsp3])

n4 = QuantumNode(name="n4")
ngp4 = QuantumNodeGenerationProtocol(n4)
nsp4 = QuantumNodeSwappingProtocol(n4)
npp4 = PrintProtocol(n4)
n4.inject_protocol([ngp4, nsp4, npp4])

n2.route = [[n1], [n3,n4]]
n3.route = [[n1,n2], [n4]]

n1.install(s)
n2.install(s)
n3.install(s)
n4.install(s)


c1 = QuantumChannel(nodes = [n1, n2], rate = 20, possible= 0.8, delay = 0.65, name="c1")
cgp1 = GenerationProtocal(c1)
c1.inject_protocol(cgp1)
c1.install(s)

c2 = QuantumChannel(nodes = [n2, n3], rate = 20, possible= 0.8, delay = 0.64, name="n2")
cgp2 = GenerationProtocal(c2)
c2.inject_protocol(cgp2)
c2.install(s)

c3 = QuantumChannel(nodes = [n3, n4], rate = 20, possible= 0.8, delay = 0.64, name="n3")
cgp3 = GenerationProtocal(c3)
c3.inject_protocol(cgp3)
c3.install(s)


s.run()
count = 0
for e in n4.registers:
    if n1 in e.nodes:
        count += 1
print(count)