import os
import rich
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import subprocess

console = Console()

def list_media(directory): 
    media_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.mp4', '.mkv', '.avi', '.mov', '.jpg','.png')):
                media_files.append(os.path.join(root, file))
    return media_files

def change_resolution(media_file, resolution):
    width, height = resolution.split('x')
    output_file = f"{os.path.splitext(media_file)[0]}_resized{os.path.splitext(media_file)[1]}"
    cmd = ['ffmpeg', '-i', media_file, '-vf', f'scale={width}:{height}', '-c:a', 'copy', output_file]
    subprocess.run(cmd, check=True)

def rotate_media(media_files, angle):
    transpose = '1' if angle == 'D' else '2'
    for media_file in media_files:
        output_file = f"{os.path.splitext(media_file)[0]}_rotated{os.path.splitext(media_file)[1]}"
        cmd = ['ffmpeg', '-i', media_file, '-vf', f'transpose={transpose}', '-c:a', 'copy', output_file]
        subprocess.run(cmd, check=True)

def main():
    directory = os.getcwd()
    console.print(f"Operando no diretório atual: {directory}", style="blue")
    media_files = list_media(directory)
    if not media_files:
        console.print("Nenhum arquivo de mídia encontrado no diretório atual.", style="red")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Arquivo", style="dim", no_wrap=True)
    table.add_column("Opções", no_wrap=True)
    for media_file in media_files:
        table.add_row(os.path.basename(media_file), "[bold green]Mudar resolução[/bold green] | [bold blue]Rotacionar[/bold blue]")
    console.print(table)
    
    
    console.print(r"""


    __________                   .___            __________        __          __  .__               
    \______   \ ____   ____    __| _/___________ \______   \ _____/  |______ _/  |_|__| ____  ____  
    |       _// __ \ /    \  / __ |/ __ \_  __ \ |       _//  _ \   __\__  \\   __\  |/  _ \ /    \ 
    |    |   \  ___/|   |  \/ /_/ \  ___/|  | \/ |    |   (  <_> )  |  / __ \|  | |  (  <_> )   |  \
    |____|_  /\___  >___|  /\____ |\___  >__|____|____|_  /\____/|__| (____  /__| |__|\____/|___|  /
            \/     \/     \/      \/    \/  /_____/      \/                 \/                    \/ 



    """, style="green")

    while True:
        console.print("Selecione uma opção:")
        console.print("1. Mudar resolução")
        console.print("2. Rotacionar")
        console.print("3. Sair")
        choice = Prompt.ask("Insira o número da opção", choices=["1", "2", "3"])

        if choice == "1":
            media_file_path = Prompt.ask("Insira o nome do arquivo que deseja mudar a resolução", choices=[os.path.basename(media_file) for media_file in media_files])
            media_file = [file for file in media_files if os.path.basename(file) == media_file_path][0]
            resolution = Prompt.ask("Insira a resolução desejada (ex: 1280x720)", default='1280x720')
            change_resolution(media_file, resolution)
        elif choice == "2":
            selected_files = []
            while True:
                media_file_path = Prompt.ask("Insira o nome do arquivo que deseja rotacionar (ou 'all' para selecionar todos, 'done' para finalizar)", choices=[os.path.basename(file) for file in media_files] + ['all', 'done'])
                if media_file_path == 'done':
                    break
                elif media_file_path == 'all':
                    selected_files = media_files
                    break
                else:
                    selected_files.append([file for file in media_files if os.path.basename(file) == media_file_path][0])
            if selected_files:
                angle = Prompt.ask("Insira a opção de rotação (D para direita, E para esquerda)", choices=['D', 'E'])
                rotate_media(selected_files, angle)
        elif choice == "3":
            break
        else:
            console.print("Opção inválida. Tente novamente.", style="red")

if __name__ == "__main__":
    main()
