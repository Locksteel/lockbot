import json

class MarriageUser:
    '''Class to hold users in the marriage feature'''
    
    allUsers: dict[tuple[int, int], 'MarriageUser'] = {}
    
    def __init__(self,
                 id: int,
                 guildID: int,
                 ):
        self.id = id
        self.guildID = guildID
        self.children:  list[int] = []
        self.parents:   list[int] = []
        self.partners:  list[int] = []
        
        self.save_path = f'serverData/{self.guildID}/{self.id}.json'
        
        self.allUsers[(self.id, self.guildID)] = self
        
    def get(self,
            id: int,
            guildID: int
            ):
        assert id
        v = self.allUsers.get((id, guildID))    # get MarriageUser object from allUsers dict
        if v: return v                          # if passed MarriageUser object exists, return it
        return self(id=id, guildID=guildID)     # else create new MarriageUser object and return that
        
    def getDict(self):
        return {'id': self.id,
                'guild_id': self.guildID,
                'children': self.children,
                'parents': self.parents,
                'partners': self.partners
                }
    
    def saveJSON(self):
        with open(self.save_path, 'w') as f:
            json.dump(self.getDict(), f)
            
    def loadJSON(self, path: str = None):
        path = self.save_path if path is None else path
        
        try:
            with open(self.path) as f:
                userDict = json.load(f)
                
            self.children = userDict['children']
            self.parents = userDict['parents']
            self.partners = userDict['partners']
        except FileNotFoundError:
            print(f"No save found for user {self.id} in guild {self.guildID}. No changes have been made.")
    
    def addChild(self, childID: int):
        child = self.get(childID, self.guildID) # get child object from ID
        
        self.children.append(childID)   # add child ID to this object's list of children
        child.parents.append(self.id)   # add this object's ID to list of child's parents
        
        # for partnerID in self.partners:                 # for each partner this object has
        #     partner = self.get(partnerID, self.guildID) # get partner object from ID
            
        #     child.parents.append(partnerID)     # add child ID to partner's list of children
        #     partner.children.append(childID)    # add child ID to partner's list of children
    
    def addPartner(self, partnerID: int):
        partner = self.get(partnerID, self.guildID) # get partner object from ID
        
        self.partners.append(partnerID)      # add partner ID to this object's list of partners
        partner.partners.append(self.id)    # add this object's ID to list of partner's partners