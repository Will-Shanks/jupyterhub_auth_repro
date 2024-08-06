from concurrent.futures import ThreadPoolExecutor

c = get_config()  #noqa
c.PAMAuthenticator.allow_all = True
c.JupyterHub.redirect_to_server = False
