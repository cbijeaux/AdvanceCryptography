class Expression:
    def __init__(self,expression:str,chosen_variable='x')->None: 
        self._variable=chosen_variable
        self._express_dict={}
        if expression!='':
            self.parse(expression)
        self._keys=''
        self.setKeys()
        self._base_two=False
    def evaluate(self,x_value):
        total=0
        for element in self._keys():
            total+=self.getVariable(element).calculate(x_value)
        return total
    def getKeys(self):
        return self._keys
    def toggleBaseTwo(self):
        self._base_two= not self._base_two
    def setDict(self,new_dict:dict):
        self._express_dict=new_dict
        self.setKeys()
    def getDict(self):
        return self._express_dict
    def setKeys(self):
        self._keys=list(self._express_dict.keys())
        self._keys.sort(reverse=True)
    def getVariable(self,key):
        return self._express_dict.get(key,False)
    def parse(self,original_expression:str)->dict:
        positive=True if original_expression[0]!='-' else False
        found_variable=False
        counter=0
        degree=1
        coefficient=1
        while counter<len(original_expression):
            current=original_expression[counter]
            if current==self._variable:
                found_variable=True
                counter+=1
            elif current in ['-','+'] and counter!=0:
                degree=0 if not found_variable else degree
                if not self._express_dict.get(degree,False):
                    self._express_dict[degree]=Expression.variable(coefficient,degree)
                    degree=1
                    coefficient=1
                else:
                    self._express_dict[degree]+=Expression.variable(coefficient,degree)
                if current=='-': 
                    positive=False
                else:
                    positive=True
                counter+=1
                found_variable=False
            elif current=="^":
                degree,increment=Expression.getNumbers(original_expression[counter+1:])
                counter+=increment+1
            else:
                coefficient,increment=Expression.getNumbers(original_expression[counter:])
                if not positive:
                    coefficient*=-1
                counter+=increment
        degree= degree if found_variable else 0
        if not self._express_dict.get(degree,False):
            self._express_dict[degree]=Expression.variable(coefficient,degree)
        else:
            self._express_dict[degree]+=Expression.variable(coefficient,degree)
    @staticmethod
    def getNumbers(substring:str):
        counter=0
        container=''
        while counter<len(substring) and substring[counter].isdigit():
            container+=substring[counter]
            counter+=1
        return int(container),counter                

    def baseTwoConversion(self):
        for element in self.getKeys():
            self.getVariable(element).baseTwo()
            if self.getVariable(element).getCoefficient()==0:
                del self._express_dict[element]
        self.setKeys()
    def __add__(self,other:object):
        new_expression=Expression('')
        new_expression.setDict(self.getDict())
        for element in other.getKeys():
            if new_expression._express_dict.get(element,False):
                new_expression._express_dict[element]=new_expression.getVariable(element)+other.getVariable(element)          
            else:
                new_expression._express_dict[element]=other.getVariable(element)
        new_expression.setKeys()
        return new_expression
    def __sub__(self, other: object):
        new_expression = Expression('')
        new_expression.setDict(self._express_dict.copy())
        for element in other.getKeys():
            if element in new_expression._express_dict:
                target=new_expression.getVariable(element) - other.getVariable(element)
                if not target.isZero():
                    new_expression._express_dict[element] = (
                        new_expression.getVariable(element) - other.getVariable(element)
                    )
                else:
                    del new_expression.getDict()[element]
            else:
                new_expression._express_dict[element] = Expression.variable(other.getVariable(element).getCoefficient()*-1, other.getVariable(element).getDegree())
        new_expression.setKeys()
        return new_expression    
    def __mul__(self, other: object):
        new_dict = {}
        current = self.getKeys()
        incoming = other.getKeys()
        for one in current:
            for two in incoming:
                new_var = self.getVariable(one) * other.getVariable(two)
                degree = new_var.getDegree()
                if degree in new_dict:
                    new_dict[degree] += new_var
                else:
                    new_dict[degree] = new_var
        result_expression = Expression("")
        result_expression.setDict(new_dict)
        result_expression.setKeys()
        return result_expression
    def __mod__(self, other):
        if self < other:
            return self
        if self._base_two:
            self.baseTwoConversion()
        current = self
        def modulo(value: object, divisor: object):
            max_divisor = max(divisor.getKeys())
            max_value = max(value.getKeys())
            degree_difference = max_value - max_divisor
            coefficient_ratio = value.getVariable(max_value).getCoefficient()*divisor.getVariable(max_divisor).getCoefficient()
            new_dict = {degree_difference: Expression.variable(coefficient_ratio, degree_difference)}
            reduction_term = Expression('')
            reduction_term.setDict(new_dict)
            resulting_expression = reduction_term * divisor
            return value - resulting_expression
        while current >= other:
            current = modulo(current, other)
            if self._base_two:
                current.baseTwoConversion()
        return current
    def __ge__(self,other:object):
        current=self.getKeys()
        comparison=other.getKeys()
        if max(current)>=max(comparison):
            return True 
        return False 
    def __le__(self,other:object):
        current=self.getKeys()
        comparison=other.getKeys()
        if max(current)<=max(comparison):
            return True 
        return False 
    def __lt__(self,other:object):
        current=self.getKeys()
        comparison=other.getKeys()
        if max(current)<max(comparison):
            return True 
        return False
    def __str__(self):
        keys=self.getKeys()
        first=keys[0]
        container=f'{self.getVariable(first)}' if self.getVariable(first).isPositive() else f'-{self.getVariable(first)}'
        for element in range(1,len(keys)):
            if self._express_dict[keys[element]].isPositive():
                container+=f'+'
            container+=f'{self._express_dict[keys[element]]}'
        return container
    class variable:
        def __init__(self,coefficient,degree,chosen_varaible='x'):
            self._coefficient=coefficient
            self._degree=degree
            self._variable=chosen_varaible
        def calculate(self,x):
            return (x**self._degree)*(self._coefficient)
        def getCoefficient(self):
            return self._coefficient
        def getDegree(self):
            return self._degree
        def isPositive(self):
            return self._coefficient>0
        def isZero(self):
            return self._coefficient==0
        def baseTwo(self):
            self._coefficient=self._coefficient%2
        def __mul__(self,other:object)->object:
            new_coefficent=self.getCoefficient()*other.getCoefficient() 
            new_degree=self.getDegree()+other.getDegree()
            return Expression.variable(new_coefficent,new_degree,self._variable)
        def __add__(self,other:object)->object:
            return Expression.variable(self.getCoefficient()+other.getCoefficient(),self._degree,self._variable)
        def __sub__(self,other:object)->object:
            return Expression.variable(self.getCoefficient()-other.getCoefficient(),self._degree,self._variable)
        def __eq__(self,other):
            if self.getDegree()==other.getDegree() and self.getCoefficient()==other.getCoefficient():
                return True 
            else:
                return False 
        def __ne__(self,other):
            if self.getDegree()!=other.getDegree() or self.getCoefficient()!=other.getCoefficient():
                return True 
            else:
                return False 
        def __str__(self):
            if abs(self._degree)>1 and abs(self._coefficient)>1:
                return f'{self.getCoefficient()}x^{self.getDegree()}'
            if self._degree==0:
                return f'{abs(self._coefficient)}'
            if self._degree==1 and abs(self._coefficient)>1:
                return f'{abs(self._coefficient)}x'
            if self._degree==1 and abs(self._coefficient)==1:
                return f'x'
            if self._degree>1 and abs(self._coefficient)==1:
                return f'x^{self._degree}'