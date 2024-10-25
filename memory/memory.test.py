from memory.memory import functions
from tools.output import output, title, OutputType, console
from rich.progress import track
import time

title("FRIDAY")
output("Starting FRIDAY", output_type=OutputType.DEBUG)
for i in track(range(10), description="Initializing...      "):
    time.sleep(0.05)

fn = functions()
fn.update(r"D:\FRIDAY\functions")

result = fn.query("i want to search for rick astley on youtube", 1)

console.print(result) if result else output("No results found", output_type=OutputType.ERROR)