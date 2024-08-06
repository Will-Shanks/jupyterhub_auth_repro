# Jupyterhub PAMAuthenticator bug repro

## Setup
- uses podman (although could be easily converted to use docker instead
- `make start` builds and starts the jupyterhub container on port `8000`
- `login.py` is a simple script that attempts to login to the hub with 20 different users at varrying levels of concurency
- `auth.py` is a copy of `auth.py` from the jupyterhub source, but with the PAMAuthenticator executor set to `ThreadPoolExecutor(10)` instead of `ThreadPoolExecutor(1)`
  - there is already an example line commented out in the makefile for how to patch this into the hub
- `login` is the pam stack login file with `auth required pam_exec.so quiet /bin/sleep 5` near the top to simulate a delay in the pam stack

## Notes
- from running `login.py` on the hub with and without the `auth.py` patch one can clearly see the difference in performance
```
# with a patched thread pool size
threads, run1(sec), run2(sec), run3(sec)
1, 101.91, 101.68, 101.61
2, 50.89, 50.94, 50.99
3, 35.77, 35.79, 35.77
4, 25.59, 25.55, 25.63
5, 20.48, 20.46, 20.52
6, 20.57, 20.59, 20.49
7, 15.42, 15.43, 15.47
8, 15.49, 15.52, 15.48
9, 15.39, 15.44, 15.45
10, 10.44, 10.43, 10.49
11, 10.39, 10.38, 10.42
12, 10.41, 10.42, 10.40

# without thread pool size patch
1, 102.02, 101.69, 101.71
2, 101.20, 101.21, 101.42
3, 101.18, 101.19, 101.40
4, 101.25, 101.08, 101.33
# snipped, since timing stays the same
```
- 20 logins * 5 sec delay each = 100s, this clearly illustrates how the PAMAuthenticator handles auth requests sequentially, with no concurency, unless the executor is patched to use more than one thread.
