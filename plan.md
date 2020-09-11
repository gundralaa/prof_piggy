# Prof. Piggy

## TextInput

### Description
A class that runs on a seperate thread that waits for input from 
a terminal and then analyzes the input to generate a monologue sentence

###  Methods
The module is run and when an ouput is produced should automatically send the monologue text to the monologue module. Therefore there will be a run and sync method.

* run(): starts the thread while waiting for user input. Once some text is typed in the nlp pipeline is applied upon the text to extract meaning from the sentence.

* match_pattern(text): returns the matched pattern type of the piece of text and returns a dict of the relevant parts of speech for creating the corresponding monologue text. Aspects such as the transitive verb and dobj or other parts of the sentence.

* generate_monologue(type, parts_of_speech): using the parts of speech dict and type, create a basic sentence that conveys the intent of the user within the perspective of the machine.

    * ex. 'Give me a new song' -> 'User wants a new song'

* post(): prints the new sentence on new line to the monogolgue thread or common monologue text based on monologue implementation.

### States

* types: every sentence has a type but mainly used to either make the distinction between a valid intent statement like a question or request vs a conversational answer which is not handled by the intent handler.

* parts_of_speech: the dep_ or tag_ label corresponding with certain key words within the sentence that define the intent of the sentence or the new information being conveyed into the monologue.

## VisionInput

### Description
A module used to run in parrallel with the text input thread that periodically checks camera input to extract relevant infromation about the surroundings.

### Methods

* run(): starts the camera thread

* detect_faces(): returns the presence of a person within the frame and the tag given to that person. If true also adds tracking to the entity in later frames or iterations

* detect_action(): if a presence is within the frame from a previous iteration, the users action is detected based on other objects within the frame or other systems
    * implementation sill needs some research

* post(): if presence or action has changed then print a basic monologue statement template

### States

* presence: defines who is in the frame if anyone and if not in frame for extended period of time changes presence.

* action: the current action of the user presence if any. If this state changes the system posts the new action and takes coresponding actions.

## Main

### Description
The main class that handles generating a cohesive monogloue using previously generated monoglogue sentances to create a cohesive stream of consiousenss. Method of implementation still unknown but could be some combinations of RNN and generative techniques.

### Methods
* run(): periodically checks the current state of the monologue file or shared data structure and generates new text for the data structure periodically based on previous entries.

* read_monologue(): returns the latest few lines of the monologue data structure.

* generate_line(): returns a new cohesive line for the monologue.

### State
* monologue: based on the thread implementation logs the history of the monologue produced by inputs and outputs.
* emotion_state: defines the bot's emotional state to figure out what actions will be taken, this also affects the monologue generation
* fatigue_state: defines the bot's ability to do more or rest based on how tired they are.

## OutputHandler
### Description
Checks the history of the internal monologue whenever a new line appears and then processes the new line to see if any action is needed to be taken. Lines that have intent directly are analyzed and run seperate from monologue. A sentience state store determines what actions are taken for what intent and when.

The output handler has its own output modules from text answer generation to searching, reading etc based on the actual action needed. Modules will be added

### Methods
* check_intent(): returns the intent type of the statement that is produced for the monologue which corresponds with a certain action

* decide_action(intent_type): analyze the intent type and decide the action_type

* perform_action(action_type): runs the corresponding module that will be running the action that is specified within the intent

## PrintOutput
### Description
Prints out generated statements of the bot as an action module

### Methods
print_statement(): prints the generated output based on the input into the output module. Based on implementation might use a basic concept and then generate a response using this concept or will use basic phrases.
