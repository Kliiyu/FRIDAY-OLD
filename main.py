import json
import subprocess
import pyttsx3

from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

import storage.prompts as prompts

low_performance = False
verbose = True

model = OllamaLLM(model="llama3.1")

func_prompt = ChatPromptTemplate.from_template(prompts.func_template)
func_chain = func_prompt | model

prompt = ChatPromptTemplate.from_template(prompts.template)
chain = prompt | model

def decode_fuction_list():
    full_string = ""
    with open('storage/function_list.json', 'r') as f:
        func_list = json.load(f)
        
        for func in func_list:
            full_string += "\n\nstart\nFunction name: {str(func_list[func]['name'])}"
            full_string += f"\nFunction description: {str(func_list[func]['description'])}"
            full_string += "\nFunction usage: "
            
            for usage in func_list[func]['usage']:
                full_string += f"\n{usage}"

            full_string += "\nFunction extract: "
            for i, extract in enumerate(func_list[func]['extract'], start=1):
                full_string += f"\n{i}. {extract}"
                full_string += f"\n{i}. Extract description: {func_list[func]['extract'][extract]}"
                
            full_string += "\nend"
    return full_string, func_list

def decode_function_call(func_call, separator="+"):
    split_call = func_call.split(separator)
    split_call[0] = split_call[0].replace(" ", "")
    return split_call


def run_script_and_get_return_value(name, *args):
    venv_python = r'.venv\Scripts\python.exe'
    if name == "none":
        return "no function was executed"

    try:
        completed_process = subprocess.run(
            [venv_python, f"functions/{name}.py", *args],
            capture_output=True,
            text=True
        )
        if completed_process.returncode == 0:
            return completed_process.stdout.strip()
        else:
            return f"Script error with return code: {completed_process.returncode}"
    except FileNotFoundError:
        print("File does not exist!")
    except Exception as e:
        print(f"An unknown error occured: {e}")
    return "no function was executed"

def handle_conversation(functions: str, func_list: json, tts):
    context = ""
    print("Welcome sir how may I assit you? Type 'exit' when you want to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        func_result = func_chain.invoke({"list": functions, "question": user_input})
        
        print("Function to run:", func_result) if verbose else None
        func_info = func_result.strip().lower()
        dec_func_info = decode_function_call(func_info)
        if verbose:
            print("Decoded function info:", dec_func_info)
            print("Function name:", dec_func_info[0])
            print("Arguments:", dec_func_info[1:])
        return_value = str(run_script_and_get_return_value(dec_func_info[0], *dec_func_info[1:]))
        print("Return value:", return_value) if verbose else None
        
        result = chain.invoke({"context": context, "question": user_input, "func_output": return_value})
        print("FRIDAY:", result)
        
        tts.say(result)
        tts.runAndWait()
        tts.stop()
    
        context += f"\nUser: {user_input}\nFRIDAY: {result}"

def main():
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)
    engine.setProperty('volume',1.0)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    
    functions, func_list = decode_fuction_list()
    print("Functions:", functions) if verbose else None
    handle_conversation(functions, func_list, engine)

if __name__ == "__main__":
    main()