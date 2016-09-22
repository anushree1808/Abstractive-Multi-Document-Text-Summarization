from collections import defaultdict 
from nltk.corpus import wordnet as wn
import logging

logging.basicConfig()
log = logging.getLogger("lexchain")
log.setLevel(logging.WARNING)

class Node(object):
    def __init__(self):
        self.adjacentNodes = {}
    def linkTo(self, target, link):
        self._typeCheckNode(target)
        self._typeCheckLink(link)
        self._addToEdge(target, link)
        target._addToEdge(self, link)
        
    def _removeFromEdge(self, target):
        del self.adjacentNodes[target]
        
    def _addToEdge(self, target, link):
        self.adjacentNodes[target] = link
        
    def unlink(self, target):
        self._typeCheckNode(target)
        target._removeFromEdge(self)
        self._removeFromEdge(target)
    def unlinkAll(self):
        nodesToUnlink = list(self.getAdjacentNodes())
        for target, _ in nodesToUnlink:
            self.unlink(target)
        assert len(self.adjacentNodes) == 0
    def isLinkedTo(self, target):
        self._typeCheckNode(target)
        return target in self.adjacentNodes
    def getAdjacentNodes(self):
        return self.adjacentNodes.iteritems()
    def getId(self):
        raise NotImplementedError("Please implement in subclass")
    
    def _typeCheckNode(self, obj):
        if not isinstance(obj, Node): raise TypeError 
    def _typeCheckLink(self, obj):
        if not isinstance(obj, LinkData): raise TypeError

class MetaChain(Node):
    def __init__(self, id):
        Node.__init__(self)  
        self.id = id
        self.nodeOrder = []
    def getId(self):
        return self.id

    def getLexNodes(self):
        return self.getAdjacentNodes()
    
    def _removeFromEdge(self, target):
        Node._removeFromEdge(self, target)
        self.nodeOrder.remove(target)
        
    def _addToEdge(self, target, link):
        Node._addToEdge(self, target, link)
        self.nodeOrder.append(target)
    
    def asList(self):
        return list(self.getAdjacentNodes())
    
    def getAdjacentNodes(self):
        for n in self.nodeOrder:
            yield n, self.adjacentNodes[n]
            
    def _typeCheckNode(self, obj):
        if not isinstance(obj, LexNode): raise TypeError
    
    def __len__(self):
        return len(self.adjacentNodes)
    def __getitem__(self, k):
        return self.adjacentNodes[k]
    def __iter__(self):
        return self.getAdjacentNodes()
    def __hash__(self):
        return self.getId().__hash__()
    def __eq__(self, other):
        return (False if not isinstance(other, MetaChain) else self.getId() == other.getId())
    def __str__(self):
        return str(self.getId())+":"+str([node for node in self.nodeOrder])+")"
    def __repr__(self):
        return self.__str__()
    
class LexNode(Node):
    
    def __init__(self, wordIndex, word, sensenum, spos=0, ppos=0):
        Node.__init__(self)
        
        self.word = word
        self.sensenum = sensenum
        self.wordIndex = wordIndex
        
        self.spos = spos
        self.ppos = ppos
    
    def _typeCheckNode(self, obj):
        if not isinstance(obj, MetaChain): raise TypeError   
    def __str__(self):
        return '%s_%s_%d'%(self.word, self.sensenum, self.wordIndex)
    def __repr__(self):
        return self.__str__()
    def __hash__(self):
        return (self.sensenum, self.word, self.wordIndex).__hash__()
    def __eq__(self, other):
        if not isinstance(other, LexNode):  return False
        return other.sensenum == self.sensenum and other.wordIndex == self.wordIndex and other.word == self.word 
    def getWord(self):
        return self.word
    def getSense(self):
        return self.sensenum
    def getId(self):
        return self.sensenum if self.sensenum else self.word
    def getWordIndex(self):
        return self.wordIndex
    def copy(self):
        lnNew = LexNode(self.wordIndex, self.word, self.sensenum, self.spos, self.ppos)
        for target, link in self.getAdjacentNodes():
            lnNew.linkTo(target, link)
        return lnNew
    def getMetaChains(self):
        return self.getAdjacentNodes()
    
    def getPos(self):
        return self.spos, self.ppos
    def getDist(self, other):
        return abs(self.spos - other.spos), abs(self.ppos - other.spos)

