import Prop2,re,math
from tabulate import tabulate

class turbofan:

    def __init__(self):
        print("\nINICIANDO TURBOFAN")
        if self.sistema_de_medidas():
            fator_conversao = 0.001
        else:
            fator_conversao = 0.0254
        
        

    


    def sistema_de_medidas(self):
        while 'resp' not in locals():
            text = input("\n Deseja inserir os dados no padrão internacional (SI)? ")
            if re.search('(?i)^sim|^s|^1',text):
                resp= True
                print("Insira as medidas a seguir utilizando o sistema métrico, em milimetros (mm): ")
            elif re.search('(?i)^não|^n|^nao|^2',text):
                resp = False
                print("Insira as medidas a seguir utilizando o sistema imperial, em polegadas (inch): ")
            else:
                print("Digite uma opção válida!\n")
            return resp
        
    def recebe_diamtros(self):
        