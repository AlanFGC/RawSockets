# RawSockets
This is an implemantation of a raw IP/TCP socket
It generates IP/TCP packets that conform RFC standards and downloads and http 1.1 file or website.
### Testing:
Testing was done using wire shark and an ubuntu 22.04 virtual machine. 
Offloading has to be turned off ass well autmotic RST tcp packages.
Testing was done manually.
We did some early tests to join and parse application data but that was scrapped afterwards.
### Libraries
socket - handling raw sockets
random -  random number generation
httpGet - auxiliary functions not the get implementation
struct -  used for parsing and creating bytes
urllib - parse urls
### Devs
Developed by Alan Garcia
Evan Hanes helped during the intial developing stages


