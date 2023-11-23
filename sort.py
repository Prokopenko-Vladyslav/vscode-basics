import os
import shutil

def normalize(text):
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z',
        'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
        'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ю': 'iu', 'я': 'ia', 'ь': '', 'ъ': '',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Ґ': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'Ye', 'Ж': 'Zh', 'З': 'Z',
        'И': 'Y', 'І': 'I', 'Ї': 'Yi', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P',
        'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch',
        'Ю': 'Yu', 'Я': 'Ya', 'Ь': '', 'Ъ': ''
    }

    normalized = ''.join(translit_dict.get(char, char) for char in text)
    normalized = ''.join(char if char.isalnum() or char in [' ', '.'] else '_' for char in normalized)
    return normalized

def sort_folder(directory):
    extensions = {
        'image': ['jpeg', 'png', 'jpg', 'svg'],
        'video': ['avi', 'mp4', 'mov', 'mkv'],
        'document': ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
        'audio': ['mp3', 'ogg', 'wav', 'amr'],
        'archive': ['zip', 'gz', 'tar']
    }

    known_extensions = set()  # Збереження відомих розширень
    unknown_extensions = set()
    sorted_directory = os.path.join(directory, 'sorted')
        # Перевірка наявності папки "sorted" і переміщення вже існуючих підпапок
    if not os.path.exists(sorted_directory):
        os.makedirs(sorted_directory)
    else:
        # Перенесення вже існуючих підпапок у відсортовану папку
        existing_folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
        for folder in existing_folders:
            source = os.path.join(directory, folder)
            destination = os.path.join(sorted_directory, folder)
            shutil.move(source, destination)

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_extension = file.split('.')[-1].lower()
            input_file_path = os.path.join(root, file)

            # Роздільне сортування файлів
            if file_extension in extensions['archives']:
                new_folder_name = os.path.join(sorted_directory, 'archives', normalize(file.split('.')[0]))
                os.makedirs(new_folder_name, exist_ok=True)

                try:
                    shutil.unpack_archive(input_file_path, new_folder_name)
                except Exception as e:
                    print(f"Failed to unpack {file}: {e}")

            else:
                found_category = False
                for category, ext_list in extensions.items():
                    if file_extension in ext_list:
                        found_category = True
                        new_file_name = f"{normalize(file.split('.')[0])}.{file_extension}"
                        category_dir = os.path.join(sorted_directory, category)
                        destination = os.path.join(category_dir, new_file_name)

                        if not os.path.exists(category_dir):
                            os.makedirs(category_dir)

                        shutil.copyfile(input_file_path, destination)
                        known_extensions.add(file_extension)
                        break
                if not found_category:
                    unknown_extensions.add(file_extension)        # додавання невідомих розширень 
                    unknown_dir = os.path.join(sorted_directory, 'unknown')

                    if not os.path.exists(unknown_dir):
                        os.makedirs(unknown_dir)

                    unknown_destination = os.path.join(unknown_dir, file)
                    shutil.move(input_file_path, unknown_destination)

    return {
        'known_extensions': list(known_extensions),
        'unknown_extensions': list(unknown_extensions),
        'extensions': extensions
    }

if __name__ == "__main__":
    import sys

    folder_path = sys.argv[1]
    result = sort_folder(folder_path)

    print(sys.argv[0])
    print("Known extensions:")
    print(result['known_extensions'])
    print("\nUnknown extensions:")
    print(result['unknown_extensions'])