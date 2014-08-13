#!/usr/bin/python
from lib.compiler import *

if __name__ == "__main__":
    code = """
    (* (+ 2 3) (* 2 4));
    (+ 1 6);
    ( @bzip2 "a.bz" "a" "\'klk" nil );
    (+ (* 3 4) 2);
    (@for a ls (@echo a (* 2 2)));
    (@range 1 10);
    (+ (* 3 4) 2);    
    (@let A 'hello world');
    (@export B 'hello world');
    (@if-else (== 1 2) (@range 2 10) (@range 1 5));
    (@if-else (@-ieq 1 2) (@range 2 10) (@range 1 5));
    (@if-else (@-eq "$a" "$b") (@range 2 10) (@range 1 5));
    """
    print qsh(code)
