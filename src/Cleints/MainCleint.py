import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from Models.Key import KeyProp
from Factories.Encryptor import Encryptor
from Factories.EncryptorSRound import EncryptorSRound

def main():
    key = KeyProp().get_key()   
    encryptor = Encryptor(key)
    encryptor2 = EncryptorSRound(key)
    plaintext = input("Enter Text: ")
    
    encrypted_text = encryptor.encrypt(plaintext)
    encrypted_text2 = encryptor2.encrypt(plaintext)

    print("-------------")
    print(f"Encrypted Text: {encrypted_text}")
    print("-------------")
    print(f"Encrypted with s Round method Text: {encrypted_text2}")
    print("-------------")

    print("Plain text and Encrypted text saved")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("plaintext.txt", "a") as f_plain:
        f_plain.write(f"{timestamp} - {plaintext}\n")
    
    #Append
    with open("encrypted.txt", "a") as f:
        f.write(f"{timestamp} - {encrypted_text}\n")

if __name__ == "__main__":
    main()