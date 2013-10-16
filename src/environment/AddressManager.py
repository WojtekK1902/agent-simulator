class AddressManager(object):

    _addresses = {}

    @staticmethod
    def getAddress(parent):
        parentId = None if parent is None else parent.getId()
        if parentId not in AddressManager._addresses:
            AddressManager._addresses[parentId] = 1
        else:
            AddressManager._addresses[parentId] += 1
        addr = AddressManager._addresses[parentId] 
        parentId = '' if parentId is None else str(parentId)
        return str(addr) if parent is None else '%s:%d' % (parentId, addr) 
