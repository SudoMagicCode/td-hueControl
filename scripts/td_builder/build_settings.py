import project_settings

release_dir: str = f"release"
package_dir: str = f"{release_dir}/package"
dest_dir: str = f"{package_dir}/{project_settings.COMP_NAME}"
log_file: str = f"{package_dir}/log.txt"
td_package_file: str = f"{dest_dir}/tdPackages.yaml"

env_vars: dict = {
    "SM_BUILD": "TRUE",
    "SM_PRIVACY": "FALSE",
    "SM_SAVE_PATH": f"../{dest_dir}",
    "SM_COMP_NAME": project_settings.COMP_NAME,
    "SM_LOG_FILE": f"../{log_file}",
    "SM_REPO": project_settings.REPO,
    "SM_TD_PACKAGE_FILE": f"../{td_package_file}"
}
