"""
Aluno: Matheus José Felipe Rosa
Docente: Helder Oliveira
Matéria: Design e Aplicações de Engenharia de Software
Data: 07/08/2023
Descrição: Fazer um programa que calcula o salário líquido de um trabalhador a partir do salário bruto, descontos legais
descontos opcionais, vale-trasporte e dependentes.
"""
import re

# Limites de Faixas do INSS 08/2023
INSS_FAIXA1 = 1320
INSS_FAIXA2 = 2571.29
INSS_FAIXA3 = 3856.94
INSS_FAIXA4 = 7507.49
# Limites de Faixas do IRRF 08/2023
IRRF_FAIXA1 = 2112
IRRF_FAIXA2 = 2826.65
IRRF_FAIXA3 = 3751.05
IRRF_FAIXA4 = 4664.68
# Valor da dedução por dependente 08/2023
VALOR_DEPENDENTE = 189.59


def main():
    def verificar_input(input_string, object_type, mostrar=0):
        """
        A função trabalha com três flags, duas numéricas: float e int e uma não numérica: str
        Para as flags numéricas, verifica se há caracteres não numéricos (exceto "." e ","). Se houver, por regex seu
         valor será modificado para conter apenas números. Se a flag for não numérica, verifica se o usuário aceitou uma
         condição a partir da primeira letra da string.
        :param input_string: String que será utilizada como frase para o input
        :param object_type: float, int e str. Utiliza o objeto como verificador do que será realizado pela função.
        :param mostrar: Opção de debug, por padrão zero, qualquer valor diferente implicará no resultado sendo mostrado
        no console.
        :return: Retorna a string corrigida
        :raises ValueError: Se houver alguma parte da string que não pode ser convertida, levantará uma exceção.
        """
        if object_type == int or object_type == float:
            # Repete até que o try seja concluído sem exceções
            while True:
                try:
                    # Replace por regex. A regex [^.|,\d] marca qualquer caractere EXCETO: ".", "," e números
                    resultado = object_type(re.sub(r'[^.|,\d]', '', input(input_string)))
                except ValueError as e:
                    print(f'{e}\nHouve um erro de digitação, atente-se a números inteiros e não inteiros.')
                else:
                    # Debug
                    if mostrar != 0:
                        print(resultado)
                    return resultado
        # Verifica aceitação/rejeição do usuário para inputs não numéricos
        elif object_type == str:
            # Repete até que o try seja concluído sem exceções
            while True:
                try:
                    # Replace por regex. A regex [^a-zA-Z] marca qualquer caractere EXCETO letras de a até z
                    resultado = re.sub(r'[^a-zA-Z]', '', input(input_string)).lower()
                except TypeError as e:
                    print(f'{e}\nVerifique se não há erros na sua resposta e tente novamente.')
                else:
                    try:
                        # Se a primeira letra for "s", encara-se a resposta como sim e retorna True, senão, False
                        if resultado[0] == 's':
                            return True
                    except IndexError as e:
                        print(f'{e}\nUtilize apenas "Sim" ou "Não" para responder.')
                    else:
                        return False

    salario_bruto = verificar_input('Digite o salário bruto: R$', object_type=float)

    def calcular_inss(sb):
        """
        Calcula o valor de desconto do INSS que incidirá sobre o salário bruto.
        Data base dos valores utilizada nos cálculos 08/2023
        :param sb: Salário bruto que será usado como base de comparação para as faixas de valores do INSS.
        :return: Retorna em float o valor de desconto do INSS proporcional a faixa em que o salário bruto se encaixa.
        """
        # Primeira faixa do INSS
        if sb <= INSS_FAIXA1:
            return INSS_FAIXA1 * 0.075
        # Segunda faixa do INSS
        elif sb <= INSS_FAIXA2:
            return (sb - INSS_FAIXA1+0.01) * 0.09 + calcular_inss(INSS_FAIXA1)
        # Terceira faixa do INSS
        elif sb <= INSS_FAIXA3:
            return (sb - INSS_FAIXA2+0.01) * 0.12 + calcular_inss(INSS_FAIXA2)
            # Quarta faixa do INSS
        elif sb <= INSS_FAIXA4:
            return (sb - INSS_FAIXA3+0.01) * 0.14 + calcular_inss(INSS_FAIXA3)
            # Teto INSS
        return (INSS_FAIXA4 - INSS_FAIXA3+0.01) * 0.14 + calcular_inss(INSS_FAIXA3)

    def calcular_irrf(sd):
        """
        Calcula o valor de desconto do INSS que incidirá sobre o salário bruto.
        Data base dos valores utilizada nos cálculos 08/2023
        :param sd: Salário descontado, resultado do cálculo do INSS que será usado como base de comparação para as
         faixas de valores do IRRF.
        :return: Retorna em float o valor de desconto do IRRF proporcional a faixa em que o salário bruto se encaixa.
        """
        # Primeira faixa do IRRF (ISENTA)
        if sd <= IRRF_FAIXA1:
            return 0
        # Segunda faixa do IRRF
        elif sd <= IRRF_FAIXA2:
            return (sd - IRRF_FAIXA1+0.01) * 0.075
        # Terceira faixa do IRRF
        elif sd <= IRRF_FAIXA3:
            return (sd - IRRF_FAIXA2+0.01) * 0.15 + calcular_irrf(IRRF_FAIXA2)
        # Quarta faixa do IRRF
        elif sd <= IRRF_FAIXA4:
            return (sd - IRRF_FAIXA3+0.01) * 0.225 + calcular_irrf(IRRF_FAIXA3)
        # Quinta faixa do IRRF
        return (sd - IRRF_FAIXA4) * 0.275 + calcular_irrf(IRRF_FAIXA4)

    def calcular_vt():
        """
        Calcula o valor do vale-transporte, se houver.
        O vale-transporte é calculado através do salário bruto. Se o valor do vale-transporte superar 6% do salário
         bruto, o funcionário paga os 6% do vale-transporte e a empresa arca com o resto do valor. Caso contrário
        o funcionário acará com qualquer valor abaixo de 6%
        O valor necessário para o transporte é apenas a quantidade diária de passagens utilizadas multiplicada pelos
        dias úteis que serão trabalhados no mês e pelo valor da passagem do transporte.
        :return: Retorna em float o valor do vale-transporte.
        """
        if verificar_input('Possui vale-transporte? (Sim/Não)\nResposta: ', object_type=str):
            dias_uteis = verificar_input('Quantos dias úteis há no mês? ', object_type=int)
            qtd_passagem_dia = verificar_input('Quantas passagens por dia? ', object_type=int)
            valor_mensal = qtd_passagem_dia * dias_uteis * verificar_input('Valor da passagem: R$', object_type=float)
            if valor_mensal > (salario_bruto * 0.06):
                return salario_bruto * 0.06
            return valor_mensal
        return 0

    def calcular_dependentes():
        """
        Calcula qual o valor a ser descontado a partir da quantidade de dependentes.
        :return: Retorna em float o valor total a ser descontado pelos dependentes.
        """
        qtd_dependentes = verificar_input('Qual o número de dependentes? ', object_type=int)
        return VALOR_DEPENDENTE * qtd_dependentes

    def calcular_descontos():
        """
        Junção de todos os cálculos anteriores para obter o salário líquido.
        :return: Retorna em float o valor do salário líquido.
        """
        valor_inss = calcular_inss(salario_bruto)
        valor_dependentes = calcular_dependentes()
        # Para calcular o IRRF, desconta-se o INSS e deduz o valor dos dependentes primeiramente
        descontado_inss_dep = salario_bruto - valor_inss - valor_dependentes
        valor_irrf = calcular_irrf(descontado_inss_dep)
        valor_vt = calcular_vt()
        outros_descontos = verificar_input('Há outros descontos a serem considerados? Digite o valor em real:'
                                           ' R$', object_type=float)
        print(f'INSS: {valor_inss:.2f}\n'
              f'IRRF: {valor_irrf:.2f}\n'
              f'Vale Transporte: {valor_vt}\n'
              f'Outros descontos: {outros_descontos}\n'
              f'Dedução de dependentes: {valor_dependentes}')
        # Após o cálculo do IRRF, adiciona-se novamente o valor dos dependentes, uma vez que ele é usado para dedução do
        # IRRF, não do salário.
        return descontado_inss_dep - valor_irrf - valor_vt - outros_descontos + valor_dependentes

    print(f'O salário líquido é: {calcular_descontos():.2f}')

    # Reinicia ou encerra a aplicação dependendo da resposta
    if verificar_input('Calcular outro salário? (Sim/Não)\nResposta: ', object_type=str):
        main()
    else:
        exit()


if __name__ == '__main__':
    main()
