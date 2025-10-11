# engine.py

class DecisionEngine:
    def __init__(self, strategy="lucro"):
        self.strategy = strategy

    def take_decision(self, consumo, producao):
        media_consumo = sum(consumo) / len(consumo)
        media_producao = sum(producao) / len(producao)

        if self.strategy == "lucro":
            return "Vender excedente" if media_producao > media_consumo else "Comprar energia"
        elif self.strategy == "eficiencia":
            return "Balancear produção e consumo"
        else:
            return "Manter estratégia atual"
