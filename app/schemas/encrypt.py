import base64

def cifrada(text:str):
    cifradaContr = base64.b64encode(text.encode('utf-8'))
    return cifradaContr.decode('utf-8')
    

def descifrada(text:str):
    return base64.b64decode(text).decode("utf-8")