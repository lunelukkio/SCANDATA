from framework.idcardfactory.id_card_factory import IDCardFactory, IDCardFactoryB

"""
https://tachikawa844.hatenadiary.org/entry/20081224/1230095888
"""

def startMain(factoryObject):
    card1 = factoryObject.create("Hiroshi Yuki")
    card2 = factoryObject.create("Tomura")
    card3 = factoryObject.create("Hanako Sato")
    card1.use()
    card2.use()
    card3.use()

if __name__ == "__main__":
    startMain(IDCardFactory())
    
    startMain(IDCardFactoryB())