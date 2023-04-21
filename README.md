# Zeply Test - Donald Dimitriovski

# This is the repo for Zeply's coding assignment


# Introduction
The purpose of this code challenge is to assess your technical skills, namely, code structure,
code quality, naming conventions, knowledge of commonly used frameworks, and overall
problem-solving skills.


Some decisions will be left up to you to make. You can choose any framework and third-party
modules that you feel improve code clarity and development agility, as well as a database
engine of your choice. The task at hand is explained in the following sections. Whatever is
unspecified will be up to you to determine

# Specification
In this Python challenge we want you to implement a simple REST API for
generating valid cryptocurrency addresses and displaying them.
Specifically, your API should provide three endpoints, as follows:
  1. Generate address 
  2. List addresses
  3. Retrieve address

## 1. Generate address
The core functionality of the API is to take a cryptocurrency as input and return a valid
address for that currency as output. Each cryptocurrency is identified by its three-letter
acronym, such as “BTC” or “ETH” for Bitcoin and Ethereum respectively. Support for the latter
two currencies is sufficient for this task, however, additional coins are welcome and earn you
bonus points. The expected address is a string like
2N3kfQkYDH48Z4ZR88uaytLHNVbNJowjTym`, whose validity can be checked using crypto
libraries, or websites like blockchain.com. For example, the following URL is for validating and
retrieving information about the aforementioned address:

https://www.blockchain.com/btc-testnet/address/2N3kfQkYDH48Z4ZR88uaytLHNVbNJowjTym

Generate Address
Each address should be stored in the database and associated with an integer ID that will be
used for retrieval purposes. The implementation should have the ability to generate multiple
addresses using a single private key.


## 2. List and Retrieve address
The API will be made complete by two additional endpoints, that is, to list and retrieve
previously generated addresses. The List endpoint takes no input and returns a list of all the
addresses generated so far. The Retrieve endpoint takes an ID, and returns the corresponding
address as stored in the database.

### General notes
You should consider that this service is going to be used in a software wallet website. Thus, it
is crucial to store securely whatever is needed to recover the wallet from backups in case of
any disaster. For example, private keys and seeds. If the deliverable is deemed satisfactory,
we will organise a session with you to discuss the solution, focusing on points such as:


  * What is needed for implementing the next steps, such as signing transactions? 

  * Is your code and data ready for that?

  * How would you back up your private keys?

  * How should a teammate add support for a new coin to the API?

  * The format you’ve chosen for inputs and outputs of the API
