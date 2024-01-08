# example/views.py
# from datetime import datetime

# from django.http import HttpResponse

# def index(request):
#     now = datetime.now()
#     html = f'''
#     <html>
#         <body>
#             <h1>Hello from Vercel!</h1>
#             <p>The current time is { now }.</p>
#         </body>
#     </html>
#     '''
#     return HttpResponse(html)

from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.template import loader
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
from ninja import Router
from django.conf import settings
import json
import time

api_key = settings.OPENAI_API_KEY

router = Router()

def index(request):
    data = {
        'param1': 'Name',
        'param2': 'Birth',
        'param3': 'Country',
        'param4': 'Genre',
        'param5': 'Philosophy'
    }
    template = loader.get_template('main.html')
    return HttpResponse(template.render(data))

@csrf_exempt
def get_prompt(request):
    if request.method == 'GET':
        prompt = request.GET.get('prompt')
        
        def generate(stream):
            gpt_model = "gpt-3.5-turbo"

            client = OpenAI(
                api_key=api_key
            )
            
            if stream == True:
                for chat_completion in client.chat.completions.create(messages=[{"role": "user", "content": prompt,}], model=gpt_model, stream=True):
                # yield chat_completion
                    item = chat_completion.choices[0].delta.content
                    if item is not None:
                        yield item
            else:
                chat_completion = client.chat.completions.create(messages=[{"role": "user", "content": prompt,}], model=gpt_model)
                msg = chat_completion.choices[0].message.content
                return msg
        
        response = StreamingHttpResponse(generate(True))
        response['Cache-Control'] = 'no-cache'
        return response

@csrf_exempt
def suggest_input(request):
    if request.method == 'GET':
        prompt = request.GET.get('prompt')
        if prompt != "":
            msg = generate_ai(prompt)
        return HttpResponse(msg)
    return HttpResponse("error")


def generate_ai(prompt):
    gpt_model = "gpt-3.5-turbo"

    client = OpenAI(
        api_key=api_key
    )

    chat_completion = client.chat.completions.create(messages=[{"role": "user", "content": prompt,}], model=gpt_model)
    msg = chat_completion.choices[0].message.content
    return msg


def generate_assistant_ai(request):
    if request.method == 'GET':
        prompt = request.GET.get('prompt')
        if prompt != "":
            msg = create_assistant(prompt)
        return HttpResponse(msg)
    return HttpResponse("error")
  
def create_assistant(prompt):
    client = OpenAI(
        api_key=api_key
    )

    assistant = client.beta.assistants.create(
        name="Writer Tutor",
        instructions=prompt,
        # tools=[{"type": ""}],
        model="gpt-3.5-turbo"
    )
    # print(assistant.id)

    thread = client.beta.threads.create()
    # print(thread.id)
    assistant_id = assistant.id
    thread_id = thread.id
    
    return f"{assistant_id}, {thread_id}"


def get_assistant_ai(request):
    if request.method == 'GET':
        prompt = request.GET.get('prompt')
        asst_id = request.GET.get('asst_id')
        thread_id = request.GET.get('thread_id')
        msg = prompt
        
        def generate(stream):
            gpt_model = "gpt-3.5-turbo"

            client = OpenAI(
                api_key=api_key
            )
        
            if stream == True:
                message = client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=msg
                )

                run = client.beta.threads.runs.create(
                    thread_id=thread_id,
                    assistant_id=asst_id
                )

                run = client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                )
        
        response = StreamingHttpResponse(generate(True))
        response['Cache-Control'] = 'no-cache'
        return response
  
  

def upload_json(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            print(file)
        # Process the file or perform any required operations
        # ...
        return HttpResponse('File uploaded successfully')
    else:
        return HttpResponse('No file provided', status=400)