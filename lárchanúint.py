import re


CONSONANTS = "bcdfghjklmnpqrstvwxyz-"
VOWELS = "aeiouáéíóúʹ"
adhWarning = False
# /ʹau/ before consonant ea(?:bh|dh|gh|mh)([bcdfghjklmnpqrstvwxyz])
# /au/ before consonant (?:a|o)(?:bh|dh|gh|mh)([bcdfghjklmnpqrstvwxyz])

# /ʹauʹ/ ea(?:bh|dh|gh|mh)ai
# /ʹau/ ea(?:bh|dh|gh|mh)a
# /auʹ/ (?:a|o)(?:bh|dh|gh|mh)ai
# /au/ (?:a|o)(?:bh|dh|gh|mh)a

# /auə/ (?:a|ea|o)(?:bh|dh|gh|mh)adh
# /auiː/ (?:a|ea|o)(?:bh|dh|gh|mh)aidh


# /ʹaiʹ/ before consonant ei(?:gh|dh)([bcdfghjklmnpqrstvwxyz])
# /ʹai/ before consonant ea(?:gh|dh)([bcdfghjklmnpqrstvwxyz])
# /aiʹ/ before consonant (?:oi|ai)(?:gh|dh)([bcdfghjklmnpqrstvwxyz])
# /ai/ before consonant a(?:gh|dh)([bcdfghjklmnpqrstvwxyz])

# /ʹaiʹ/ (?:ei|ea)(?:gh|dh)(?:ai|i)
# /ʹai/ (?:ei|ea)(?:gh|dh)(?:ea|a)
# /aiʹ/ (?:oi|ai|a)(?:gh|dh)(?:i|ai)
# /ai/ (?:oi|ai|a)(?:gh|dh)(?:ea|a)
def au(sounds):
    if re.sub(r"(?:o(?:v|ɣ)|av)([bcdfghjklmnpqrstvwxyz])", r"au\1", sounds):
        sounds = re.sub(r"(?:o(?:v|ɣ)|av)([bcdfghjklmnpqrstvwxyz])", r"au\1", sounds)
    if re.sub(r"(?:o(?:v|ɣ)|av)(?:ə)", r"au", sounds):
        sounds = re.sub(r"(?:o(?:v|ɣ)|av)(?:ə)", r"au", sounds)
    return sounds

def ai(sounds): #TODO: faigh etc
    if re.sub(r"(?:[oea](?:ɣʹ|vʹ)|aɣ)([bcdfghjklmnpqrstvwxyz])", r"ai\1", sounds):
        sounds = re.sub(r"(?:[oea](?:ɣʹ|vʹ)|aɣ)([bcdfghjklmnpqrstvwxyz])", r"ai\1", sounds)
    if re.sub(r"(?:[oea](?:ɣʹ|vʹ)|aɣ)ə", r"ai", sounds):
        sounds = re.sub(r"(?:[oea](?:ɣʹ|vʹ)|aɣ)ə", r"ai", sounds) 
    return sounds 
def finalIdh(sounds):
    if re.sub(r"əɣʹ$", r"iː", sounds):
        sounds = re.sub(r"əɣʹ", r"iː", sounds)
    return sounds

def finalAdh(sounds):
    # consider verbal noun vs saorbhriathar endings
    if re.sub(r"əɣ$", r"ə", sounds):
        sounds = re.sub(r"əɣ$", r"ə", sounds)
    return sounds, True

def initialR(sounds):
    if re.sub(r"^rʹ", r"r", sounds):
        sounds = re.sub(r"^rʹ", r"r", sounds)
    return sounds

def checkForFVerbEnding(sounds):
    if re.sub(r"(?:f|fʹ)(əɣʹ|ənʹ|əmʹədʹ|əmʹiːsʹ|ədʹiːsʹ)", r"h\1", sounds):
        sounds = re.sub(r"(?:f|fʹ)(əɣʹ|ənʹ|əmʹədʹ|əmʹiːsʹ|ədʹiːsʹ)", r"h\1", sounds)
    if re.sub(r"(?:f|fʹ)əɣ", r"həx", sounds) is not sounds:
        sounds = re.sub(r"(?:f|fʹ)əɣ", r"həx", sounds)
    return sounds

def devoice(sounds): #TODO: these loops are needless and inefficient
    for cluster, devoiced in zip([r"bh", r"dh", r"gh", r"vh", r"kh", r"ph", r"th", r"sh"], [r"p", r"t", r"k", r"f", r"k", r"p", r"t", r"s"]):
        if re.sub(cluster, devoiced, sounds):
            sounds = re.sub(cluster, devoiced, sounds)
    return sounds

