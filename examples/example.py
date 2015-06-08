#!/usr/bin/env python
import os
import sys
PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(PATH))
from quickbash.quickbash import qsh

if __name__ == "__main__":
    code = """
    (@let a "b")(@let b "C")
    (@let A (* (+ 2 3) (* 2 4)))
    (@let B (* (+ 3 3) (* 4 4)))
    (@tar ~zcpf "archive.tar.gz" "archive")
    (@for a ls (@echo (@var a) (* 2 2)))
    (@let VAR1 (@range 1 10))
    (@let VAR2 'HELLO WORLD!')
    /* This is a raw command */
    (@comment 'a raw command')
    (@raw 'cat myfile.txt | gzip --best - > myfile.txt.gz')
    // Quick Bash comment (C++ style) (will be omitted in the output)
    (@comment 'the following exports a variable named B')
    (@export B "hello world\'")    
    (@pipe (@echo 'hello') (@ssh host1))
    (@if-else (== 1 2) (@echo (@exec 'date')) (@ls ~alr))
    (@if-else 
        (@eq? 1 2) 
            (@let R (@range 2 10)) 
        (@let R (@range 1 5))
    )
    (@if-else 
        (@ne? "$a" "$b") 
            (@let G (@range 2 10)) 
        (@let G (@range 1 5))
    )
    (@let CURRENT_DATETIME (:datetime.datetime.utcnow))
    (@let A_DATETIME (:datetime.datetime.strptime "2014-05-06" "%Y-%m-%d"))
    """
    print qsh(code)
