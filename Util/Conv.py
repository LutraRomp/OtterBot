class Conv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.people={}
        self.places={}
        self.conversations=[]
        self.count=0

    def add(self,priv,person,place,sent):
        if not self.people.has_key(person): self.people[person]=[place]
        if not self.places.has_key(place): self.places[place]=[person]
        self.conversations.append((priv,person,place,sent))
        self.count=self.count+1

    def dump(self):
        for c in self.conversations:
            print "[%s]%s@%s> %s" % c
