#!/usr/bin/python
from quickbash.quickbash import qsh

if __name__ == "__main__":
    code = """
    (@let a "b")(@let b "C")
    (@let A (* (+ 2 3) (* 2 4)))
    (@let B (* (+ 3 3) (* 4 4)))
    (@tar ~zcpf "archive.tar.gz" "archive")
    (@for a ls (@echo a (* 2 2)))
    (@let VAR1 (@range 1 10))
    (@let VAR2 'HELLO WORLD!')
    (@export B 'hello world')
    (@if-else (== 1 2) (@echo (@exec 'date')) (@range 1 5))
    (@if-else (@-eq 1 2) (@range 2 10) (@range 1 5))
    (@if-else (@-eq "$a" "$b") (@range 2 10) (@range 1 5))
    """
    print qsh(code)
