from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from .models import Quiz, Question, AnswerOption, QuizAttempt, UserAnswer



def register(request):
    if request.method == 'POST':
         # Manually capture form data
        username = request.POST['username']
        email = request.POST['email']
        name = request.POST['name']
        gender = request.POST['gender']
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        User = get_user_model()
        
        #Checking if the email is already exist
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already exists. Please use a different email address.")
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists. Please use a different username.")
        
        # Check if the two passwords match
        if password != confirm_password:
            return HttpResponse("Passwords do not match!")
       
        user = User.objects.create(username=username, email=email, password=make_password(password))
        
        user.name = name
        user.gender = gender
        user.save()

        messages.success(request, f'Account created for {username}!')
        return redirect('login')  
    else:
        form = UserRegisterForm()
    return render(request, 'quiz_app/register.html', {'form': form})


def home(request):
    return render(request, 'quiz_app/home.html')

# Contact view
def contact(request):
    return render(request, 'quiz_app/contact.html')

# Login view
def user_login(request):
     if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')

        # Authenticating the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            # Redirect to a success page.
            return redirect('home')  
        else:
            # Return an 'invalid login' error message.
            messages.error(request, 'Invalid username or password.')

     return render(request, 'quiz_app/login.html')

def user_logout(request):
    logout(request)
    # Redirect to login page after logout
    return redirect('login')

#User view for Quizzes and other Related functionalities.


def quiz_list(request):
    quizzes = Quiz.objects.filter(active=True).order_by('-date_created')
    return render(request, 'quizzes/quiz_list.html', {'quizzes': quizzes})

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from .models import Quiz, Question, AnswerOption, QuizAttempt, UserAnswer

def take_quiz(request, quiz_id):
    # Retrieve the quiz object
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # Ensure a quiz_attempt is initialized for authenticated users at the beginning
    if request.user.is_authenticated:
        quiz_attempt, created = QuizAttempt.objects.get_or_create(
            quiz=quiz,
            user=request.user,
            defaults={'score': 0}  # Used only if a new object is created
        )
    
    if request.method == 'POST':
        # Extract question ID and selected option ID from POST data
        question_id = request.POST.get('question_id')
        selected_option_id = request.POST.get('answer')

        # Retrieve the current question based on question_id
        current_question = get_object_or_404(Question, id=question_id)
        
        # Validate and process the selected option
        if selected_option_id:
            selected_option = get_object_or_404(AnswerOption, id=selected_option_id)
            # Check if the selected option is correct
            if selected_option.is_correct:
                # Increment the user's score for a correct answer
                if request.user.is_authenticated:
                    quiz_attempt.score += 1
                    quiz_attempt.save()

            # Save the user's answer (if authenticated)
            if request.user.is_authenticated:
                UserAnswer.objects.create(
                    quiz_attempt=quiz_attempt,
                    question=current_question,
                    selected_answer=selected_option,
                    # Assume there's a field to indicate correctness in UserAnswer
                    is_correct=selected_option.is_correct  
                )

        # Redirect to the next question or to the score page if this is the last question
        questions = list(quiz.questions.all())
        current_question_index = questions.index(current_question)
        if current_question_index + 1 < len(questions):
            next_question = questions[current_question_index + 1]
            return render(request, 'quizzes/take_quiz.html', {'quiz': quiz, 'question': next_question})
        else:
            # This was the last question
            return HttpResponseRedirect(f'/quiz/{quiz.id}/score/')
    else:
        # If it's not a POST request, show the first question or a specific question
        questions = list(quiz.questions.all())
        if questions:
            question = questions[0]
            return render(request, 'quizzes/take_quiz.html', {'quiz': quiz, 'question': question})
        else:
            # Handle case with no questions
            return render(request, 'quizzes/no_questions.html', {'quiz': quiz})
        
def quiz_score(request, quiz_id):
    if not request.user.is_authenticated:
        # Redirect to login page or show an error
        return redirect('login')

    quiz_attempt = QuizAttempt.objects.filter(quiz_id=quiz_id, user=request.user).latest('date_attempted')
    return render(request, 'quizzes/quiz_score.html', {'quiz_attempt': quiz_attempt})
