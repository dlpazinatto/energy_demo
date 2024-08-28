from conectors.connector_play import ConnectorPlay

def connector_play():
    key = ''
    connector = ConnectorPlay(key)
    connector.get_page("https://conecte.celesc.com.br/autenticacao/login", key)
    connector.close()

if __name__ == "__main__":
    connector_play()
