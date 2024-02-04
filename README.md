# FileThiefEncrypted
**Warning! Do not use the codes/files provided here for any kind of malicious purposes.**
**The owner will not take any responsibility for any actions performed by any party using this repository files**
There are two files in the profect. CC_server.py (a code for a command and control server. the one that attacker runs on his device) and victim.py (contains the code for the actual malware that is sent to the victims computer (converted to .exe using pyinstaller in the actual scenario))
After attacker runs the CC_server.py on his computer and the victim runs the executable, the attacker gets a shell that supports the following commands:
  1. pwd - check the current location on in the victim's filesystem
  2. cd \<directory\> - switching the directory (supports both absolute and relative paths. supports ".." argument as well)
  3. ls - shows all the files and directories of the current directory
  4. download \<filename\> - steals (downloads) a file from a victims computer (NO ABSOLUTE PATH! IN ORDER TO DOWNLOAD, FIRST MOVE TO THE DIRECTORY OF THE DESIRED FILE). The file transfer is encrypted using the symmetric encryption AES algorithm
