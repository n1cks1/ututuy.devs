import json
from datetime import datetime

def date_range(data):
    dates = [datetime.strptime(p['date'], '%Y-%m-%d') for p in data if 'date' in p]
    min_date, max_date = min(dates), max(dates)
    print(f"Диапазон дат публикования: с {min_date.strftime('%Y-%m-%d')} по {max_date.strftime('%Y-%m-%d')}")

def count_missing(data, field):
    return sum(1 for p in data if field not in p or not p[field])

def main():
    with open('patents.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    date_range(data)

    fields = ['date', 'author', 'text_patent', 'title']
    missing_counts = {field: count_missing(data, field) for field in fields}

    texts = [p.get('text_patent', '') for p in data]
    word_counts = [len(text.split()) for text in texts]
    sorted_word_counts = sorted(word_counts)
    median_words = sorted_word_counts[len(sorted_word_counts) // 2] if len(sorted_word_counts) % 2 == 1 else (sorted_word_counts[len(sorted_word_counts) // 2 - 1] + sorted_word_counts[len(sorted_word_counts) // 2]) / 2

    all_words = [word for text in texts for word in text.split()]
    uniq_words = set(all_words)

    print(f'Количество записей - {len(data)}')
    print(f'Общее количество слов в {len(data)} записях - {len(all_words)}')
    print(f'Количество уникальных слов - {len(uniq_words)}')
    print('Доля пропусков в записях по каждому из атрибутов:')
    print(', '.join([f'{field.capitalize()} - {round(missing_counts[field]/len(data), 4)*100}%' for field in fields]))
    print(f'Минимальное количество слов - {min(word_counts)}')
    print(f"Максимальное количество слов: {max(word_counts)}")
    print(f"Среднее количество слов: {round(sum(word_counts)/len(word_counts), 0)}")
    print(f"Медианное количество слов: {median_words}")

if __name__ == "__main__":
    main()