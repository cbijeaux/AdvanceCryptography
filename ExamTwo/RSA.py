class RSA:
    #
    # Function Name: encrypt  <STATIC>
    # Formal Parameters:
    #   1) [int] message: the message that needs to be encrypted
    #   2) [tuple(int,int)] public_key: the key that will be needed in order to encrypt the message, contains the n integer and the public exponent 
    # Return Value:int
    # Usage: encrpyts the message using RSA algorithms
    #
    @staticmethod
    def encrypt(message:int,public_key:tuple[int,int])->int:
        return RSA.square_multiply(message,public_key[1],public_key[0])
    #
    # Function Name: decrypt  <STATIC>
    # Formal Parameters:
    #   1) [int] ciphertext: encrypted text that needs to be decrypted
    #   2) [tuple(int,int)] private_key: the key needed to decrypt the ciphertext, contains 'd' integer and 'n' integer
    # Return Value:str
    # Usage: decrypts the cihper text into the original message
    #
    @staticmethod
    def decrypt(ciphertext:int,private_key:tuple[int,int])->str:
        return RSA.square_multiply(ciphertext,private_key[1],private_key[0])
    #
    # Function Name: eulers_totient  <STATIC>
    # Formal Parameters:
    #   1) [int] number: the number that need to be calculated using the eulers toitient
    # Return Value:int
    # Usage: calculates the phi of number
    #
    @staticmethod                           #I am aware of (p-1)(q-1)=n, but I found this algorithm and 
    def eulers_totient(number:int)->int:    #I thought it would be cool to utilize it. 
        prime_number=2
        result=number
        while prime_number**2<=number:  
            if number%prime_number==0:
                while number%prime_number==0:
                    number//=prime_number
                result*=(1-1/prime_number)
            prime_number+=1                 #goes to the next prime number once the current one is no longer needed
        if number>1:
            result*=(1-1/number)
        return result                       #returns the final result
    #
    # Function Name: square_multiply  <STATIC>
    # Formal Parameters:
    #   1) [int] value: the base value
    #   2) [int] power: the base exponent connected to the value
    #   3) [int] mod: the modulous
    # Return Value:int
    # Usage: calculates the 'value^power modulous mod'using the squared mutliplication algorithm
    #
    @staticmethod
    def square_multiply(value:int,power:int,mod:int)->int:
        current_value=1
        binary_power=RSA.decimal_to_binary(power)
        for bit in binary_power:
            current_value=current_value**2%mod      #squaring happens regardless, the only condition to check is
            if bit=='1':                            #if 1 is present at the end, which requires an additional calculation
                current_value=current_value*value%mod   #modulous is calculated between everystep
        return current_value
    #
    # Function Name: generate_keys  <STATIC>
    # Formal Parameters:
    #   1) [int] p: the p integer
    #   2) [int] q: the q integer
    # Return Value:tuple(tuple(int,int),tuple(int,int))
    # Usage: generates the public and private key tuples within a tuple
    #
    @staticmethod
    def generate_keys(p: int, q: int)->tuple[tuple[int,int],tuple[int,int]]:
        n=p*q
        phi_n=RSA.eulers_totient(n)
        public_exponent=17
        d=RSA.euclidian.extendedEuclidean(public_exponent,phi_n)        #using previously made extended euclidean algorithm to find d
        public_key=(n,public_exponent)
        private_key=(n,d)
        return public_key,private_key
    #
    # Function Name: decimal_to_binary  <STATIC>
    # Formal Parameters:
    #   1) [int] decimal: the integer value to be converted to binary
    # Return Value:str
    # Usage: converts decimal integer to binary string
    #
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
    class euclidian:
        #
        # Function Name: GCD  <STATIC>
        # Formal Parameters:
        #   1) [int] a: the first integer used for the function
        #   2) [int] b: the second integer used for the function
        # Return Value:int
        # Usage: used to calculate the GCD of the integers a and b
        #
        @staticmethod
        def GCD(a:int,b:int)->int:
            if a==0 or b==0:  # if one of the values is 0, then the GCD is the highest of the two integers
                return a+b    # I am practicing some brachless programming to use in my code, this seems like a good        start to use it
            while b:          # will only leave while loop if b=0, since 0 is equivalent to False
                a,b=b,RSA.euclidian.modular(a,b) # how this works is simple. the function uses euclidian.modular() to calculate
            return abs(a)    # a mod b. the current b value is stored in a, and the a mod b result is stored in b                                         
        #                                    # this continues until b=a, to which then the absolute value of a is returned.
        # Function Name: extendedEuclidean  <STATIC>
        # Formal Parameters:
        #   1) [int] x: the integer value
        #   2) [int] n: the modular value
        # Return Value:int or str
        # Usage: uses the extended Euclidean Algorithm to calculate the inverse of x modulo n.
        #        Returns string stating that no inverse can be found if the GCD of the two numbers is above 1. 
        @staticmethod 
        def extendedEuclidean(x: int ,n: int)->int|str:
            if RSA.euclidian.GCD(n,x)!=1:               # handles the edge case where there is no inverse value
                return "NO INVERSE FOUND"           
            steps=[]           #individual lists created for each portion so it is easier to track visually
            quotients=[]
            remainder=[]
            base=n
            increment=[]    #current base or previous quotient[a]= quotients[x](increment[q])+remainder[r]
            # zero step
            quotients.append(x)                         # quotient is current x value
            remainder.append(RSA.euclidian.modular(n,x))    # remainder is calculated using the modular function
            increment.append((n-remainder[-1])/x)       # increment is calculated using (base-remainder)/increment
            steps.append(0)                             # Zero step is by default 0
            if remainder[-1]==0:                        # handles the edge case where the answer is calculated after the first step
                return 0        # technically this needs to do one more step cacluation, but most of my research has found that if the answer is found at this point
                                # then the answer is typically zero. As a result, we can skip a calculation and just return 0. 
            # first Step
            remainder.append(RSA.euclidian.modular(quotients[-1],remainder[0]))     # the quotient mod remainder value is added to remainder list
            increment.append((quotients[-1]-remainder[-1])/remainder[-2])       # pulls values from list to calculate increment and adds it to the list
            quotients.append(remainder[-2])                                     # second to last remainder value added to quotients, to act as the quotient for the next round
            steps.append(1)                                                     # first step is by default 1
            # start of loop
            while remainder[-1]:                                                    # while loop continues until remainder is zero                                             
                remainder.append(RSA.euclidian.modular(quotients[-1],remainder[-1]))    # remainder is again calculated from the current quotient and remainder
                increment.append((quotients[-1]-remainder[-1])/remainder[-2])       # next increment is again calculated: (quotients-remainder)/x
                quotients.append(remainder[-2])                                     # new quotient pulled from remainder list
                steps.append(0)                                                     # the step counter is first initialized as zero, then assigned its actual value in the next line
                steps[-1]=RSA.euclidian.modular(steps[-3]-(steps[-2]*increment[-3]),base)  # p_(i-2)-p_(i-1)*q(i-2) mod base (increment is set to [-3] because the new value is initialize before step is calculated)
            return int(RSA.euclidian.modular(steps[-2]-(steps[-1]*increment[-2]),base)) # since the modular inverse is p(k+2) after finding one, we need to do the step calculation one more time before returning the final value
        #
        # Function Name: modular  <STATIC>
        # Formal Parameters:
        #   1) [int] numberone: the first integer
        #   2) [int]  numbertwo: the second integer
        # Return Value:int
        # Usage: calculates numberone mod numbertwo and returns the int value
        #
        @staticmethod
        def modular(integer: int, modulo:int )-> int:
            if integer==0 or modulo==0:
                return integer+modulo  # handles edge case where either numberone or numbertwo is 0
            return integer%modulo

