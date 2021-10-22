# EncryptoCLI - By Arpan Pandey
![EncryptoCLI Thumbnail](./docs-files/EncryptoCLI-Thumbnail.png)

## 📚 Description
Encrypto CLI is a command line program that provide you with a intuitive and easy-to-use program that allows for a highly efficient and customisable interface to generate hashes of files or encrypt them. This allows you to encrypt and decrypt files or text data. This is all powered by the [Fernet](https://cryptography.io/en/latest/fernet/) Encryption.    

## Technologies Used
* Python3
* Cryptography Module (Fernet Encryption)
* Hashing Module
* Termcolor
* PyInquirer
* Scrypt

## How it works?
The idea is very simple. The program first asks you about which operation do you want to perform and then asks you 2-3 questions relative to which operation you have selected.![First Image](./docs-files/screenshots/1.png)    

## Hashing
You can generate hashes for text or file data by selecting the algorithm from the 5 options provided: 
![Hashing Image](./docs-files/screenshots/3.png)
The five algoritms supported are:
* MD5
* SHA256
* SHA512
* BLAKE2
* BLAKE2b

Also, if you are interested in an analysis of these algoritms or implementing them by yourself you can head over to this article that I wrote on [hashing](https://hackersreboot.tech/articles/Cryptography/hashing).

## Encrypting 
You can encrypt data by going through these steps.
1. Select the type of data you want to encrypt. ![Encrypt Type Selection](./docs-files/screenshots/6.png)
2. Input the data (either the text or path to a file). ![Encrypt Data Input](./docs-files/screenshots/7.png)
3. Enter a password. ![Encrypt Data Password](./docs-files/screenshots/8.png)
4. And you are done.

## Decrypting 
You can decrypt data by going through these steps.
1. Select the type of data you want to decrypt. ![Decrypt Type Selection](./docs-files/screenshots/9.png)
2. Input the data (either the text or path to a file). ![Decrypt Data Input](./docs-files/screenshots/10.png)
3. Enter the password. ![Decrypt Data Password](./docs-files/screenshots/11.png)
4. And you are done.


## 🐋 Docker
You can pull this image from Docker Hub and build it very easily.
1. Just pull the image. 
    ```bash
    docker pull arpanpandey/encrypto:latest
    ```
OR 

1. You can build the image using.
    ```bash
    docker build --pull --rm -f "Dockerfile" -t arpanpandey/encrypto:latest "."
    ```

2. Running the container with the image (Be sure to put the `-t` and `-d` flag.)
    ```bash
    docker run -t -d arpanpandey/encrypto:latest
    ```

## License
This project is licensed under the MIT License.

### Video Demo
You can access the video demo at: [https://youtu.be/Zmf2EK9jPCw](https://youtu.be/Zmf2EK9jPCw)

#### Thank You!
Thanks a lot to the team at CS50 for teaching me so much about the fascinating world of computer science and programming.