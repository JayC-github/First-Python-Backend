> **General assumptions:**

- When testing one function, we assume all other functions behave as intended
- Other than errors defined all cases will be valid inputs
- All functions are working as specified in the specifications
- Tokens are unique for the same user each session
- User_ids are unique and same for each user
- If unsure what a wrong input is then put it in assumptions and place a dummy value
- Data will be reset every time a function is run
- Data types will be as specified in the project document
- Slackr owner will be considered to be the first registered user

---

> **Assumptions for auth functions:**

**general:**
- User can generate separate tokens in a separate session, and have 2 active tokens at the same time

**__auth_register:__**
- The provided function is used to check whether the email is valid/invalid
- Regular expression for validating an email will be: '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
- If the user has been registered successfully they will be considered to have been logged in
- Empty input in email address will be judged as an invalid email address
- If user registers with the same email address they will not receive a new u_id
- A handle is generated that is the concatentation of a lowercase-only first and last name
- If the concatenation is longer than 20 characters, it is cutoff at 20 characters 
- If the handle is already taken, handle will be modified to make it unique
- 「0」(zero, int) is not a valid value for a token.

**__auth_login:__**
- The generated user id from the same user should be the same with auth_register function, but the token outputs should be different and unique.
- There must be a database to check if the entered email belongs to a user or not

**__auth_logout:__**
- Users cannot logout before they have registered or logged in
- After logout, a token assigned to a user will expire and will not be valid

---


> **Assumptions for Channel(s) Functions:**

**__channel_details:__**
- An owner of a channel will show up under "all_member"


**__channel_invite:__**
- If an invitation is sent to a member of the channel, AccessError will be thrown
- When the owner of slackr is invited to the channel, they will automatically have ownership for the channel
- A member of the channel can send out invitation
- A user can be invited into a private channel

  
**__channel_messages:__**
- If a channel is empty, a call with start index 0 will return an empty message list.


**__channel_join:__**
- An invalid channel would be a channel that does not exist (no channel id) or a channel that the user is already a member of
- Admin refers to slackr owner 
- Owners will also be members


**__channel_leave:__**
- If user leaving is only member of channel then channel is removed


**__channel_addowner:__**
- When adding owners the user being added in does not have to be a member
- A valid channel id is one that is on the channel list 
- When user creates a channel with channel_create they are made the owner of that channel
- Slackowners do not have to belong to a channel to add users as owners

**__channel_removeowner:__**
- When removed as owner the user will become a regular member
- There must be at least 1 owner existing for a channel


**__channels_listall:__**
- channels_listall will show all channels, including the private channels

**__channels_list:__**
- The owner of slackr will be able to see channels that they have not joined

**__channels_create:__**
- When creating a channel, we assume that the name can be duplicated, however the channel_id must be unique

---


> **Assumptions for message:**


**__message_send:__**
- Slackr owner can send messages without being part of a channel

**__message_remove:__**
- Message ids are unique (throughout all channels)
- Query_str for search checks for all strings with query string within


**__message_edit:__**
- No input errors will exist (message_id will always be valid when this function is used)
- When message is edited only the text is changed and the uid and msg id remains the same
- When message edit content is '' it will delete the message

**__message_react:__**
- active react is for each user (1 user can have 1 active react tpe for a message)
- global react list?????
- all types of reacts will be stored in the message (where a react that hasnt been used with have empty u_id list
**__message_pinned:__**
- message pinned default to false

> **Assumptions for users:**

- users_all is required to output the users list even when called with an invalid token or no token.
- user_profile is required to output the users list even when called with an invalid token.


---
> **Assumptions for search:**


**__search:__**
- Searching an empty string search(token,'') will give list of all messages in channels that the user is part of







