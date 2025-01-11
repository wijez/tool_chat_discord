def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            messages = file.readlines()
        return [message.strip() for message in messages]
    except OSError as e:
        print(f"Không thể mở file: {e}")
        return []
