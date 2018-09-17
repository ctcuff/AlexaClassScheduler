# AlexaClassScheduler
If you're as lazy as I am (which is probably impossible), you'll know how much of a pain it is to have to remember what classes you have on what day. AlexaClassScheduler is an Alexa skill that'll keep track of your classes so you won't have to.

# How does it work?
Classes are stored in an online database using [DynamoDB](https://aws.amazon.com/dynamodb/). When a user asks Alexa to add a class to their schedule, once the conversation is finished, the name of the class, the dates it occurrs on, and the times are added to a table in the db. From there, and depending on what the user asks, Alexa either reads from the table, updates values from the table, or deletes values from the table. Here's what a sample table looks like:

Class name | Days                              | Start time | End time
-----------|-----------------------------------|------------|----------
Biology    | ["monday", "wednesday", "friday"] | 12:00      | 1:30
Psychology | ["tuesday", "thursday"]           | 9:30       | 10:45
Physics    | ["tuesday"]                       | 7:30       | 10:20

# How do I build this myself?
0. Head over to the [Amazon dev site](https://developer.amazon.com/) and create a developer account if you haven't already done so.
1. Head over to Amazon's [DynamoDB site](https://aws.amazon.com/dynamodb/), create an account if you haven't already, then create a table similar to the one above (all values are stored as strings, except for days, which is stored as an array of strings).
2. Take note of the Access Key and Access Key Secret you hopefullygot from step 1 and create `keys.py` in the `src` directory. It should look **exactly** like this:
```python
# ../src/keys.py
ACCESS_KEY_ID = 'some value here'
SECRET_ACCESS_KEY = 'some secret value here'

```
3. Assuming you know how to upload an Alexa skill, once you've down steps 0 - 2, this should be ready to use. If you're not familiar with uploading an Alexa skill follow [this link](https://developer.amazon.com/alexa-skills-kit/alexa-skill-python-tutorial) for a quick 4. minute tutorial or [this link](https://chatbotsmagazine.com/how-to-develop-an-alexa-skill-in-under-10-minutes-8f288e26ba29) if you're like me and got nowhere fast from the first link.
4.5 As a bonus, you can run [zip.py](https://github.com/ctcuff/AlexaClassScheduler/blob/master/zip.py) to package the source of the skill into a zip file and upload the resulting zip file into AWS Lambda.

# Sample conversation
### Viewing your schedule

**User**: "Alexa, ask class scheduler to show me my schedule."

**Alexa**: "You have two classes today, Physics, which starts at 9:30 and Biology, which starts at 1:20"

### Adding classes

**User**: "Alexa, add Psychology to my schedule."

**Alexa**: "Alright, I'll add Psychology to your schedule, what time does Psychology start?"

**User**: "Twelve o'clock."

**Alexa**: "What time does Psychology end?"

**User**: "One thirty."

**Alexa**: "On what days does Psychology occurr?"

**User**: "Tuesdays and Thursdays."

**Alexa**: "Alright, you've told me that psychology starts at 12:00, ends at 01:30, and occurs on Tuesdays and Thursdays. Is this correct?"

**User**: "Yes."

**Alexa**: "Ok, I've added psychology to your schedule."

Note that there are a few more conversation options available than what's listed. For example, Alexa will warn you when you're about to add a class that's already been added and will just update that class if you can continue. To view more specifically what starts a conversation, take a look at [Intents.json](https://github.com/ctcuff/AlexaClassScheduler/blob/master/speech/Intents.json).
