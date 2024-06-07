import os
import inquirer
import subprocess
import readline


cypress_features_dir = os.path.join('cypress', 'features')
cypress_step_definitions_dir = os.path.join(cypress_features_dir, 'step_definitions')
temp_feature_file_path = os.path.join(cypress_features_dir, 'temp_interactive_test.feature')
temp_step_definitions_file_path = os.path.join(cypress_step_definitions_dir, 'temp_interactive_test_steps.js')
history_file_path = 'command_history.log'
ending_step = ["cy.wait(786);", "cy.pause();"][0]  # pause or wait 

collected_features = []
def write_feature():
    temp_interactive_test_feature = f"""
Feature: Interactive Cypress Test
Scenario: Run interactive commands
    {'\n'.join(collected_features)}
    And I run the commands
    """
    with open(temp_feature_file_path, 'w') as f:
        f.write(temp_interactive_test_feature)


collected_steps = []
def write_step():
    temp_interactive_test_steps = \
        "import { Given, When, Then } from '@badeball/cypress-cucumber-preprocessor'" + "\n\n" + \
        "Given('I run the commands', () => {" + "\n\n" + \
        '\n'.join(collected_steps) + "\n" + \
        ending_step + "\n" + \
        "});"
    with open(temp_step_definitions_file_path, 'w') as f:
        f.write(temp_interactive_test_steps)


# Function to load history from the history file
def load_history():
    if os.path.exists(history_file_path):
        readline.read_history_file(history_file_path)

# Function to save history to the history file
def save_history():
    readline.write_history_file(history_file_path)

# Function to delete history to the history file
def delete_history():
    readline.clear_history()
    if os.path.exists(temp_feature_file_path):
        os.remove(temp_feature_file_path)
    if os.path.exists(temp_step_definitions_file_path):
        os.remove(temp_step_definitions_file_path)
    if os.path.exists(history_file_path):
        os.remove(history_file_path)
    # open(history_file_path, 'w').close()

def launch_cypress():
    subprocess.run(['npx', 'cypress', 'run', '--spec', temp_feature_file_path, '--headed'], check=True)    


# write a step file since we dont have one yet:
if not os.path.exists(temp_step_definitions_file_path):
    write_step()
# write a feature file since we dont have one yet:
    write_feature()
# Load command history from history file
load_history()

def get_multiline_input(prompt):
    print(prompt)
    lines = []
    while True:
        line = input()
        if line.strip() == "'''":
            break
        lines.append(line)
    return "\n".join(lines)

while True:
    # Take interactive input
    questions = [
        inquirer.Text('command', message="Enter your Cypress feature step (or type 'exit' to quit)")
    ]
    answers = inquirer.prompt(questions)
    current_command = answers['command']
    
    if current_command.lower() == 'exit':
        break
    # Log the command to history
    readline.add_history(current_command)
    save_history()

    if current_command.lower() == 'delete':
        delete_history()
        break

    if current_command.startswith("'''"):
        print("Enter your code block (end with '''):")
        multiline_input = get_multiline_input("Enter your code block (end with '''):")
        current_command = multiline_input

    if 'Given' in current_command or 'When' in current_command or 'Then' in current_command or 'And' in current_command:
        collected_features.append(current_command)
        write_feature()
    else:
        collected_steps.append(current_command)
        write_step()

    # Launch Cypress
    launch_cypress()
