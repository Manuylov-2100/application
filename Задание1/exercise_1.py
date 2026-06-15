# Импорт необходимых библиотек
import re
import sys
from collections import Counter

# Удаление знаков препинания и приведение к нижнему регистру
def clean_word(word):
    cleaned = re.sub(r'[^a-zA-Zа-яА-Я]', '', word.lower())
    return cleaned

# Анализ файла: подсчет частоты слов и сортировка по убыванию
def analyze_text_file(input_filename, output_filename=None, console_output=False):
    # Args:
        # input_filename: имя входного файла
        # output_filename: имя выходного файла (если None, то result.txt)
        # console_output: флаг вывода в консоль

    if output_filename is None:
        output_filename = "result.txt"

    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            text = f.read()

        # Разбиение на слова и очистка
        words = text.split()
        cleaned_words = []

        for word in words:
            cleaned = clean_word(word)
            if cleaned and len(cleaned) > 0:
                cleaned_words.append(cleaned)

        # Подсчет частоты слов
        word_counter = Counter(cleaned_words)

        # Сортировка по убыванию частоты, затем по алфавиту при равной частоте
        sorted_words = sorted(word_counter.items(), key=lambda x: (-x[1], x[0]))

        # Формирование результата
        result_lines = []
        for word, count in sorted_words:
            result_lines.append(f"{word.capitalize()} {count}")

        result_text = "\n".join(result_lines)

        # Вывод в файл
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(result_text)

        # Вывод в консоль если требуется
        if console_output:
            print("\n=== РЕЗУЛЬТАТ АНАЛИЗА ===")
            print(result_text)
            print("=== КОНЕЦ РЕЗУЛЬТАТА ===")

        return True

    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_filename}' не найден!")
        return False
    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")
        return False

def main():
    input_file = "resourse_1.txt"
    output_file = "result.txt"
    console_output = False

    # Обработка аргументов командной строки
    if len(sys.argv) > 1:
        if "-c" in sys.argv:
            console_output = True

    # Выполнение анализа
    success = analyze_text_file(input_file, output_file, console_output)

    if success:
        print("\nПрограмма выполнена успешно!")
    else:
        print("\nПрограмма завершена с ошибкой!")
        sys.exit(1)

if __name__ == "__main__":
    main()