class LinkData:
    
    class Type:
        count = 7
        IDENT, SYN, HYPER, HYPO, SIBLING, TERM, OTHER  = xrange(count)
        @classmethod
        def validate(cls, val):  
            if not 0 <= val <= cls.count:   raise TypeError(str(val)+" is not a valid LinkData.Type")
            
    def __init__(self, lexDist=0, type=Type.OTHER):
        LinkData.Type.validate(type)
        
        self.lexDist = lexDist
        self.type = type
        
    def getLexDist(self):
        return self.lexDist
    
    def getType(self):
        return self.type
    
class LexGraph(object):
    
    class InputError(ValueError):
        pass
    
    def __init__(self, data=None, additionalTerms={}, wnMaxdist=3):
          
        self.reset()
        
        self.maxdist = wnMaxdist
    
        self.additionalTerms = additionalTerms
        
        if data:
            self.feedDocument(data)
    
    def reset(self):
        self.chains = {}
        self.words = defaultdict(set)
        self.wordInstances = []
        self.sentpos = self.parapos = self.wordpos = 0
        
        self.reduced = False
    
    def feedDocument(self, paragraphs, reset=True):
        self.reset()
        for para in paragraphs:
            self.feedParagraph(para)
    
    def feedParagraph(self, sentences):
        self.parapos += 1
        for sent in sentences:
            self.feedSentence(sent)
            
    def feedSentence(self, chunks):
        self.sentpos += 1
        if not chunks: return
        if isinstance(chunks[0], tuple):
            chunks = self._handleTaggedInput(chunks)
        for chunk in chunks:
            self._addWord(chunk)
            
    def computeChains(self):
        if not self.isReduced():
            self._reduceGraph()
        
        scoredChains = []
        for ch in self.chains.itervalues():
            score = self._scoreChain(ch)
            if score > 0:
                scoredChains.append((ch, score))
                
        return scoredChains
    
    def isReduced(self):
        return self.reduced
    
    @classmethod
    def chainsAsList(cls, scoredChains):
        return [[ln for ln, _ in ch.getAdjacentNodes()] for ch, _ in scoredChains]
    @classmethod
    def chainsAsRankedList(cls, scoredChains):
        return cls.chainsAsList(cls.chainsAsRanked(scoredChains))
    @classmethod
    def chainsAsRanked(cls, scoredChains):
        return sorted(scoredChains, key=lambda (k,v): v, reverse=True)
    
    def _handleTaggedInput(self, taggedWords):
        chunk = []
        lastPostag = None
        for wordpostag in taggedWords:
            try:
                word, postag = wordpostag
            except ValueError:
                raise LexGraph.InputError("POS-tagged input assumed - has to be of format [(token, POS), .... ]!" +
                                          " Current element was: %s"%(str(wordpostag)))
            if len(postag) == 0:
                raise LexGraph.InputError("Empty POS tag in input: %s"%(str(wordpostag)))
            "We look for combinations of adjectives and nouns"
            if postag[0] == 'N':
                chunk.append(word)
            elif postag == 'JJ' and len(chunk) == 0:
                chunk.append(word)
            elif len(chunk) > 0 and lastPostag[0] == "N":
                yield chunk
                chunk = []
            lastPostag = postag
        if chunk:
            yield chunk
        
    
    def _makeLink(self, ln, type, chain=None, lexDist=0):
        return LinkData(lexDist, type)
    
    def _addToChain(self, ln, senseOrToken=None, lexDist=0, type=LinkData.Type.IDENT):
        senseOrToken = ln.getId() if not senseOrToken else senseOrToken
        try:
            chain = self.chains[senseOrToken]
            link = self._makeLink(ln, type, chain, lexDist)
            chain.linkTo(ln, link)
           # log.debug("added "+str(ln)+" to chain "+str(chain))
        except KeyError:
            "A new chain always has to start with a node owning the chain (i.e. lexnode ID = chain ID)"
            "TODO discuss how this might affect coverage"
            if lexDist == 0:
                link = self._makeLink(ln, type, None, lexDist)
                self.chains[senseOrToken] = chain = MetaChain(senseOrToken)
                chain.linkTo(ln, link)
               # log.debug("created new chain for "+str(ln))
        
            
    def _addWord(self, word):
        self.wordpos += 1
        
        #log.debug("Adding "+str(word)+" at "+str(self.wordpos))
        wordSet = set()
        self.wordInstances.append(wordSet)
        
        for wnSense, term, dist, type in self._expandWord(word):
            if not wnSense:
                #id = self._idForUnknownLemma(term)
                if dist == 0:
                    ln = LexNode(self.wordpos, term, None, self.sentpos, self.parapos)
                    self._addToChain(ln)
                    wordSet.add(ln)
                else:
                    if term in self.chains:
                        assert ln
                        self._addToChain(ln, term, dist, type)
                        #log.info("Term connection between "+str(word)+" and "+str(term))
            else:
                if dist == 0:
                    "Another word sense: Create own LexNode"
                    ln = LexNode(self.wordpos, term, wnSense, self.sentpos, self.parapos)
                    wordSet.add(ln)
                    self._addToChain(ln)
                else:
                    assert ln
                    self._addToChain(ln, wnSense, dist, type)
        
        wordKey = list(wordSet)[0].getWord()
        self.words[wordKey].update(wordSet)
    def expandLst(self, lst, alreadySeen, word, dist, type):
        for synset in lst:
            if synset.offset not in alreadySeen:
                alreadySeen.add(synset.offset)
                firstLemmaInSynset = synset.lemmas()[0]
                yield synset.offset, firstLemmaInSynset.name().replace("_"," "), dist, type                
                    
    def _expandWord(self, word, maxDist=None, inclOtherRels=False):
        maxDist = maxDist if maxDist else self.maxdist
        if isinstance(word, list):
            headWord = word[-1]
            word = " ".join(word)
        else:
            headWord = word
        syns = wn.synsets(word.replace(" ","_"), "n") 
        if not syns and word not in self.additionalTerms:
            syns = wn.synsets(headWord, "n")
        if not syns:
            yield None, word, 0, LinkData.Type.IDENT
            relTerms = self.additionalTerms.get(word, None) or self.additionalTerms.get(headWord, None)
            if relTerms:
                for term in relTerms:
                    if term != word:
                        yield None, term, 1, LinkData.Type.TERM
        else:
            for syn in syns:
                yield syn.offset, word, 0, LinkData.Type.SYN
                alreadySeen = set()
                alreadySeen.add(syn.offset)
                
                hyperBases = [syn]
                hypoBases = [syn]
                for dist in range(1, maxDist):
                    newHypers = sum([h.hypernyms() for h in hyperBases], [])
                    newHypos = sum([h.hyponyms() for h in hypoBases], [])
                    for el in self.expandLst(newHypers, alreadySeen, word, dist, LinkData.Type.HYPER):
                        yield el
                    for el in self.expandLst(newHypos, alreadySeen, word, dist, LinkData.Type.HYPO):
                        yield el
                    if dist == 1:
                        for el in self.expandLst(sum([h.hyponyms() for h in newHypers], []), alreadySeen, word, dist, LinkData.Type.SIBLING):
                            yield el                    
                    hyperBases, hypoBases = newHypers, newHypos
                
                if inclOtherRels:
                    otherRels = [syn.instance_hypernyms, syn.instance_hyponyms, syn.also_sees, syn.member_meronyms, syn.part_meronyms, syn.substance_meronyms, syn.similar_tos, syn.attributes, syn.member_holonyms, syn.part_holonyms, syn.substance_holonyms]
                    for rel in otherRels:
                        for el in self.expandLst(rel(), alreadySeen, word, 1, LinkData.Type.OTHER):
                            yield el
    
    def _getRelBetweenNodes(self, ln1, ln2):
        if ln1.getWord() == ln2.getWord():    return LinkData.Type.IDENT
        if ln1.getSense() == ln2.getSense():    return LinkData.Type.SYN
        assert ln1.getId() in self.chains and ln2.getId() in self.chains
        ln1Chain = self.chains[ln1.getId()]
        ln2Chain = self.chains[ln2.getId()]
        try:    return ln1Chain[ln2].getType()
        except KeyError:
            try:    return ln2Chain[ln1].getType()
            except KeyError:    return None
    
    def _scoreLnk(self, ln, lnk, lnOther, lnkOther):
        raise NotImplementedError("To be implemented by subclasses")
    
    def _scoreChain(self, chain):
        if len(chain) <= 1: return 0
        score = 1.0
        owningNodeExists = False
        chainLst = chain.asList()
        if chainLst[0][0].getId() != chain.getId():   return 0
        for ind in xrange(len(chainLst)-1):
            ln, lnk = chainLst[ind]
            owningNodeExists = owningNodeExists or ln.getId() == chain.getId()
            lnOther, lnkOther = chainLst[ind+1]
            score += self._scoreLnk(ln, lnk, lnOther, lnkOther)
        if not owningNodeExists:
            return 0
        return score
    
    def _reduceGraph(self):
        raise NotImplementedError("To be implemented by subclasses")

