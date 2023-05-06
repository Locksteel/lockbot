import json

class MarriageUser:
    '''Class to hold users in the marriage feature'''
    
    allUsers: dict[tuple[int, int], 'MarriageUser'] = {}
    
    def __init__(self,
                 id: int,
                 guildID: int,
                 empty: bool = False
                 ):
        self.id = id
        self.guildID:   int = guildID
        self.children:  list[int] = []
        self.parents:   list[int] = []
        self.partners:  list[int] = []
        self.pending:   bool = False
        
        self.savePath = f'serverData/{self.guildID}/{self.id}.json'
        
        if not empty: self.loadJSON()
        
        self.allUsers[(self.id, self.guildID)] = self
    
    def __del__(self):
        self.saveJSON()
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.saveJSON()
        
    def get(self,
            id: int,
            guildID: int
            ):
        assert id
        v = self.allUsers.get((id, guildID))        # get MarriageUser object from allUsers dict
        if v: return v                              # if passed MarriageUser object exists, return it
        return MarriageUser(id, guildID)            # else create new MarriageUser object and return that 
        
    def getDict(self):
        return {'id': self.id,
                'children': self.children,
                'parents':  self.parents,
                'partners': self.partners,
                'pending':  self.pending
                }
    
    def saveJSON(self):
        with open(self.savePath, 'w') as f:
            json.dump(self.getDict(), f)
            
    def loadJSON(self, path: str = None):
        path = self.savePath if path is None else path
        
        try:
            with open(self.savePath) as f:
                userDict = json.load(f)
                
            self.children = userDict['children']
            self.parents = userDict['parents']
            self.partners = userDict['partners']
            self.pending = userDict['pending']
        except FileNotFoundError:
            print(f"No save found for user {self.id} in guild {self.guildID}. No changes have been made.")
    
    def addChild(self, childID: int):
        child = self.get(childID, self.guildID) # get child object from ID
        
        self.children.append(childID)   # add child ID to this object's list of children
        child.parents.append(self.id)   # add this object's ID to list of child's parents
        child.saveJSON()                # save changes
        
        # for partnerID in self.partners:                 # for each partner this object has
        #     partner = self.get(partnerID, self.guildID) # get partner object from ID
            
        #     child.parents.append(partnerID)     # add child ID to partner's list of children
        #     partner.children.append(childID)    # add child ID to partner's list of children
    
    def addPartner(self, partnerID: int):
        partner = self.get(partnerID, self.guildID) # get partner object from ID
        
        self.partners.append(partnerID)     # add partner ID to this object's list of partners
        partner.partners.append(self.id)    # add this object's ID to list of partner's partners
        partner.saveJSON()                  # save changes
        
    def removeChild(self, childID: int):
        child = self.get(childID, self.guildID)
        
        self.children.remove(childID)
        child.parents.remove(self.id)
        child.saveJSON()
    
    def removePartner(self, partnerID: int):
        partner = self.get(partnerID, self.guildID)
        
        self.partners.remove(partnerID)
        partner.partners.remove(self.id)
        partner.saveJSON()
    
    def removeParent(self, parentID: int):
        parent = self.get(parentID, self.guildID)
        
        self.parents.remove(parentID)
        parent.children.remove(self.id)
        parent.saveJSON()
    
    def setPending(self, newVal: bool):
        self.pending = newVal
        self.saveJSON()
        
    def setOtherPending(self, id: int, newVal: bool):
        other = self.get(id, self.guildID)
        other.setPending(newVal)