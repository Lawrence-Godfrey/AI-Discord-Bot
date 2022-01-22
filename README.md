# AI Discord Bot
## A Discord bot for the interacting with various AI models. 
### GPT-3
There are a number of commands which allow a user to interact with the [GPT-3](https://en.wikipedia.org/wiki/GPT-3) model. These commands use a hardcoded "seed text" which sets the context for the GPT-3 model. 
For example, if a user uses the /clue command, the bot will set up a context using a set of examples of crossword clues and their corresponding answers before inserting the clue given by the user.
#### Commands
 - `/clue`: Given a clue and the length the answer should be, the bot will respond with the predicted answer to the clue. 
    
 - `/chat`: Have a conversation with the GPT-3 bot.    
    
 - `/summarize`: Given a text, the bot will summarize the text.    
    
 - `/QandA`: Given a question, the bot will respond with the answer to the question.    
### StyleGAN2
The `/thispersondoesnotexist` command gets a random image from [thispersondoesnotexist.com](https://thispersondoesnotexist.com/). This site generates images using the StyleGAN2 model, which is a type of GAN (Generative Adversarial Network). This model is trained to produce completely new images based on a set of random input parameters. In this case the model generates images of faces, i.e., faces of people which don't exist. 

### Image Classification with EfficientNet
By posting an image in any channel which the bot has access to, and including the text "predict" in the body of the message, the bot will make a prediction of the image using the pretrained [EfficientNetB6](https://paperswithcode.com/method/efficientnet#:~:text=EfficientNet%20is%20a%20convolutional%20neural,resolution%20using%20a%20compound%20coefficient.&text=EfficientNet%20uses%20a%20compound%20coefficient%20to%20uniformly%20scales%20network%20width,resolution%20in%20a%20principled%20way). model. 
This model takes in a 528x528 image and outputs a vector of probabilities for each of the 1000 classes in the ImageNet dataset. 

## Usage 
To use this bot on your own server you will need to [create a Discord bot](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/) and configure it to allow slash commands (`applications.commands` in OAuth2 settings), as well as some other permissions it will need to read and send messages, etc. 
Once it's created you will need to add the bot token to the .env file.
For the bot to be able to interact with the GPT-3 API you will need to [sign up to OpenAI](https://openai.com/api/) and get a token, which you can add to the .env file.