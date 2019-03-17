# sammy
Yet Another Python Discord Bot\
## Functionality
Sammy is a basic discord bot made as a useful learning project.\
Right now the functionality is pretty barebones.\
It can sends messages in regular intervals (via autobumper() function, which can be treated as a template)\
It also autoresponds for some substrings in a message and there is a template for autoresponding on messages equal to a given string.

## memo
The biggest functionality right now is a per-user memo command, which reacts on a message formatted in a given way:\
`!memo YYYY-MM-DD HH:MM memo_content`\
Memos are not persistent yet.\
There's also a `!memo_get` command which returns all the memos in queue for a given user.
