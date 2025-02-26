import os


def _set_env_var(key: str, value: str) -> None:
    os.environ[key] = value
    print(f"--> setting var {key.upper()} = {value}")


def set_env_vars(build_settings: dict, dist_info: dict):
    print(f"-> Setting Environment Variables")
    for each_key, each_val in build_settings.env_vars.items():
        _set_env_var(each_key, each_val)
    _set_env_var("SM_TOXVERSION", dist_info.get('major_minor', 'dev'))


def _remove_env_var(key: str) -> None:
    del os.environ[key]
    print(f"--> removing var {key.upper()}")


def clear_env_vars(build_settings: dict):
    print(f"-> Cleaning up Environment Variables")
    for each_key in build_settings.env_vars.keys():
        _remove_env_var(each_key)
    _remove_env_var("SM_TOXVERSION")
