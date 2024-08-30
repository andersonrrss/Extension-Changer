import os
import re
import shutil
from sys import argv

def main():
    options = {
        3: (rename, 2),  # 3 argumentos: rename(argv[1], argv[2])
        4: (rename, 3),  # 4 argumentos: rename(argv[1], argv[2], argv[3])
        5: (rename, 4)  # 5 argumentos: rename(argv[1], argv[2], argv[3], argv[4])
    }

    if len(argv) not in options:
        print("Uso do comando: <extensão original> <extensão nova> <caminho do diretório de entrada(opcional)> <caminho do diretório de saída(opcional)>")
        return

    func, num_args = options[len(argv)]
    func(*argv[1:num_args+1])

def rename(extension, new_extension, source_dir="./", target_dir=None):
    # Checa se as extensões foram realmente fornecidas
    if not validate_extension(extension) or not validate_extension(new_extension):
        raise ValueError("Extensão original e nova extensão devem ser fornecidas")
    
    # Checa se o arquivo de entrada é válido
    if not os.path.exists(source_dir) and (not os.path.isdir(source_dir) or not os.path.isfile(source_dir)):
        raise ValueError("Caminho de entrada inválido")

    # Define o arquivo de saída para o mesmo de entrada se ele não for expecificado
    if target_dir is None:
        target_dir = source_dir
    try:
        # Cria a pasta de saída se ela não existir
        os.makedirs(target_dir, exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"Ocorreu um erro ao criar o diretório de saída: {e}")

    extension = extension.lower()
    new_extension = new_extension.lower()

    # Itera pelos arquivos da pasta de entrada
    for item in os.listdir(source_dir):
        file_path = os.path.join(source_dir, item) # Caminho completo do arquivo
        # Checa se o arquivo termina com a extensão expecificada
        if os.path.isfile(file_path) and file_path.endswith(extension):
            try:
                base, _ = os.path.splitext(item)
                new_path = os.path.join(target_dir, f"{base}.{new_extension}") # Muda a extensão do arquivo
                shutil.copy2(file_path, new_path) # Copia o arquivo renomeado na pasta de saída
            except Exception as e:
                raise RuntimeError(f"Falha ao mudar a extensão de {file_path}: {e}")
            
    # Imprime mensagem de sucesso se caso não houver falhas
    print("Todos os arquivos foram copiados e renomeados com sucesso!")


def validate_extension(extension):
    """
    Verifica se a extensão é válida.

    Uma extensão é considerada válida se:
    - Não estiver vazia
    - Não contiver caracteres inválidos (como ../, ~, etc.)
    - Tiver apenas letras, dígitos e pontos (.)

    :param extension: A extensão a ser validada
    :return: True se a extensão for válida, False caso contrário
    """
    if not extension:
        return False

    pattern = r'^[a-zA-Z0-9\.]+$'
    if re.match(pattern, extension):
        return True
    return False

        
if __name__ == "__main__":
    main()