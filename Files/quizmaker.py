"""
Quiz Maker - Make an application which takes various questions form a file, picked randomly, and puts together a
quiz for students. Each quiz can be different and then reads a key to grade the quizzes.
"""
import random


class Question:
    def __init__(self, qid, text, mark, answer):
        """
        Class constructor

        qid:    Integer - The question unique id
        text:   String  - The question text
        mark:   Double  - The question mark
        answer: Answer  - An instance of Answer for the question
        """
        self.id = int(qid)
        self.text = text
        self.answer = answer
        self.mark = float(mark)


class Answer:
    def __init__(self, answer):
        """
        Class constructor

        answer: String  - The correct answer for a question
        """
        self.answer = answer

    def is_correct(self, answer):
        """
        Whether or not an answer is correct

        answer: String - An answer text from a user input
        returns: Boolean
        """
        return answer.lower() == self.answer.lower()


class UserAnswer:
    def __init__(self, question, answer):
        """
        Class constructor

        question:   Question    - The question the user is attempting to answer
        answer:     String      - The user answer
        """
        self.question = question
        self.answer = answer

        # Process user answer on the question
        self.mark = 0
        if self.question.answer.is_correct(self.answer):
            self.mark = self.question.mark

    def is_correct(self):
        """
        Whether or not the user answer is correct

        returns: Boolean
        """
        return self.mark > 0


class Quiz:
    # Constants used for coloring the output
    MESSAGE_COLOR_RED = '\033[91m'
    MESSAGE_COLOR_GREEN = '\033[92m'
    MESSAGE_COLOR_BLUE = '\033[94m'

    def __init__(self, summary, data_source):
        """
        Class constructor

        summary:        String  - Summary text to be displayed at the top of the quiz
        data_source:    String  - Full path to CSV file containing the questions
        """
        # Set quiz attributes
        self.summary = summary
        self.questions = {}
        self.users_answers = {}

        # Load questions from the data source
        try:
            self.load_questions(data_source)
        except IOError:
            self.error('Unable to load questions from the data source.')
        except Exception as e:
            self.error(e.message)

    def load_questions(self, data_source):
        """
        Add a child to the current person

        data_source: String - Full path to CSV file containing the questions
        """
        # Open file and read its lines
        file_object = open(data_source, 'r')
        lines = file_object.readlines()
        file_object.close()

        # lambda function to format a line into a list
        format_line = lambda l: map(lambda x: x.strip(), l.split(','))

        # Remove the first line as it is the header
        header = format_line(lines.pop(0))

        # Loop lines and create questions & answers
        for i, line in enumerate(lines):
            parts = format_line(line)

            # Create question instance
            question = Question(i,
                                parts[header.index('text')],
                                parts[header.index('mark')],
                                Answer(parts[header.index('answer')]))

            # Add question to dictionary
            self.add_question(question)

    def add_question(self, question):
        """
        Add a question to quiz questions collections

        question: Question - An instance of a question
        """
        if isinstance(question, Question):
            self.questions[question.id] = question

    def add_user_answer(self, user_answer):
        """
        Add a user answer to quiz user answers collections

        user_answer: UserAnswer - An instance of a user answer
        """
        if isinstance(user_answer, UserAnswer):
            self.users_answers[user_answer.question.id] = user_answer

    def qet_user_answer(self, question):
        """
        Find a user answer instance

        question: Question - An instance of a question
        returns: An instance of the UserAnswer or None if not found
        """
        if question.id in self.users_answers:
            return self.users_answers[question.id]
        return None

    def start(self, limit=5):
        """
        Start the quiz

        limit: Integer - Number of questions to display
        """
        # Display quiz header
        print self.summary
        print "".center(len(self.summary), "=") + "\n"

        # Select random questions
        selected_questions = self.get_random(limit)

        # Total mark
        total = 0.0
        user_total = 0.0

        # Display the quiz
        i = 1  # Question number
        for qid, question in selected_questions:
            # Display quiz question
            self.render(question, i)

            # Count quiz mark
            total += question.mark
            user_total += self.qet_user_answer(question).mark

            i += 1  # Increment question number

        # Display quiz total
        message = 'Total mark: %i/%i' % (user_total, total)
        print "".center(len(message), "=")
        self.print_message(message, self.MESSAGE_COLOR_BLUE)

    def render(self, question, no):
        """
        Render a question in the quiz

        question:   Question - An instance of a question
        no:         Integer  - The question number in the quiz
        """
        # Ask question & return answer
        answer_text = raw_input("%i)\t%s\n" % (no, question.text))

        # User answer object
        user_answer = UserAnswer(question, answer_text)
        self.add_user_answer(user_answer)

        # Check if correct
        message_status = 'Incorrect'
        message_color = self.MESSAGE_COLOR_RED
        if user_answer.is_correct():
            message_color = self.MESSAGE_COLOR_GREEN
            message_status = 'Correct'

        # Display question mark
        self.print_message('Answer is %s' % message_status, message_color)

    def get_random(self, limit):
        """
        Get random question

        limit:  Integer - Number of questions to return
        returns: List containing a random selected questions
        """
        items = self.questions.items()
        return random.sample(items, limit)

    def error(self, message):
        """
        Display error message

        message:  String - The message to display
        """
        self.print_message(message, self.MESSAGE_COLOR_RED)

    @staticmethod
    def print_message(message, color):
        """
        Static method to display a colored message

        message:    String - The message to display
        color:      String - The color of the message
        """
        print "%s%s\033[0m\n" % (color, message)


# Start the program
if __name__ == '__main__':
    Quiz('Random Quiz', './quizmaker_questions.csv').start()
