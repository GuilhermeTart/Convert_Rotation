import os  # Importa o módulo os para interagir com o sistema operacional
import rich  # Importa o módulo rich para formatação e exibição de texto no console
from rich.console import Console  # Importa a classe Console do módulo rich.console
from rich.prompt import Prompt  # Importa a classe Prompt do módulo rich.prompt
from rich.table import Table  # Importa a classe Table do módulo rich.table
import subprocess  # Importa o módulo subprocess para executar comandos do sistema

console = Console()  # Cria uma instância da classe Console para exibir texto formatado no console


# Função para listar arquivos de mídia em um diretório
def list_media(directory):
    media_files = []  # Inicializa uma lista vazia para armazenar os arquivos de mídia
    for root, dirs, files in os.walk(directory):  # Percorre o diretório e subdiretórios
        for file in files:  # Percorre os arquivos encontrados
            if file.endswith(('.mp4', '.mkv', '.avi', '.mov')):  # Verifica se o arquivo é de mídia
                media_files.append(os.path.join(root, file))  # Adiciona o caminho completo do arquivo à lista
    return media_files  # Retorna a lista de arquivos de mídia

# Função para mudar a resolução de um arquivo de mídia
def change_resolution(media_file, resolution):
    width, height = resolution.split('x')  # Divide a resolução em largura e altura
    output_file = f"{os.path.splitext(media_file)[0]}_Renderizado{os.path.splitext(media_file)[1]}"  # Cria o nome do arquivo de saída
    cmd = ['ffmpeg', '-i', media_file, '-vf', f'scale={width}:{height}', '-c:a', 'copy', output_file]  # Comando ffmpeg para mudar a resolução
    subprocess.run(cmd, check=True)  # Executa o comando ffmpeg
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para rotacionar um arquivo de mídia
def rotate_media(media_file, angle):
    output_file = f"{os.path.splitext(media_file)[0]}_rotated{os.path.splitext(media_file)[1]}"  # Cria o nome do arquivo de saída
    transpose = '1' if angle == 'D' else '2'  # Define o valor de transpose com base no ângulo
    cmd = ['ffmpeg', '-i', media_file, '-vf', f'transpose={transpose}', '-c:a', 'copy', output_file]  # Comando ffmpeg para rotacionar o vídeo
    subprocess.run(cmd, check=True)  # Executa o comando ffmpeg
    os.system('cls' if os.name == 'nt' else 'clear')


# Função principal que coordena a execução do script
def main():
    directory = os.getcwd()  # Obtém o diretório de trabalho atual
    console.print(f"Operando no diretório atual: {directory}",style="blue")  # Exibe o diretório atual no console
    media_files = list_media(directory)  # Lista os arquivos de mídia no diretório atual
    if not media_files:  # Verifica se não há arquivos de mídia
        console.print("Nenhum arquivo de mídia encontrado no diretório atual.", style="red")  # Exibe mensagem de erro
        return  # Encerra a função

    # Cria uma tabela para exibir os arquivos de mídia e opções
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Arquivo", style="dim")
    table.add_column("Opções")
    for media_file in media_files:  # Adiciona os arquivos de mídia à tabela
        table.add_row(os.path.basename(media_file), "[bold green]Mudar resolução[/bold green] | [bold blue]Rotacionar[/bold blue]")
    console.print(table)  # Exibe a tabela no console
    console.print(r"""


__________                   .___            __________        __          __  .__               
\______   \ ____   ____    __| _/___________ \______   \ _____/  |______ _/  |_|__| ____   ____  
 |       _// __ \ /    \  / __ |/ __ \_  __ \ |       _//  _ \   __\__  \\   __\  |/  _ \ /    \ 
 |    |   \  ___/|   |  \/ /_/ \  ___/|  | \/ |    |   (  <_> )  |  / __ \|  | |  (  <_> )   |  \
 |____|_  /\___  >___|  /\____ |\___  >__|____|____|_  /\____/|__| (____  /__| |__|\____/|___|  /
        \/     \/     \/      \/    \/  /_____/      \/                 \/                    \/ 



""", style="green")
                
    while True:  # Loop infinito para exibir o menu de opções
        console.print("Selecione uma opção:",style="green")
        console.print("1. Mudar resolução")
        console.print("2. Rotacionar")
        console.print("3. Sair")
        choice = Prompt.ask("Insira o número da opção", choices=["1", "2", "3"])  # Solicita ao usuário que escolha uma opção

        if choice == "1":  # Se a escolha for mudar a resolução
            media_file_path = Prompt.ask("Insira o nome do arquivo que deseja mudar a resolução", choices=[os.path.basename(media_file) for media_file in media_files])  # Solicita o nome do arquivo
            media_file = [file for file in media_files if os.path.basename(file) == media_file_path][0]  # Obtém o caminho completo do arquivo
            resolution = Prompt.ask("Insira a resolução desejada ((V): 720x1280)", default='(H)1280x720')  # Solicita a resolução desejada
            change_resolution(media_file, resolution)  # Chama a função para mudar a resolução

        elif choice == "2":  # Se a escolha for rotacionar
            media_file_path = Prompt.ask("Insira o nome do arquivo que deseja rotacionar", choices=[os.path.basename(file) for file in media_files])  # Solicita o nome do arquivo
            media_file = [file for file in media_files if os.path.basename(file) == media_file_path][0]  # Obtém o caminho completo do arquivo
            angle = Prompt.ask("Insira a opção de rotação (D para direita, E para esquerda)", choices=['D', 'E'])  # Solicita o ângulo de rotação
            rotate_media(media_file, angle)  # Chama a função para rotacionar o vídeo

        elif choice == "3":  # Se a escolha for sair
            break  # Encerra o loop

        else:  # Se a escolha for inválida
            console.print("Opção inválida. Tente novamente.",style ="red")  # Exibe mensagem de erro

# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    main()  # Chama a função principal
