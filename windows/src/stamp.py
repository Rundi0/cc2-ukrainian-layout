"""sha256 of uacc.c, CRLF-insensitive.

git checks the file out with native line endings, so a plain hash of the bytes
on disk differs between a Linux clone, a Windows clone with core.autocrlf=true
and one with autocrlf=false.  install.ps1 computes the same normalised hash.
"""
import hashlib
import pathlib

src = pathlib.Path(__file__).with_name('uacc.c').read_bytes()
print(hashlib.sha256(src.replace(b'\r\n', b'\n')).hexdigest())
