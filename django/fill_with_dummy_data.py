import os,sys 
sys.path.append('/mnt/c/Users/Mikeg/Projects/think')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
import csv
from think.models import Question,Answer
from django.contrib.auth.models import User

def fill_with_test_data():

    files = ['../demo_files/users.txt','../demo_files/questions.txt','../demo_files/answers.txt']

    with open(files[0],'r',newline='\n') as f:
        # USERS
        reader = csv.reader(f)
        # This skips the first row of the CSV file.
        next(reader)
        data = list(reader)
        for user in data:
            print(f"Adding user {user}")
            t = User.objects.create_user(
                username=user[0],
                password=user[1],
                email=user[2],
            )
            t.profile.alien_form = user[3]
            t.save()
            print('** User Added **')

    with open(files[1],'r',newline='\n') as f:
        # Questions
        reader = csv.reader(f)
        # This skips the first row of the CSV file.
        next(reader)
        data = list(reader)
        for question in data:
            print(f"Adding question {question}")
            t = Question(
                question_text=question[1],
            )
            t.save()
            print('** Question Added **')

    with open(files[2],'r',newline='\n') as f:
        # Answers
        reader = csv.reader(f)
        # This skips the first row of the CSV file.
        next(reader)
        data = list(reader)
        for an in data:
            print(f"Adding answer {an}")
            user = User.objects.get(username=an[1])
            question = Question.objects.get(question_id=an[2])
            print(user)
            t = Answer(
                user=user,
                question=question,
                answer_text=an[3]
            )
            t.save()
            print('** Answer Added **')
            
def main():
    fill_with_test_data()

if __name__ == "__main__":
    main()