def checkForLenition(letters):
    #TODO: Add exception for Sheo-, Sheó-, Shiú-, and Sheáin
    for cluster, lenited in zip([r"bh", r"ch", r"dh", r"fh", r"gh", r"mh", r"sh", r"th"], [r"v", r"x", r"ɣ", r"", r"ɣ", r"v", r"h", r"h"]):
        if re.sub(cluster, lenited, letters):
            letters = re.sub(cluster, lenited, letters)
    return letters
def checkForEclipsis(letters):
    for cluster, eclipsed in zip([r"mb", r"gc", r"nd", r"bhf", r"ng", r"bp", r"dt", r"n-"], [r"m", r"g", r"n", r"v", r"ŋ", r"b", r"d", r"n"]):
        if re.sub(cluster, eclipsed, letters):
            letters = re.sub(cluster, eclipsed, letters)
    return letters
def checkForConsonantClusters(letters):
    for double, single in zip([r"nn", r"ll"], [r"n", r"l"]):
        if re.sub(double, single, letters):
            letters = re.sub(double, single, letters)
    return letters

def checkForVowelClusters(letters, stressed): #TODO: Looping here is kind of a mess / Actually maybe it's fine? / account for tríú or séú
    for cluster in [r"uío", r"aío", r"aoi", r"uí", r"aí", r"ao", r"ío", r"í"]:
        if re.sub(cluster, r"iː", letters) is not letters:
            return re.sub(cluster, r"iː", letters)
    for cluster in [r"eái", r"eá", r"ái", r"á"]:
        if re.sub(cluster, r"aː", letters) is not letters:
            return re.sub(cluster, r"aː", letters)
    for cluster in [r"aei", r"ae", r"éa", r"éi", r"é"]:
        if re.sub(cluster, r"eː", letters) is not letters:
            return re.sub(cluster, r"eː", letters)
    for cluster in [r"eoi", r"eo", r"ói", r"ó"]:
        if re.sub(cluster, r"oː", letters) is not letters:
            return re.sub(cluster, r"oː", letters) #TODO: exceptions
    for cluster in [r"iúi", r"úi", r"iú", r"ú"]:
        if re.sub(cluster, r"uː", letters) is not letters:
            return re.sub(cluster, r"uː", letters)
    for cluster in [r"iai", r"ia"]:
        if re.sub(cluster, r"iə", letters) is not letters:
            return re.sub(cluster, r"iə", letters)
    for cluster in [r"uai", r"ua"]:
        if re.sub(cluster, r"uə", letters) is not letters:
            return re.sub(cluster, r"uə", letters)
    if stressed is True:
        for cluster in [r"ea", r"ai"]:
            if re.sub(cluster, r"a", letters) is not letters:
                return re.sub(cluster, r"a", letters)
        for cluster in [r"ei"]:
            if re.sub(cluster, r"e", letters) is not letters:
                return re.sub(cluster, r"e", letters)
        for cluster in [r"io", r"ui"]:
            if re.sub(cluster, r"i", letters) is not letters:
                return re.sub(cluster, r"i", letters)
        for cluster in [r"oi"]:
            if re.sub(cluster, r"o", letters) is not letters:
                return re.sub(cluster, r"o", letters)
        for cluster in [r"iu"]:
            if re.sub(cluster, r"u", letters) is not letters:
                return re.sub(cluster, r"u", letters)
    else:
        for cluster in [r"ea", r"ai", r"ui", r"ei", r"oi", r"io", r"iu", r"a", r"i", r"e", r"o", r"u"]:
            if re.sub(cluster, r"ə", letters) is not letters:
                return re.sub(cluster, r"ə", letters)
    return letters

def slenderConsonants(letters, initial=False): # rʹ(d|n|l|t|s)ʹ
    if re.sub(r"([bcdfghjklmnpqrstvwxyz])", r"\1ʹ", letters):
        letters = re.sub(r"([bcdfghjklmnpqrstvwxyzɣ])", r"\1ʹ", letters)
    if re.sub(r"rʹ(d|n|l|t|s)ʹ", r"r\1ʹ", letters): # r exceptions
        letters = re.sub(r"rʹ(d|n|l|t|s)ʹ", r"r\1ʹ", letters)
    if initial:
        if re.sub(r"sʹ(f|m|p)ʹ", r"s\1ʹ", letters):
            letters = re.sub(r"^sʹ(f|m|p)ʹ", r"s\1ʹ", letters)
    return letters




