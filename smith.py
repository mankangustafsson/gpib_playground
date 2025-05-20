from skrf import Network

ring_slot = Network("s:\\gpib\\rosenberger female load.s1p")
ring_slot.plot_s_smith()
