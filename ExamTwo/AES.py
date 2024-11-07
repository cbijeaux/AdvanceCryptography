from Expression import Expression
from baseConversion import baseConversion

class AES:
    def __init__(self,s_box):
        self._sbox=s_box
    def encrypt(self,input_text,keys):
        encrypted=self.byteTransformation(input_text)
        encrypted=self.shiftTransformation(encrypted)
        if type(keys[0][0])==list:
            for key in keys:
                encrypted=self.mixColumns(encrypted,key)
        else:
            encrypted=self.mixColumns(encrypted,keys)
        return encrypted
    def decrypt(self,encrypted_text,keys):
        pass
    def byteTransformation(self,input_text):
        for element in range(len(input_text)):
            for second in range(len(input_text[element])):
                current=input_text[element][second]
                x_dec=baseConversion.hexadecimal_to_decimal(current[0])
                y_dec=baseConversion.hexadecimal_to_decimal(current[1])
                input_text[element][second]=self._sbox[x_dec][y_dec]
        return input_text
    def mixColumns(self,input_box,key):
        new=[[] for x in range(len(key))]
        for column in range(len(key)):
            current=[x[column] for x in input_box]
            for element in range(len(current)):
                new[element].append(baseConversion.binary_to_hexadecimal(self.mixColumnsCalculate(current,key[element])))
        return new
    def mixColumnsCalculate(self,input_row,key_row):
        temp=[]
        for element in range(len(input_row)):
            temp.append(AES.hexCalculate(input_row[element],key_row[element]))
        return AES.xor(temp[0],temp[1],temp[2],temp[3])
    @staticmethod
    def hexCalculate(hexone,hextwo):
        px=Expression('x^8+x^4+x+3+x+1')
        if hexone=='01':
            return baseConversion.hexadecimal_to_binary(hextwo)
        elif hextwo=='01':
            return baseConversion.hexadecimal_to_binary(hexone)
        binary_one=baseConversion.hexadecimal_to_binary(hexone)
        binary_two=baseConversion.hexadecimal_to_binary(hextwo)
        expresssion_one=baseConversion.binary_to_expression(binary_one)
        expression_two=baseConversion.binary_to_expression(binary_two)
        expresssion_one=Expression(expresssion_one)
        expression_two=Expression(expression_two)
        product=expresssion_one*expression_two
        if product>=px:
            product=product%px
        return baseConversion.expression_to_binary(product)
    def shiftTransformation(self,input_box):
        temp_box=[input_box[0]]
        counter=1
        length=len(input_box[0])
        for row in range(1,len(input_box)):
            temp=[]
            for element in range(len(input_box[0])):
                temp.append(input_box[row][((element+(counter))%length)])
            temp_box.append(temp)
            counter+=1
        return temp_box
    @staticmethod
    def xor(bits_one, bits_two, bits_three, bits_four):
        bits_one=bits_one.zfill(8)
        bits_two=bits_two.zfill(8)
        bits_three=bits_three.zfill(8)
        bits_four=bits_four.zfill(8)
        container = ''
        for element in range(len(bits_one)):
            container += str(
                int(bits_one[element]) ^ int(bits_two[element]) ^ int(bits_three[element]) ^ int(bits_four[element])
            )
        return container


aes_sbox = [
    ["63", "7C", "77", "7B", "F2", "6B", "6F", "C5", "30", "01", "67", "2B", "FE", "D7", "AB", "76"],
    ["CA", "82", "C9", "7D", "FA", "59", "47", "F0", "AD", "D4", "A2", "AF", "9C", "A4", "72", "C0"],
    ["B7", "FD", "93", "26", "36", "3F", "F7", "CC", "34", "A5", "E5", "F1", "71", "D8", "31", "15"],
    ["04", "C7", "23", "C3", "18", "96", "05", "9A", "07", "12", "80", "E2", "EB", "27", "B2", "75"],
    ["09", "83", "2C", "1A", "1B", "6E", "5A", "A0", "52", "3B", "D6", "B3", "29", "E3", "2F", "84"],
    ["53", "D1", "00", "ED", "20", "FC", "B1", "5B", "6A", "CB", "BE", "39", "4A", "4C", "58", "CF"],
    ["D0", "EF", "AA", "FB", "43", "4D", "33", "85", "45", "F9", "02", "7F", "50", "3C", "9F", "A8"],
    ["51", "A3", "40", "8F", "92", "9D", "38", "F5", "BC", "B6", "DA", "21", "10", "FF", "F3", "D2"],
    ["CD", "0C", "13", "EC", "5F", "97", "44", "17", "C4", "A7", "7E", "3D", "64", "5D", "19", "73"],
    ["60", "81", "4F", "DC", "22", "2A", "90", "88", "46", "EE", "B8", "14", "DE", "5E", "0B", "DB"],
    ["E0", "32", "3A", "0A", "49", "06", "24", "5C", "C2", "D3", "AC", "62", "91", "95", "E4", "79"],
    ["E7", "C8", "37", "6D", "8D", "D5", "4E", "A9", "6C", "56", "F4", "EA", "65", "7A", "AE", "08"],
    ["BA", "78", "25", "2E", "1C", "A6", "B4", "C6", "E8", "DD", "74", "1F", "4B", "BD", "8B", "8A"],
    ["70", "3E", "B5", "66", "48", "03", "F6", "0E", "61", "35", "57", "B9", "86", "C1", "1D", "9E"],
    ["E1", "F8", "98", "11", "69", "D9", "8E", "94", "9B", "1E", "87", "E9", "CE", "55", "28", "DF"],
    ["8C", "A1", "89", "0D", "BF", "E6", "42", "68", "41", "99", "2D", "0F", "B0", "54", "BB", "16"]
]
input_plaintext = [
    ["9D", "F1", "6E", "3C"],
    ["86", "BA", "A5", "03"],
    ["FA", "95", "D8", "95"],
    ["82", "47", "18", "C6"]
]
mix_columns_matrix = [
    ["02", "03", "01", "01"],
    ["01", "02", "03", "01"],
    ["01", "01", "02", "03"],
    ["03", "01", "01", "02"]
]

encrypter=AES(aes_sbox)
result=encrypter.encrypt(input_plaintext,mix_columns_matrix)
for list in result:
    print(list)