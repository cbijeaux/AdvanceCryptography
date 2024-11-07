from Expression import Expression
class baseConversion:
    @staticmethod
    def decimal_to_binary(decimal:int)->str:
        final=''
        while decimal>0:
            if decimal%2!=0:
                final='1'+final
            else:
                final='0'+final
            decimal//=2
        return final
    def binary_to_decimal(binary:str)->int:
        return int(binary, 2)
    @staticmethod
    def binary_to_hexadecimal(binary:str)->str:
        decimal_number = int(binary, 2)
        return str(hex(decimal_number)[2:]).upper()
    def hexadecimal_to_binary(hex:str)->str:
        decimal_number = int(hex, 16)  # Convert hexadecimal to decimal
        binary_string = bin(decimal_number)[2:]  # Convert decimal to binary and remove the '0b' prefix
        return str(binary_string)
    @staticmethod
    def decimal_to_hexadecimal(decimal:int)->str:
        return str(hex(decimal)).upper()
    @staticmethod
    def hexadecimal_to_decimal(hex:str)->int:
        return int(hex, 16)
    @staticmethod
    def expression_to_binary(expression:object)->str:
        keys=expression.getKeys()
        bits=['0']*(max(keys)+1)
        for element in keys:
            bits[element]='1'
        bits.reverse()
        return ''.join(bits)
    @staticmethod
    def binary_to_expression(binary:str)->str:
        container=[]
        length=len(binary)
        counter=0
        while counter<length:
            if binary[counter]!='0':
                if counter==length-1:
                    container.append(f'1')
                elif counter==length-2:
                    container.append('x')
                else:
                    container.append(f'x^{length-counter-1}')
            counter+=1
        return '+'.join(container)
