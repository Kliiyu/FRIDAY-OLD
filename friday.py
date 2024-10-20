import json
import subprocess
import pyttsx3
import time

from memory.memory import functions, ltm
from rich.progress import track
from output import output, OutputType, title, track_desc_gen, inp, console
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
import storage.prompts as prompts

STM_PATH = "memory/stm.txt"

# Tts engine
def init_tts():
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)
    engine.setProperty('volume',1.0)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    output("TTS engine initialized.", OutputType.INFO, verbose=verbose)
    return engine

def speak(engine, response):
    output("Speaking...", OutputType.INFO, verbose=verbose)
    console.print(f"[green]FRIDAY > {response}[/]")
    engine.say(response)
    engine.runAndWait()
    output("Finished speaking.", OutputType.INFO, verbose=verbose)
    
# Run function
def run_func(chain, fn_vec, user_input, verbose: bool = True):
    func_result = fn_vec.query(user_input, 1)
    name = func_result["ids"][0][0]
    desc = func_result["documents"][0][0]

    run = pre_func_chain.invoke({"question": user_input, "function": name, "description": desc}).lower().strip()

    if run == "yes":
        qfi = {
            "question": user_input,
            "function": name,
            "instruct": desc
        }
        
        output(f"Extracting arguments for function: {name}", OutputType.INFO, verbose=verbose)
        arguments = chain.invoke(qfi)
        arguments = arguments.split("+")
        arguments[0] = arguments[0].replace(" ", "")
        
        output(f"Function to run: {name} with arguments: {arguments}", OutputType.INFO, verbose=verbose)
        
        venv_python = r'.venv\Scripts\python.exe'
        if arguments == "none":
            arguments = []
        
        try:
            completed_process = subprocess.run(
                [venv_python, f"functions/{name}/function.py", *arguments],
                capture_output=True,
                text=True
            )
            if completed_process.returncode == 0:
                return completed_process.stdout.strip()
            else:
                return f"Script error with return code: {completed_process.returncode}"
        except FileNotFoundError:
            output("File does not exist!", OutputType.ERROR, verbose=verbose)
        except Exception as e:
            output(f"An unknown error occurred: {e}", OutputType.ERROR, verbose=verbose)
    else:
        return "no function was executed"
    

def get_ltm(user_input):
    long_term = ltm(verbose=verbose)
    
    long_term.insert(["my day has been great", "i like bananas a lot", "apples are not that good", "i am made by Adrian", "steam is a video game platform"], ["id1", "id2", "id3", "id4", "id5"])
    
    fetched = long_term.query(user_input, 5)
    formatted = ""
    for i in range(len(fetched["documents"][0])):
        formatted += f"{i+1}. {fetched['documents'][0][i]}\n\n"
    
    return formatted

def get_stm(path, user_input):
    with open(path, "r") as f:
        lines = f.readlines()
    
    formatted = ""
    for line in lines:
        if user_input.lower() in line.lower():
            formatted += line
    
    return formatted


def update_stm(path, user_input, response):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(path, "a") as f:
        f.write(f"{timestamp} - Me > {user_input}; FRIDAY > {response}\n")
    
    with open(path, "r") as f:
        lines = f.readlines()
    
    if len(lines) > 50:
        lines = lines[-50:]
    
    with open(path, "w") as f:
        f.writelines(lines)
    
# Main
def main(verbose):
    title("FRIDAY", verbose=verbose)
    output("Starting FRIDAY", output_type=OutputType.DEBUG, verbose=verbose)
    if verbose:
        for _ in track(range(10), description=track_desc_gen("Initializing...")):
            time.sleep(0.05)
            
    fn_vec = functions(verbose=verbose)
    fn_vec.update(r"D:\FRIDAY\functions")
        
    engine = init_tts()
    
    console.print("\n[white]Welcome sir how may I assist you? Type [red]'exit'[/] when you want to quit.[/]")
    console.print("[white]Type [red]'help'[/] for more commands.[/]")
    
    while True:
        user_input = inp(f"[red]YOU > [/]")
        if user_input == "exit":
            break
        elif user_input == "clear":
            subprocess.run("cls", shell=True)
            continue
        elif user_input == "verbose":
            verbose = not verbose
            console.print(f"[white]Verbose mode set to [red]{verbose}[/].[/]\n")
            continue
        elif user_input == "help":
            console.print("\n[white]How may I assist you? Type [red]'exit'[/] when you want to quit.[/]")
            console.print("[white]Type [red]'clear'[/] to clear the screen.")
            console.print("[white]Type [red]'verbose'[/] to toggle verbose mode.\n")
            continue
        
        output("Processing...", OutputType.INFO, verbose=verbose)
        function_output = run_func(func_chain, fn_vec, user_input, verbose=verbose)
        
        long_term = get_ltm(user_input)
        short_term = get_stm(STM_PATH, user_input)
        
        result = response_chain.invoke({"long_term": long_term, "short_term": short_term, "question": user_input, "func_output": function_output})
        update_stm(STM_PATH, user_input, result)
        
        if tts: 
            speak(engine, result)
        else:
            console.print(f"[green]FRIDAY > {result}[/]")
        
    output("Exiting...", OutputType.INFO, verbose=verbose)
    engine.stop()
    
if __name__ == "__main__":
    low_performance = False
    verbose = True
    tts = True

    if low_performance:
        model = OllamaLLM(model="llama3.2:1b")
        output("Using low performance model.", OutputType.INFO, verbose=verbose)
    else:
        model = OllamaLLM(model="llama3.1")
        output("Using high performance model.", OutputType.INFO, verbose=verbose)

    # Prompts
    pre_func_prompt = ChatPromptTemplate.from_template(prompts.pre_func_template)
    pre_func_chain = pre_func_prompt | model
    
    func_prompt = ChatPromptTemplate.from_template(prompts.func_template)
    func_chain = func_prompt | model
    
    response_prompt = ChatPromptTemplate.from_template(prompts.template)
    response_chain = response_prompt | model

    main(verbose)