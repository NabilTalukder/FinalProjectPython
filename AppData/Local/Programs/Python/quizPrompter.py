from openai import OpenAI
import socket


#initialise API key and client
OPENAI_API_KEY = open("C:\\Users\\Nabil\\AppData\\Local\\Programs\\Python\\OPENAI_API_KEY.txt", "r").read()
client = OpenAI(api_key = OPENAI_API_KEY)

def generateQuiz(qgi):

  prompt = '''Create a multiple choice quiz with 3 questions.
  The first line should say exactly: Multiple Choice Quiz.
  Every question should be listed like so: #X: Q where X is replaced by the question number and Q is the question.
  There should be 4 options, where each option should be listed like so: Y) where Y is a capital letter, in alphabetical order to distinguish the options.
  The answer to each question should be written under the last option of each question like so: Answer: Z) A 
  where Z is the letter corresponding to the answer and A is the answer text, matching exactly the text in the corresponding option.
  Create the quiz based on the information in the following text:''' +  qgi

  #instruct system how to behave and then prompt to generate quiz
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a question generator designed to give multiple choice questions based on inputted text."},
      {"role": "user", "content": prompt}
    ]
  )

  print(completion.choices[0].message.content)
  #return "#" so Java client knows end of message reached
  #and "\n" so Java client can read this output as lines using the BufferedReader
  return str(completion.choices[0].message.content) + "#\n"

#initialise server socket and wait for Java client to connect
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("localhost", 3007))
serverSocket.listen()
print("server listening ", str(3007))

while True:
    clientSocket, address = serverSocket.accept()
    print("Server connected client ", address)
    
    #receive input from Java client 
    print("awaiting request")
    data = clientSocket.recv(1024)
    if not data:
       continue
    print("received quizGenInput")
    #generate quix from user inputted text and send output back to client
    quizGenOutput = generateQuiz(data.decode())
    clientSocket.send(quizGenOutput.encode())
    print("sent")