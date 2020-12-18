import math, numpy as np

################################################################################

#    Problem 1 (25 pts)
#
#    Up to 5 points will be awarded for making progress toward a correct
#    solution.
#
#    Assume you are given a list of filenames of text files. Assume
#    that the text files only contain the punctuation
#    [".", ",", "!", "?", "-"].
#    The files may also contain the newline character "\n".

def get_words(content):
    '''
    Gets all whitespace- or punctuation-separated words from a string.
    '''
    # Replaces all punctuation and newlines with whitespace
    for punc in [".", ",", "!", "?", "-", "\n"]:
        content = content.replace(punc, " ")
    # Returns the lowercase list of words
    return content.lower().split()

def get_frequency(words):
    '''
    Gets a word-frequency object from a list of words.
    '''
    freq = {}
    for word in words:
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1
    return freq

def get_most(freq):
    most = {"word": "", "frequency": 0}
    for entry in freq:
        if(freq[entry] > most["frequency"]):
            most = {"word": entry, "frequency": freq[entry]}
    return most

def most_common_frequent_word(files):
    frequency = {}
    most = {}
    for path in files:
        frequency[path] = {}
        with open(path, "r", encoding="utf-8") as file:
            words = get_words(file.read())
            frequency[path] = get_frequency(words)
            most[path] = get_most(frequency[path])
    vmost = 0
    for file in most:
        if(most[file]["frequency"] > vmost):
            amost = most[file]["word"]
            vmost = most[file]["frequency"]
            pmost = file
    # print(f"Most is '{amost}', with {vmost} entries in '{pmost}'.")
    return amost

################################################################################

#    Problem 2 (20 pts)
#
#    This problem will be auto-graded.
#
#    Recall that links in an html file are given in the format
#    <a href = "http://engsci.utoronto.ca">EngSci homepage</a>
#    Write a function that takes in the text of an html file, and returns a dictionary
#    whose keys are the link texts (e.g. "EngSci homepage") and whose values are
#    the corresponding URLs (e.g., "http://engsci.utoronto.ca"). You can assume
#    that link texts do not repeat.
#    Sample call:
#     get_links('<a href = "http://engsci.utoronto.ca">EngSci homepage</a>')
#    should return {"EngSci homepage": "http://engsci.utoronto.ca"}

def get_link_tags(html_text):
    '''
    Find all link tags in an HTML text
    '''
    tagstarts = []
    tagends = []
    for i in range(len(html_text)-1):
        if html_text[i:i+2].lower() == "<a":
            tagstarts.append(i)
        elif html_text[i:i+2].lower() == "/a":
            tagends.append(i+2)
    tags = []
    for tag in range(len(tagstarts)):
        tags.append(html_text[tagstarts[tag]:tagends[tag]+1])
    return tags

def parse_tag(tag):
    '''
    Parse a link tag into its elements
    '''
    tag = str(tag)
    firstEnd = tag.index('>')
    firstQuote = tag.index('"')
    return {tag[firstEnd+1:tag.index('<', firstEnd+1)]: tag[firstQuote+1:tag.index('"', firstQuote+1)]}

def get_links(html_text):
    '''
    Assumes links are formatted exactly as: <a href = "link">title</a>
    '''
    links = {}
    for tag in get_link_tags(str(html_text).replace("\n", "")):
        links.update(parse_tag(tag))
    return links

###############################################################################

#   Problem 3 (10 pts)
#
#    Without using for-loops or while-loops, write  function for which
#    the tight asymptotic bound on the runtime complexity is O((n^2)*log(n)).
#    You may create helper functions, as long as they also do not use while-
#    and for-loops.
#    Justify your answer in a comment. The signature of the function must be

# k*(n^2)*log(n)
def f(n):
    if(n < 1):
        return
    else:
       f(n/2)



##############################################################################


###############################################################################
#  Problem 4 (15 pts)
#
#  This problem will be auto-graded.
#
#  It is possible to combine the numbers 1, 5, 6, 7 with arithemtic operations
#  to get 21 as follows: 6/(1-5/7).
#
#  Write a function that takes in a list of three numbers and a target number, and
#  returns a string that contains an expression that uses all the numbers
#  in the list once, and results in the target. Assume that the task is possible
#  without using parentheses.
#
#  For example, get_target_noparens([3, 1, 2], 7) can return "2*3+1" or "1+2*3"
#  (either output would be fine).

def get_all_single_ops(nums):
    ops = []
    # nums = list(nums)
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            ops.extend({"exp":f"{nums[i]}+{nums[j]}", "params":[i,j]})
            ops.extend({"exp":f"{nums[i]}-{nums[j]}", "params":[i,j]})
            ops.extend({"exp":f"{nums[j]}-{nums[i]}", "params":[i,j]})
            ops.extend({"exp":f"{nums[i]}*{nums[j]}", "params":[i,j]})
            if(nums[j] != 0):
                ops.extend({"exp":f"{nums[i]}/{nums[j]}", "params":[i,j]})
            if(nums[i] != 0):
                ops.extend({"exp":f"{nums[j]}/{nums[i]}", "params":[i,j]})
    return nums

def get_op_combinations(nums, exps=[]):
    if(len(exps) == 0):
        exps.extend([str(n) for n in nums])
    for exp in exps:
        exp = str(num)
        newnums = nums
        newnums.remove(num)
        return exp.extend(exps)

def get_target_noparens(nums, target):
    # expression.extend(ops[0])
    # expression.extend(ops[1]) IF not (ops0 is +- and ops1 is */)

################################################################################
#  Problem 5 (15 pts)
#
#  Up to 3 pts will be awarded for making progress toward a solution.
#
#  Now, write the function get_target which returns a string that contains an
#  expression that uses all the numbers in the list once, and results in the
#  target. The expression can contain parentheses. Assume that the task is
#  possible.
#  For example, get_target([1, 5, 6, 7], 21) can return "6/(1-5/7)"

def get_target(nums, target):
    pass

# See partial work in problem 4.

################################################################################

if __name__ == "__main__":
    # most_common_frequent_word(["exams/lorem1.txt", "exams/lorem2.txt"])
    # with open("exams/webpage.html", "r") as file: 
    #     print(get_links(file.read()))
    n = 100000
    f(n)
    print(f"{n} : {steps}")
        