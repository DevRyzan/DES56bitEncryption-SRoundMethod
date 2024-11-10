import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from Models.Key import KeyProp
from Factories.Encryptor import Encryptor
from Factories.EncryptorSRound import EncryptorSRound
from Factories.DecryptionSRound import DecryptorSRound
from Factories.Decryption import Decryptor

def main():
    try:
        key = KeyProp().get_key()

        encryptor = Encryptor(key)
        encryptor2 = EncryptorSRound(key)
        decryptor2 = DecryptorSRound(key)
        decryptor = Decryptor(key)

        plaintext = input("Enter Text: ").strip()
        if not plaintext:
            print("Error: No text entered.")
            return
        print("Encrypting text...")
        encrypted_text = encryptor.encrypt(plaintext)
        encrypted_text2 = encryptor2.encrypt_sRound(plaintext)
        print("Decrypting text...")
        decrypted_text2 = decryptor2.decrypt_sRound(encrypted_text2)
        decrypted_text = decryptor.decrypt(encrypted_text)

        print("-------------")
        print(f"Encrypted Text: {encrypted_text}")
        print("-------------")
        print(f"Decrypted Text: {decrypted_text}")
        print("-------------")
        print(f"Encrypted with s Round method Text: {encrypted_text2}")
        print("-------------")
        print(f"Decrypted with s Round method Text: {decrypted_text2}")
        print("-------------")

        with open("plaintext.txt", "a") as f_plain:
            f_plain.write(f"-{plaintext}\n")
        
        with open("encrypted.txt", "a") as f:
            f.write(f"-{encrypted_text}\n")
        
        with open("decrypted.txt", "a") as f:
            f.write(f"-{decrypted_text}\n")
            
        print("Plain text and Encrypted text saved successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
if __name__ == "__main__":
    main()