def lettersToSounds(group):
    letters = group.letters
    # print("current letters: " + letters)
    if isinstance(group, ConsonantGroup):
        if group.initial:
            letters = checkForEclipsis(letters)
        letters = checkForLenition(letters)
        if re.sub(r"c", r"k", letters):
            letters = re.sub(r"c", r"k", letters)
        for double, single in zip([r"nn", r"ll"], [r"n", r"l"]):
            if re.sub(double, single, letters):
                letters = re.sub(double, single, letters)
        if group.slender:
            letters = slenderConsonants(letters, group.initial) #TODO: this needs to change, right now it takes group which doesn't  have changes of previous bits

    else:
        letters = checkForVowelClusters(letters, group.stressed)
    return letters

def processSounds(sounds):
    adhWarning = False
    sounds = au(sounds)
    #print("sounds after au " + sounds)
    sounds = ai(sounds)
    sounds = checkForFVerbEnding(sounds)
    sounds = finalIdh(sounds)
    #print("Sounds are: " + sounds)
    sounds, adhWarning = finalAdh(sounds)
    sounds = initialR(sounds)
    sounds = devoice(sounds)
    return sounds, adhWarning

class Word(object):
    """docstring for Word"""
    def __init__(self, spelling):
        self.spelling = spelling
        self.groups = []
        lastGroup = None
        currentGroup = None
        currentGroupText = ""
        isCheckingForConsonant = True
        wasStressApplied = False
        for letter in self.spelling:
            currentType = CONSONANTS if isCheckingForConsonant else VOWELS
            if letter in currentType:
                currentGroupText += letter
            else:
                if isCheckingForConsonant:
                    currentGroup = ConsonantGroup(currentGroupText) 
                else:
                    if wasStressApplied == False:
                        currentGroup = VowelGroup(currentGroupText, True)
                        wasStressApplied = True
                    else: 
                        currentGroup = VowelGroup(currentGroupText)
                self.groups.append(currentGroup)
                if lastGroup is not None:
                    lastGroup.next = currentGroup
                currentGroupText = letter
                lastGroup = currentGroup

                isCheckingForConsonant = not isCheckingForConsonant
        if isCheckingForConsonant:
            currentGroup = ConsonantGroup(currentGroupText)
            self.groups.append(currentGroup)
            lastGroup.next = currentGroup
        else:
            currentGroup = VowelGroup(currentGroupText)
            self.groups.append(currentGroup)
            lastGroup.next = currentGroup
        if isinstance(self.groups[0], ConsonantGroup):
            if self.groups[1].initialSlender:
                self.groups[0].slender = True

        for group in self.groups:
            if isinstance(group, VowelGroup) and group.endingSlender and group.next:
                    group.next.slender = True
                    #print(group.next.letters)
        self.groups[0].initial = True
        self.groups[-1].final = True

# Array of VowelGroup and ConsonantGroup objects
class LetterGroup():
    def __init__(self, letters):
        self.letters = letters
        self.sounds = None
        self.next = None
        self.previous = None
        self.initial = False
        self.final = False

class VowelGroup(LetterGroup):
    def __init__(self, letters, stressed=False):
        super().__init__(letters)
        self.stressed = stressed
        self.initialSlender = True if letters[0] in "íéieʹ" else False
        self.endingSlender = True if letters[-1] in 'íiʹ' else False
        #print("endingSlender = " + str(self.endingSlender))
            
class ConsonantGroup(LetterGroup):
    def __init__(self, letters, slender=False):
        super().__init__(letters)
        self.slender = slender


testword = Word("seirbhís")
testsounds = []
for group in testword.groups:
    #print("group letters: "+ group.letters)
    testsounds.append(lettersToSounds(group))
#print(testword.spelling)
#print("".join(testsounds))
#print(processSounds("".join(testsounds)))

while True:
    word = Word(input("Please enter a word for phonetic transcription:\n"))
    testsounds = []
    for group in word.groups:
        testsounds.append(lettersToSounds(group))
    processed, adhWarning = processSounds("".join(testsounds))
    print("/" + processed + "/")
    if adhWarning:
        print("**The word you entered could be a verbal noun or a past tense verb in the autonomous form, if it is a verbal noun, replace /ə/ with /əx/**\n")
