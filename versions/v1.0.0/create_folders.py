# Use this script to create the folder structure based on tag, type, and action.
# Credit to ChatGPT.

import os

folder_structure = {
    "Collectible": {
        "Approval": ["Approve", "Revoke"],
        "Burn": [],
        "Mint": [],
        "Trade": ["Buy", "Sell"],
        "Transfer": [],
    },
    "Exchange": {
        "Swap": [],
        "Liquidity": ["Add", "Remove", "Collect"],
        "Staking": ["Stake", "Unstake", "Claim"],
    },
    "Metaverse": {
        "Burn": [],
        "Mint": [],
        "Trade": ["Buy", "Sell", "List"],
        "Transfer": [],
    },
    "RSS": {"Feed": []},
    "Social": {
        "Comment": [],
        "Mint": [],
        "Post": [],
        "Profile": ["Create", "Update"],
        "Revise": [],
        "Reward": [],
        "Share": [],
    },
    "Transaction": {
        "Approval": ["Approve", "Revoke"],
        "Bridge": ["Withdraw", "Deposit"],
        "Burn": [],
        "Mint": [],
        "Transfer": [],
    },
}


# Adjust the function to work with the new structure
def create_folder_structure_with_action(folder_structure):
    for tag, types in folder_structure.items():
        tag_folder = tag
        os.makedirs(tag_folder, exist_ok=True)

        tag_main_adoc = os.path.join(tag_folder, "main.adoc")
        if not os.path.exists(tag_main_adoc):
            with open(tag_main_adoc, "w") as file:
                file.write(f"== {tag}\n")

        for type, actions in types.items():
            type_folder = os.path.join(tag_folder, type)
            os.makedirs(type_folder, exist_ok=True)

            type_main_adoc = os.path.join(type_folder, "main.adoc")
            type_main_exists = os.path.exists(type_main_adoc)
            if not type_main_exists:
                with open(type_main_adoc, "w") as type_file:
                    type_file.write(f"=== {type}\n")

            for action in actions:
                action_file_path = os.path.join(type_folder, f"{action}.adoc")
                if not os.path.exists(action_file_path):
                    with open(action_file_path, "w") as action_file:
                        action_file.write(f"==== {action}\n")

                    if not type_main_exists:
                        with open(type_main_adoc, "a") as type_file:
                            type_file.write(f"include::{action}.adoc[]\n")

            if not type_main_exists:
                with open(tag_main_adoc, "a") as tag_file:
                    tag_file.write(f"include::{type}/main.adoc[]\n")


def create_global_main_adoc(folder_structure, main_adoc_path="main.adoc"):
    existing_tags = set()

    # Check if main.adoc already exists and read its content
    if os.path.exists(main_adoc_path):
        with open(main_adoc_path, "r") as main_file:
            for line in main_file:
                if line.startswith("include::") and "/main.adoc[]" in line:
                    existing_tag = line.split("/")[0].split("::")[1]
                    existing_tags.add(existing_tag)

    # Write the new include statements to main.adoc
    with open(main_adoc_path, "a") as main_file:
        for tag in folder_structure.keys():
            if tag not in existing_tags:
                main_file.write(f"include::{tag}/main.adoc[]\n")


# Function to create folder structure
create_folder_structure_with_action(folder_structure)

# Create the global main.adoc
create_global_main_adoc(folder_structure)
