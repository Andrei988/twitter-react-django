# class Tweet():
#     id = 0
#     content = ""
#     image = ""

#     def __str__(self):
#         return self.id + '\n' + self.content

# tweet1 = Tweet()
# tweet2 = Tweet()
# tweet3 = Tweet()
# tweet4 = Tweet()

# tweet1.id = 1
# tweet1.content = "This is the 1 comment !!!"
# tweet2.id = 2
# tweet2.content = "This is the 2 comment !!!"
# tweet3.id = 3
# tweet3.content = "This is the 3 comment !!!"
# tweet4.id = 4
# tweet4.content = "This is the 4 comment !!!"

# tweetList = [tweet1, tweet2, tweet3, tweet4]    

# dictionaryTweetList = [{"id" : x.id, "content":x.content} for x in tweetList]

# print(tweetList)
# print()
# print(dictionaryTweetList)
# print()
# dictionaryTweetList[0].id = 3
# print(dictionaryTweetList[0].__class__)
# print()
# print(dictionaryTweetList[1])