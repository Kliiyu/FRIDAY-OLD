import json
import subprocess
import pyttsx3
import time

from memory.memory import functions
from rich.progress import track
from output import output, OutputType, title, track_desc_gen, inp, console
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import storage.prompts as prompts


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
def run_func(fn_vec, user_input, verbose: bool = True):
    func_result = fn_vec.query(user_input, 1)
    return func_result
    
    
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
    
    console.print("\n[white]Welcome sir how may I assit you? Type [red]'exit'[/] when you want to quit.[/]")
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
            console.print("\n[white]How may I assit you? Type [red]'exit'[/] when you want to quit.[/]")
            console.print("[white]Type [red]'clear'[/] to clear the screen.")
            console.print("[white]Type [red]'verbose'[/] to toggle verbose mode.\n")
            continue
        output("Processing...", OutputType.INFO, verbose=verbose)
        run_func(fn_vec, user_input, verbose=verbose)
        response = test_chain.invoke({"question": user_input})
        if tts: 
            speak(engine, response)
        else:
            console.print(f"[green]FRIDAY > {response}[/]")
        
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
    test_prompt = ChatPromptTemplate.from_template(prompts.test_template)
    test_chain = test_prompt | model

    main(verbose)