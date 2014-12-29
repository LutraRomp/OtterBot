class Conv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.people={}
        self.places={}
        self.conversations=[]
        self.count=0

    def add(self,priv,person,place,sent):
        if not self.people.has_key(person): self.people[person]=[]
        if not self.places.has_key(place): self.places[place]=[]
        self.people[person].append(self.count)
        self.places[place].append(self.count)
        self.conversations.append((priv,self.count,person,place,sent))
        self.count=self.count+1

    def dump(self):
        for c in self.conversations:
            print "[%s:%d]%s@%s> %s" % c
