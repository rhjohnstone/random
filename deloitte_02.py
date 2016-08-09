# Solution for 2nd Deloitte programming challenge thing.

# This script must be run from the same directory containing vigenere.py.
# This script ignores numbers in the ciphertext and treats all letters as lowercase when decoding.

# The hint tells us to use the previous challenge's solution, which is 141, to find a keyword also from the previous challenge.
# When doing this, it seems we have to include a lone hyphen as a word.
# Excluding the hyphen, "what" is the 141st word.
# Including the hyphen, "tactic" is the 141st word (and turns out to be the word we want).
# Also, the last letter of the ciphertext was incorrectly capitalised; the solution requires it to be lowercase. However, I've left it as it was here since it doesn't affect the code's output.

from vigenere import Vigenere

page_text = r"In Forensic Technology complex problem solving is a large part of our day-to-day work. Paying homage to our fondness of brain-teasers, we're launching a monthly Forensic Technology Challenge - a new series of logical, analytical and coding problems that put into practice the STEM, finance and technology skills essential to our work. Every month we'll post a new challenge created by the Forensic Technology team, focusing on one of these skills. You can solve these problems in any way that you want. We're looking forward to seeing the different ways that you approach them! Without further ado, here is the first challenge straight from the Forensic Technology hive-mind: Of the first 2016 prime numbers, which ones have digits that sum to 13? Our solution involved creating a Python script to do all of the heavy-lifting, but this is only one tactic. What was your method? We'll be posting how we solved this next month, along with Challenge #2. Don't forget to look out for our bonus question next week! If you are someone who enjoys problem-solving, logical thinking and technology, check out our Forensic Technology graduate professional roles to see if they are the right fit. What's the answer? Here's what you've been waiting for, the solutions to the first #4TechChallenge posted last month as well as the answer to the bonus question. So without further ado here is the Python script we used to generate the list of primes and subsequently find how many had their digits sum to a specified total."

previous_solution = 141

page_text = page_text.split()
#page_text.remove('-') # I originally removed the lone hyphen
keyword = page_text[previous_solution-1].lower()
print "Keyword =", keyword

ciphertext = 'rowmcdxRztjNT7US9D'
cipher = Vigenere()
plaintext = cipher.decode(ciphertext,keyword)

print "Decoded text (lowercase and excluding numbers):", plaintext
