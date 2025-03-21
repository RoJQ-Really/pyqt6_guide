import sys,copy
if sys.platform == 'win32':
    import winreg

    def read_registry_value(hive, key_path, value_name):
        """
        Читает значение из реестра Windows.

        :param hive: Корневой ключ реестра (например, winreg.HKEY_LOCAL_MACHINE).
        :param key_path: Путь к ключу реестра (например, r"SOFTWARE\Microsoft\Windows\CurrentVersion").
        :param value_name: Имя значения, которое нужно прочитать (например, "ProgramFilesDir").
        :return: Значение из реестра или None, если значение не найдено.
        """
        try:
            # Открываем ключ реестра
            with winreg.OpenKey(hive, key_path, 0, winreg.KEY_READ) as key:
                # Читаем значение
                value, _ = winreg.QueryValueEx(key, value_name)
                return copy.deepcopy(value)
        except FileNotFoundError:
            print(f"Ключ реестра '{key_path}' или значение '{value_name}' не найдены.")
        except PermissionError:
            print(f"Нет доступа к ключу реестра '{key_path}'.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        return None
else: 
    
    def read_registry_value(*args):
        return None