import os
import shutil

def normalize(text):
    # Словник для транслітерації кириличних символів
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z',
        'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
        'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ю': 'iu', 'я': 'ia',
        'ь': '', 'ъ': '',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Ґ': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'Ye', 'Ж': 'Zh', 'З': 'Z',
        'И': 'Y', 'І': 'I', 'Ї': 'Yi', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P',
        'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch',
        'Ю': 'Yu', 'Я': 'Ya',
        'Ь': '', 'Ъ': ''
    }

    # Заміна кириличних символів на латинські та очищення від небажаних символів
    normalized = ''.join(translit_dict.get(char, char) for char in text)
    normalized = ''.join(char if char.isalnum() or char in [' ', '.'] else '_' for char in normalized)

    return normalized

def sort_folder(directory):
    # Створення словників для розширень файлів
    extensions = {
        'images': ['JPEG', 'PNG', 'JPG', 'SVG'],
        'videos': ['AVI', 'MP4', 'MOV', 'MKV'],
        'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
        'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
        'archives': ['ZIP', 'GZ', 'TAR']
    }

    unknown_extensions = set()  # Множина для невідомих розширень

    # Рекурсивна обробка всіх файлів та папок у даній директорії
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_extension = file.split('.')[-1].upper()

            # Створюємо шляхи до вхідних та вихідних файлів
            input_file_path = os.path.join(root, file)
            output_directory = os.path.join(directory, 'sorted_files')

            # Створюємо нову папку для відсортованих файлів, якщо вона ще не існує
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            # Перевіряємо, чи це архів
            if file_extension in extensions['archives']:
                new_folder_name = os.path.join(output_directory, normalize(file.split('.')[0]))

                # Створюємо папку для архіву
                os.makedirs(new_folder_name)

                # Розпаковуємо архів
                shutil.unpack_archive(input_file_path, new_folder_name)

            else:
                # Визначаємо категорію файлу
                found_category = False
                for category, ext_list in extensions.items():
                    if file_extension in ext_list:
                        found_category = True
                        new_file_name = f"{normalize(file.split('.')[0])}.{file_extension}"
                        destination = os.path.join(output_directory, category, new_file_name)

                        # Створюємо папку для категорії, якщо вона ще не існує
                        if not os.path.exists(os.path.join(output_directory, category)):
                            os.makedirs(os.path.join(output_directory, category))

                        # Копіюємо файл у відповідну категорію
                        shutil.copyfile(input_file_path, destination)
                        break

                if not found_category:
                    unknown_extensions.add(file_extension)

    # Повертаємо дані про файли
    return {
        'unknown_extensions': list(unknown_extensions),
        'extensions': extensions
    }

if __name__ == "__main__":
    import sys

    # Отримуємо аргумент командного рядка, який вказує на папку для сортування
    folder_path = sys.argv[1]

    # Запускаємо функцію сортування
    result = sort_folder(folder_path)

    # Виводимо результати сортування
    print("Known extensions:")
    print(result['extensions'])
    print("\nUnknown extensions:")
    print(result['unknown_extensions'])