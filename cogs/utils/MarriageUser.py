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
    
    def saveJSON(self) -> None:
        with open(self.savePath, 'w') as f:
            json.dump(self.getDict(), f)
            
    def loadJSON(self, path: str = None) -> None:
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
    
    def addChild(self, childID: int) -> None:
        child = self.get(childID, self.guildID) # get child object from ID
        
        self.children.append(childID)   # add child ID to this object's list of children
        child.parents.append(self.id)   # add this object's ID to list of child's parents
        child.saveJSON()                # save changes
        
        # for partnerID in self.partners:                 # for each partner this object has
        #     partner = self.get(partnerID, self.guildID) # get partner object from ID
            
        #     child.parents.append(partnerID)     # add child ID to partner's list of children
        #     partner.children.append(childID)    # add child ID to partner's list of children
    
    def addPartner(self, partnerID: int) -> None:
        partner = self.get(partnerID, self.guildID) # get partner object from ID
        
        self.partners.append(partnerID)     # add partner ID to this object's list of partners
        partner.partners.append(self.id)    # add this object's ID to list of partner's partners
        partner.saveJSON()                  # save changes
        
    def removeChild(self, childID: int) -> None:
        child = self.get(childID, self.guildID)
        
        self.children.remove(childID)
        child.parents.remove(self.id)
        child.saveJSON()
    
    def removePartner(self, partnerID: int) -> None:
        partner = self.get(partnerID, self.guildID)
        
        self.partners.remove(partnerID)
        partner.partners.remove(self.id)
        partner.saveJSON()
    
    def removeParent(self, parentID: int) -> None:
        parent = self.get(parentID, self.guildID)
        
        self.parents.remove(parentID)
        parent.children.remove(self.id)
        parent.saveJSON()
    
    def setPending(self, newVal: bool) -> None:
        self.pending = newVal
        self.saveJSON()
        
    def setOtherPending(self, id: int, newVal: bool) -> None:
        other = self.get(id, self.guildID)
        other.setPending(newVal)
        
    # returns dict of lists of user ids
    def getGrandparents(self, greats: int = -1, grandparents: dict[str, list[int]] = {}, origin: int = 0) -> dict[str, list[int]]:
        # print('getGrandparent called with great=' + str(greats))
        # print('Initializing getGrandparent with dict: ' + str(grandparents))
        
        if greats == -1:
            origin = self.id
            grandparents = {}
            
        if not (greats == 0 and self.id == origin):
            for parentID in self.parents:
                if greats != -1:
                    if ('great ' * greats) + 'grandparents' in grandparents:
                        # print(('great ' * greats) + 'grandparents found in dict')
                        grandparents[('great ' * greats) + 'grandparents'].append(parentID)
                    else:
                        grandparents[('great ' * greats) + 'grandparents'] = [parentID]
                parent = self.get(parentID, self.guildID)
                
                grandparents.update(parent.getGrandparents(greats + 1, grandparents, origin))

        # print('Returning grandparent dict: ' + str(grandparents))
        return grandparents
    
    def getGrandchildren(self, greats: int = -1, origin: int = 0) -> dict[str, list[int]]:
        grandchildren = {}
        
        if greats == -1:
            origin = self.id
            
        if not (greats == 0 and self.id == origin):
            for childID in self.children:
                if greats != -1:
                    if ('great ' * greats) + 'grandchildren' in grandchildren:
                        grandchildren[('great ' * greats) + 'grandchildren'].append(childID)
                    else:
                        grandchildren[('great ' * greats) + 'grandchildren'] = [childID]
                parent = self.get(childID, self.guildID)
                
                grandchildren.update(parent.getGrandchildren(greats + 1, origin))

        return grandchildren
    
    def getSiblings(self) -> list[int]:
        siblings = []
        
        for parentID in self.parents:
            parent = self.get(parentID, self.guildID)
            for siblingID in parent.children:
                if siblingID != self.id and siblingID not in siblings:
                    siblings.append(siblingID)
                
        return siblings
    
    def getNiecesNephews(self) -> list[int]:
        niecesNephews = []
        
        for siblingID in self.getSiblings():
            sibling = self.get(siblingID, self.guildID)
            for childID in sibling.children:
                if childID != self.id and childID not in niecesNephews:
                    niecesNephews.append(childID)
        
        return niecesNephews
    
    def getAuntsUncles(self) -> list[int]:
        auntsUncles = []
        
        for parentID in self.parents:
            parent = self.get(parentID, self.guildID)
            for auID in parent.getSiblings():
                if auID != self.id and auID not in auntsUncles:
                    auntsUncles.append(auID)
        
        return auntsUncles
    
    def getStepparents(self) -> list[int]:
        stepparents = []
        
        for parentID in self.parents:
            parent = self.get(parentID, self.guildID)
            for partnerID in parent.partners:
                if partnerID != self.id and \
                    partnerID not in self.parents and \
                    partnerID not in stepparents:
                    stepparents.append(partnerID)
        
        return stepparents