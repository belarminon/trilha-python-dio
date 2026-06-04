class Passaro:
    def voar(self):
        print("O pássaro está voando.")

class Pardal(Passaro):
    def voar(self):
        super().voar()

class Avestruz(Passaro):
    def voar(self):
        print("O avestruz não pode voar.")

# FIXME: exemplo ruim para ganhar tempo, mas é só para mostrar o polimorfismo
class Aviao:
    def voar(self):
        print("O avião está decolando.")

def plano_voo(obj):
    obj.voar()

p1 = Pardal()
p2 = Avestruz()

plano_voo(p1)
plano_voo(p2)

plano_voo(p1)
plano_voo(p2)