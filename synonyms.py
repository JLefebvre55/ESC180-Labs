import math

def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    t = sum([vec1[i]*vec2[i] for i in set(vec1).intersection(set(vec2))])
    j = sum([vec1[i]**2 for i in vec1])
    k = sum([vec2[i]**2 for i in vec2])
    return t/math.sqrt(j*k)


def build_semantic_descriptors(sentences):
    semdesc = {}
    i = 0
    for sentence in sentences:
        #Only concerned with number of SENTENCES IN COMMON, does not include repetition per sentence
        for word in set(sentence):
            if not word in semdesc:
                i+=1
                # if i %10000 == 0:
                #     print(f"{i} unique words catalogged...")
                semdesc[word] = {w:1 for w in set(sentence).difference({word})}
            else:
                for w in set(sentence).difference({word}):
                    if not w in semdesc[word]:
                        semdesc[word][w]=1
                    else:
                        semdesc[word][w]=semdesc[word][w]+1
    return semdesc

def build_semantic_descriptors_from_files(filenames):
    semdesc = {}
    for filename in filenames:
        with open(filename, "r", encoding="utf-8") as file:
            s = file.read().lower()
            #Remove unnecessary punctuation - including wierd utf-8 nonsense - while preserving contractions, replace sentence-ending punct. with "."
            for punc in [",", "-", "--", ":", ";", "_", "*", "(", ")", '"', "\n", "“", " ‘", " '", "' ", "‘ ", "”", " ’", "’ ", "—"]:
                s = s.replace(punc, " ")
            for punc in ["?", "!", "....", "..."]:
                s = s.replace(punc, ".")
            #Split text into sentences via "."
            sentences = s.split(".")
            #Split sentences into words, removes those little in betweeners
            sentences = [[word for word in sentence.split() if word != ""] for sentence in sentences]
                
            #Build semdesc
            new_semdesc = build_semantic_descriptors(sentences)
            #Combine the new with the old
            for word in new_semdesc:
                if not word in semdesc:
                    semdesc[word] = new_semdesc[word]
                else:
                    for entry in new_semdesc[word]:
                        if not entry in semdesc[word]:
                            semdesc[word][entry] = new_semdesc[word][entry]
                        else:
                            semdesc[word][entry] = semdesc[word][entry]+new_semdesc[word][entry]
            file.close()
    return semdesc

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    largest = choices[0]
    largest_sim = -1
    for choice in choices:
        if (not word in semantic_descriptors) or (not choice in semantic_descriptors):
            continue
        val = similarity_fn(semantic_descriptors[word], semantic_descriptors[choice])
        if val > largest_sim:
            largest = choice
            largest_sim = val
    return largest


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    correct = 0
    total = 0
    with open(filename, "r", encoding="utf-8") as file:
        for test in file.readlines():
            q = test.lower().replace("\n", "").split()
            total +=1
            sim = most_similar_word(q[0], q[2:], semantic_descriptors, similarity_fn)
            if sim == q[1]:
                correct +=1
    return 100.0*correct/total

if __name__ == "__main__":
    # dict1 = {"i": 3, "am": 3, "a": 2, "sick": 1, "spiteful": 1, "an": 1, "unattractive": 1}
    # dict2 = {"i": 1, "believe": 1, "my": 1, "is": 1, "diseased": 1}
    # print(cosine_similarity(dict1, dict2))
    # print(cosine_similarity({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6}))
    
    # sentences = [["i", "am", "a", "sick", "man"],
    #             ["i", "am", "a", "spiteful", "man"],
    #             ["i", "am", "an", "unattractive", "man"],
    #             ["i", "believe", "my", "liver", "is", "diseased"],
    #             ["however", "i", "know", "nothing", "at", "all", "about", "my",
    #             "disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]
    # print(build_semantic_descriptors(sentences)["man"])
    semdesc = build_semantic_descriptors_from_files(["wp.txt", "sw.txt"])
    res = run_similarity_test("test.txt", semdesc, cosine_similarity)
    print(res, "of the guesses were correct")