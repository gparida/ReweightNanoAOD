#a quick class used for lloading other modules in the package in a convenient way

class RecursiveLoader():
    def __init__(self):
        pass
    def LoadPath(self,PathToLoad):
        Module = __import__(PathToLoad)
        ToLoad = PathToLoad.split('.')
        if len(ToLoad) == 1:
            return Module
        else:            
            for i in range(1,len(ToLoad)):
                Module = getattr(Module,ToLoad[i])                
            return Module    
    #def LoadPath(self,PathToLoad):
	#print ("Module to Load: ",PathToLoad)
        #Module = __import__(PathToLoad)
	#Module = __import__(PathToLoad, fromlist=[None])
	#ToLoad = PathToLoad.split('.')
	#print ("After Splitting",ToLoad,ToLoad[len(ToLoad)-1])
	#Module = __import__(PathToLoad, fromlist=(ToLoad[len(ToLoad)-1]))
	#Module = __import__(PathToLoad)
	#print ("Module tha was loaded: ", type(Module),Module)
	#return Module
        #ToLoad = PathToLoad.split('.')
        #if len(ToLoad) == 1:
	    #print ("Entering If statement")
            #return Module
        #else:
	    #print ("Entering Else statement")            
            #for i in range(1,len(ToLoad)):
		#print ToLoad[i]
                #try:
		    #print ("Output of GetAtrr comamnd",getattr(Module,ToLoad[i]))
                    #Module = getattr(Module,ToLoad[i])
                #except AttributeError:
                    #print("oopsies")
                    #continue
            #print (type(Module),Module)                
            #return Module
    def LoadFromDirectoryPath(self,PathToLoad):
        #trim the .py file extension off
        PathToLoad=PathToLoad[:len(PathToLoad)-3]
        PathToLoad=PathToLoad.replace("/",".")        
        return self.LoadPath(PathToLoad)