class GalleyMcKeownChainer(LexGraph):
    def __init__(self, data=None, additionalTerms={}, wnMaxdist=3):
        LexGraph.__init__(self, data=data, additionalTerms=additionalTerms, wnMaxdist=wnMaxdist)
    
    def _disambiguate(self):
        wsdict = {}
        for word in self.words:
            dis = self._disambiguateWord(word)
            wsdict[word] = dis
        for word, lns in self.words.iteritems():
            for ln in lns:
                if wsdict[word].getSense() != ln.getSense():
                    #log.debug("Unlink "+str(ln))
                    ln.unlinkAll()
            self.words[word] = set([wsdict[word]])
    
    def _disambiguateWord(self, word):
        maxscore = -1
        maxsense = None
        #log.debug("Disambiguating "+str(word)+". Has senses: "+str(self.words[word]))
        for ln in self.words[word]:
            score = self._scoreNode(ln)
            if score > maxscore:
                maxscore, maxsense = score, ln
        #log.debug("    Chosen: "+str(maxsense))
        return maxsense
                
    def _scoreNode(self, ln):
        score = 0
        for chain, lnk in ln.getMetaChains():
            "For each LN in that chain"
            for otherLn, otherLnk in chain.getLexNodes():
                if otherLn.getWordIndex() == ln.getWordIndex():    continue
                score += self._scoreLnk(ln, lnk, otherLn, otherLnk)
        return score
    
    def _scoreLnk(self, ln, lnk, lnOther, lnkOther):
        sdist, pdist = ln.getDist(lnOther)
        return self._getScoreFromMatrix(self._getRelBetweenNodes(ln, lnOther), sdist, pdist)
        
    def _getScoreFromMatrix(self, rel, sd, pd):
        if rel == LinkData.Type.IDENT or rel == LinkData.Type.SYN:
            if sd <= 3: return 1
            return .5
        if rel == LinkData.Type.HYPER or rel == LinkData.Type.HYPO:
            if sd <= 1: return 1
            if sd <= 3: return .5
            return .3
        if rel == LinkData.Type.SIBLING:
            if sd <= 1: return 1
            if sd <= 3: return .3
            if pd <= 1: return .2
            return 0
        return 0
    
    def _reduceGraph(self):
        self._disambiguate()
        self.reduced = True
