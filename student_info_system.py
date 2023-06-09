import hashlib
import time
import random
import copy 

class Student:
    def __init__(self, id, name, age, courses):
        self.id = id
        self.name = name
        self.age = age
        self.courses = courses

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256(f"{self.index}{self.timestamp}{self.data}{self.previous_hash}".encode('utf-8')).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.validators = []

    def assign_marks(self, student_id, course_id, marks):
        student = self.get_student_data(student_id)
        if student:
            updated_student = copy.deepcopy(student)
            # updated_student = student.copy()
            if course_id not in updated_student["courses"]:
                updated_student["courses"][course_id] = 0
            updated_student["courses"][course_id] += marks
            self.add_block(updated_student)
        else:
            print(f"Student with ID {student_id} not found.")

    def create_genesis_block(self):
        return Block(0, int(time.time()), "Genesis Block", "0")

    def add_validator(self, address, stake):
        self.validators.append(Validator(address, stake))

    def select_validator(self):
        total_stake = sum([validator.stake for validator in self.validators])
        validator_chances = [validator.stake / total_stake for validator in self.validators]
        return random.choices(self.validators, validator_chances)[0]

    def add_block(self, data):
        validator = self.select_validator()
        new_block = Block(len(self.chain), int(time.time()), data, self.chain[-1].hash)
        if validator.validate_block(new_block, self.chain[-1]):
            self.chain.append(new_block)
            validator.balance += 10

    def is_valid(self):
        validator = self.select_validator()
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if not validator.validate_block(current_block, previous_block):
                return False
        return True
    
    def get_student_data(self,student_id):
        for block in reversed(self.chain):
            if block.data != 'Genesis Block':
                if block.data.get("id") == student_id:
                    student = block.data
                    break
        return student

class Validator:
    def __init__(self, address, stake):
        self.address = address
        self.stake = stake
        self.balance = 0

    def validate_block(self, block, previous_block):
        if block.previous_hash != previous_block.hash:
            return False
        if block.hash != block.calculate_hash():
            return False
        return True


def main():
    student_blockchain = Blockchain()
    student_blockchain.add_validator("0xValidator1", 10)
    student_blockchain.add_validator("0xValidator2", 20)
    student1 = Student("001", "Alice", 20, {})
    student_blockchain.add_block(student1.__dict__)
    student_blockchain.assign_marks("001", "MATH101", 90)
    student_blockchain.assign_marks("001", "MATH101", 30)
    student_blockchain.assign_marks("001", "PHYS101", 85)
    print("Validator 1 balance:", student_blockchain.validators[0].balance)
    print("Validator 2 balance:", student_blockchain.validators[1].balance)
    student2 = Student("002", "Bob", 22, {"Chemistry": 0, "Biology": 0})
    student_blockchain.add_block(student2.__dict__)
    print("Validator 1 balance:", student_blockchain.validators[0].balance)
    print("Validator 2 balance:", student_blockchain.validators[1].balance)
    studentone = student_blockchain.get_student_data("001")
    studenttwo = student_blockchain.get_student_data("002")
    print(studentone)
    print(studentone['courses'])
    print(studenttwo['courses'])
    print("Blockchain valid?", student_blockchain.is_valid())

if __name__ == "__main__":
    main()