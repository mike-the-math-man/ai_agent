from functions.get_files_info import get_files_info,get_file_content
from functions.danger import write_file
from functions.run_python_file import run_python_file
def test():
    '''
    print(f"Result for current dir: {get_files_info("calculator", ".")}")
    print(f"Result for pkg: {get_files_info("calculator", "pkg")}")
    print(f"Result for /bin: {get_files_info("calculator", "/bin")}")
    print(f"Result for ../: {get_files_info("calculator", "../")}")
    
    print(get_file_content("calculator", "lorem.txt"))
    
    print(f"main: {get_file_content("calculator", "main.py")}")
    print(f"pkg/calculator: {get_file_content("calculator", "pkg/calculator.py")}")
    print(f"/bin/cat: {get_file_content("calculator", "/bin/cat")} (this should return an error string)")
    print(f"pkg/dne: {get_file_content("calculator", "pkg/does_not_exist.py")} (this should return an error string)")
    
    print(f"lorem: {write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")}")
    print(f"morelorem: {write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")}")
    print(f"/tmp/temp: {write_file("calculator", "/tmp/temp.txt", "this should not be allowed")}")
    '''
    print(f"\n\
        {run_python_file("calculator", "main.py")} (should print the calculator's usage instructions) \n\
        -----------------------------------------------------------------------------------------\n\
        \n{run_python_file("calculator", "main.py", ["3 + 5"])} (should run the calculator... which gives a kinda nasty rendered result) \n\
        -----------------------------------------------------------------------------------------\n\
        \n{run_python_file("calculator", "tests.py")} \n\
        -----------------------------------------------------------------------------------------\n\
        \n{run_python_file("calculator", "../main.py")} (this should return an error) \n\
        -----------------------------------------------------------------------------------------\n\
        \n{run_python_file("calculator", "nonexistent.py")} (this should return an error) \n\
        -----------------------------------------------------------------------------------------\n\
        \n{run_python_file("calculator", "lorem.txt")} (this should return an error)\n")

if __name__ == "__main__":
    test()