'''  
def demo():
    """ Computes and prints lexical chains in a sample text (taken from Galley/McKeown 2003) """
    from nltk.tag import pos_tag
    from nltk.tokenize import word_tokenize, sent_tokenize
    
    input = \'''Passages from spoken or written text have a quality of unity
    that arises in part from the surface properties of the text; 
    syntactic and lexical devices can be used to create a sense of 
    connectedness between sentences, a phenomenon known as textual cohesion
    [Halliday and Hasan, 1976]. Of all cohesion devices, lexical cohesion is
    probably the most amenable to automatic identification [Hoey, 1991]. 
    Lexical cohesion arises when words are related semantically, 
    for example in reiteration relations between a term and a synonym or superordinate. Lexical chaining is the process of connecting semantically
    related words, creating a set of chains that represent different threads of cohesion through the text. This intermediate representation of text has been used in many natural language processing applications, including automatic summarization [Barzilay and Elhadad, 1997; Silber andMcCoy, 2003], infor- mation retrieval [Al-Halimi and Kazman, 1998], intelligent spell checking [Hirst and St-Onge, 1998], topic segmentation [Kan et al., 1998], and hypertext construction [Green, 1998]
    \''' 
    input = input.replace("-\n","")
    input = sent_tokenize(input)
    input = [[pos_tag(word_tokenize(sent)) for sent in input]]
    #mc = GalleyMcKeownChainer(data=input)
    mc = SilberMcCoyChainer(data=input)
    chains = mc.computeChains()
    #print "Lexical chains according to Galley/McKeown"
    #print "\n".join([str((ch, score)) for ch, score in LexGraph.chainsAsRanked(chains) if len(ch) > 1])
    
if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
    demo()
'''    