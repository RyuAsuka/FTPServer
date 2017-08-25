# FTPServer
A simple FTP server and client implementation by Python

## Usage
python ./FTPClient.py <SERVER\_IP> <SERVER\_PORT>

python ./FTPServer.py

## Supported commands in FTP client
    ls <remote|local>                   List Files in current directory
    cd <remote|local> <dir>             Change Working directory
    upload <filename>                   Upload file from local directory to current remote directory
    download <filename> <localDir>      Download file from remote directory to
    md <remote|local> <DirName>         Make a new folder in current directory
    del <remote|local> <filename>       Delete a file in current remote directory
    deltree <remote|local> <DirName>    Delete a directory in current remote directory
    rename <remote|local> <old> <new>   Rename a file or a directory
    quit                                Quit FTP Client
