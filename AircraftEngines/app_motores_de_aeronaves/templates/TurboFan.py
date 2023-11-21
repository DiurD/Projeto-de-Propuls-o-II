import Prop2,re,math
from tabulate import tabulate

class turbofan:

    def __init__(self):
        print("\nINICIANDO TURBOFAN")
        SI = self.sistema_de_medidas()
        medida = "Diâmetro [mm]" if SI else "Diâmetro [in]"
        self.characteristics = {
            #'Engine Part': ["Engine","Intake","Fan","Turbojet intake","HP Turbine","Turbojet Nozzle","Fan Nozzle"],
            'Partes do motor': ["Motor","Admissão","Fan","Admissão do Turbojato","Turbina de Alta","Bocal do Turbojato","Bocal do Fan"],
            medida: [],
            'Diâmetro [m]': [],
            'Área [m²]': [],
            'Área do Fan [m²]': float(0),
            'Bypass ratio (Alpha)': float(1),
        }
        self.preenche_diametros(SI)
        self.preenche_compressores()
        

    def preenche_diametros(self,SI):

        if SI:
            fator_conversao = 0.001
        else:
            fator_conversao = 0.0254

        medidas = "milímetros (m)" if SI else "polegadas (in)"
        medida_original = "Diâmetro [mm]" if SI else "Diâmetro [in]"

        for keys in self.characteristics['Partes do motor']:
            temp = float(input(f"Insira o diâmetro de/do/da {keys.lower()} em {medida_original}: "))
            self.characteristics[medida_original].append(temp)
            temp =temp*fator_conversao
            self.characteristics['Diâmetro [m]'].append(temp)
            self.characteristics['Área [m²]'].append(math.pi*temp**2/4)



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
        
    def altera_diametros(self):
        SI = self.sistema_de_medidas()
        medida = "Diâmetro [mm]" if SI else "Diâmetro [in]"
        if "Diâmetro [mm]" in self.characteristics.keys():
            del self.characteristics["Diâmetro [mm]"]
        elif "Diâmetro [in]" in self.characteristics.keys():
            del self.characteristics["Diâmetro [in]"]
            
        self.characteristics['Diâmetro [m]'] = []
        self.characteristics[medida] = []
        self.characteristics['Área [m²]'] = []
        self.preenche_diametros(SI)

    def preenche_compressores(self):
        self.compressores = {
            'Pi_c / Estágio': 1.0,
            'Pi_f': 1.0,
            'Tau_f': 1.0,
            'Estágios Compressor LP': 1,
            'Estágios Compressor HP': 1,
            'Pi_cL': 1.0,
            'Pi_cH': 1.0,
            'Pi_c': 1.0
        }

        self.compressores['Pi_c / Estágio'] = float(input("\nQual o aumento da pressão total por estágio de compressor (Pi_c / Estágio padrão 1.265)? "))
        self.compressores['Pi_f'] = float(input("\nQual o aumento de pressão total no fan (Pi_f padrão 1.7)? "))
        self.compressores['Estágios Compressor LP'] = int(input("\nQuantos estágios o compressor de baixa possui? "))
        self.compressores['Estágios Compressor HP'] = int(input("\nQuantos estágios o compressor de alta possui? "))
        self.compressores['Pi_cL'] = self.compressores['Pi_c / Estágio']**self.compressores['Estágios Compressor LP']
        self.compressores['Pi_cH'] = self.compressores['Pi_c / Estágio']**self.compressores['Estágios Compressor HP']
        self.compressores['Pi_c'] = self.compressores['Pi_cL']*self.compressores['Pi_cH']