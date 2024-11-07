from baseConversion import baseConversion
class Random:
    @staticmethod
    def bitStream(xor_index:list,base:list)->int:
        xor=xor_index
        new=base.copy()
        counter=1
        while new!=base or counter==1:
            compare=0
            counter+=1
            for element in range(len(xor)):
                compare=compare^int(new[xor[element]])
            new=[compare]+new[:-1]
        return counter
    @staticmethod
    def linearCongruentialGenerator(modulus, multiplier, increment, seed):
        seed_list = []
        while seed not in seed_list:
            seed_list.append(seed)
            seed = (multiplier * seed + increment) % modulus
        return seed_list
    @staticmethod
    def blumBlumShub(p,q,seed):
        modulus=p*q
        seed_list=[]
        while (seed:=(seed**2)%(modulus)) not in seed_list:
            seed_list.append(seed)
        container=''
        for element in seed_list:
            binary=baseConversion.decimal_to_binary(element)
            container+=binary[-1]
        return container

