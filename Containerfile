FROM quay.io/jupyterhub/jupyterhub:latest

RUN useradd foo
RUN echo "foo:bar" | chpasswd

RUN for i in $(seq 1 200); do useradd "foo$i"; echo "foo$i:bar$i" | chpasswd; done

COPY login /etc/pam.d/login

CMD /usr/bin/python3 /usr/local/bin/jupyterhub -f /etc/jupyterhub/jupyterhub_config.py
